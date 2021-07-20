from ximea import xiapi
import time
import numpy as np
import multiprocessing as mp
from copy import copy
import json

def shtr_spd(framerate):
    return int((1/framerate)*1e+6)-100

def get_WB_coef(s_n, framerate, shutter, gain):
    cam = xiapi.Camera()
    img = xiapi.Image()
    cam.open_device_by_SN(s_n)
    cam.set_sensor_feature_value(1)
    cam.set_imgdataformat("XI_RGB24")
    cam.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
    cam.set_framerate(framerate)
    cam.set_exposure(shutter)
    cam.set_gain(gain)
    cam.enable_auto_wb()
    cam.start_acquisition()
    start = time.monotonic()
    while (time.monotonic() - start) <= 1:
        cam.get_image(img)

    kR = cam.get_wb_kr()
    kG = cam.get_wb_kg()
    kB = cam.get_wb_kb()

    cam.stop_acquisition()
    cam.close_device()

    return kR, kG, kB


def camera_init(s_n, framerate, shutter, gain):
    cam = xiapi.Camera()
    img = xiapi.Image()
    cam.open_device_by_SN(s_n)
    cam.set_sensor_feature_value(1)
    cam.set_imgdataformat("XI_RAW8")
    cam.disable_auto_bandwidth_calculation()
    cam.set_counter_selector("XI_CNT_SEL_API_SKIPPED_FRAMES")
    cam.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
    cam.set_framerate(framerate)
    cam.set_exposure(shutter)
    cam.set_gain(gain)
    return cam, img


s_n = "06955451"
fps = 200
gain = 5
shutter = shtr_spd(fps)

kR, kG, kB = get_WB_coef(s_n, 30, shutter, gain)

print(kR, kG, kB)

cam, img = camera_init(s_n, fps, shutter, gain)

cam_list = []


# def dump_and_run(list, name):
#     frames = np.array([i.get_image_data_numpy() for i in cam_list])
#     np.save("{}.npy".format(name), frames)

def dump_and_run(lists, name):
    frames = np.array(lists)
    np.save("{}.npy".format(name), frames)


metadata = {
    "frame_timestamp": [],
    "api_frames_dropped": [],
    "framerate": fps,
    "shutter_speed": shutter,
    "gain": gain,
    "sn": s_n,
    "WB_auto_coeff_RGB": [kR, kG, kB]
}

print(cam.get_cfa())

cam.start_acquisition()

start = time.monotonic()
while (time.monotonic() - start) <= 5:
    cam.get_image(img)
    cam_list.append(img.get_image_data_numpy())
    metadata["api_frames_dropped"].append(cam.get_counter_value())
    metadata["frame_timestamp"].append(time.monotonic())

start_x = time.monotonic()

filename = "frames_{}_duration_5".format(len(cam_list))

dump_and_run(cam_list, filename)
stop_x = time.monotonic()
print("GET IMAGE + DUMP:", stop_x - start_x)


cam.stop_acquisition()
cam.close_device()

print("FRAMES:", len(cam_list))

with open("{}.json".format(filename), "w") as fp:
    json.dump(metadata, fp)

