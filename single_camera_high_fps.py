from ximea import xiapi
import cv2
import time

cam1 = xiapi.Camera()
cam1.disable_auto_bandwidth_calculation()
cam1.open_device_by_SN("39050251")
framerate = 200.0
shutter = int((1/framerate)*1e+6)-1000
gain = 15

cam1.set_sensor_feature_value(1)
cam1.set_exposure(shutter)
cam1.set_gain(gain)
cam1.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
cam1.set_framerate(framerate)
cam1.set_imgdataformat("XI_RGB24")

# cam1.set_limit_bandwidth()

cam1.enable_auto_wb()

img1 = xiapi.Image()

start = time.monotonic()

cam1_list = []
try:
    cam1.start_acquisition()
    while (time.monotonic() - start) <= 2:
        cam1.get_image(img1)
        cam1_data = img1.get_image_data_numpy()
        cam1_list.append(cam1_data[:,:,:3])
        print(cam1.get_framerate())
except:
    print("error")

cam1.stop_acquisition()
cam1.close_device()