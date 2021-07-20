from ximea import xiapi
import cv2
import time
import numpy as np

framerate = 10.0
shutter = int((1/framerate)*1e+6)-1000

cam = xiapi.Camera()
img = xiapi.Image()

cam.open_device_by_SN("06955451")
cam.set_sensor_feature_value(1)
cam.set_imgdataformat("XI_RGB24")
cam.enable_auto_wb()
cam.disable_auto_bandwidth_calculation()
# cam.set_trigger_source("XI_TRG_SOFTWARE")
cam.set_counter_selector("XI_CNT_SEL_API_SKIPPED_FRAMES")

# cam.set_buffer_policy("XI_BP_SAFE")
# cam.get_trigger_software() trigger
# cam.get_timestamp() timestamp
# cam.get_counter_value() dropped frames counter

cam.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
cam.set_framerate(framerate)
cam.set_exposure(shutter)
cam.set_gain(5)
# cam.set_acq_buffer_size(200*1024*1024)
# cam.set_buffers_queue_size(100)
# print(cam.get_buffers_queue_size_minimum())
# print(cam.get_buffers_queue_size_maximum())

cam_list = []
metadata = {
    "frame_timestamp": [],
    "frames_dropped": [],
    "framerate": framerate,
    "shutter_speed": shutter,
}
cam.start_acquisition()
start = time.monotonic()
while (time.monotonic() - start) < 1:
    cam.get_image(img)
    cam_list.append(img)

cam.stop_acquisition()
cam.close_device()
print(len(cam_list))


print(cam_list[0].get_image_data_numpy().shape)
# frames = np.array([i.get_image_data_numpy() for i in cam_list])
# np.save("frames.npy", frames)

# cam.set_exposure(int((1/framerate)*1e+6)-100)
# cam.set_gain(5)
# cam.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
# cam.set_framerate(framerate)
# cam.set_imgdataformat("XI_RAW8")
# cam.enable_auto_wb()


# cam.set_trigger_source("XI_TRG_SOFTWARE")

# img = xiapi.Image()

# cam.start_acquisition()

# start = time.monotonic()
# cam.set_trigger_selector("XI_TRG_SEL_FRAME_START")
# while (time.monotonic() - start) <= 1:
#     print("x")
# cam.get_image(img)
# output = img.get_image_data_numpy()
# cam.stop_acquisition()
# cam.close_device()


# print(output)
