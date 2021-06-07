from ximea.xidefs import XI_PRM_SENS_DEFECTS_CORR_LIST_CONTENT
import numpy as np
from ximea import xiapi
import ffmpeg
import os
import cv2
import time

framerate = 120.0
shutter = int((1/framerate)*1e+6)-100
gain = 5
f_size = (1280, 1024)
img_format = "XI_RGB32"

cam1 = xiapi.Camera()
cam1.open_device_by_SN("32052251")
cam1.set_exposure(shutter)
cam1.set_gain(gain)
cam1.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
cam1.set_framerate(framerate)
cam1.set_imgdataformat(img_format)
cam1.enable_auto_wb()
img1 = xiapi.Image()
cam1.start_acquisition()

cam2 = xiapi.Camera()
cam2.open_device_by_SN("06955451")
cam2.set_exposure(shutter)
cam2.set_gain(gain)
cam2.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
cam2.set_framerate(framerate)
cam2.set_imgdataformat(img_format)
cam2.enable_auto_wb()
img2 = xiapi.Image()
cam2.start_acquisition()

cam1_list = []
cam2_list = []

start = time.monotonic()
try:
    
    while (time.monotonic() - start) <= 5:
        cam1.get_image(img1)
        cam1_data = img1.get_image_data_numpy()
        cam1_list.append(cam1_data[:,:,:3])
        cam2.get_image(img2)
        cam2_data = img2.get_image_data_numpy()
        cam2_list.append(cam2_data[:,:,:3])

except:
    print("error")

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
cam1_vid = cv2.VideoWriter(
    "output_cam1_{}_frames.avi".format(len(cam1_list)), 
    fourcc, 
    float(framerate), 
    f_size
)
[cam1_vid.write(i) for i in cam1_list]
cam1_vid.release()


cam2_vid = cv2.VideoWriter(
    "output_cam2_{}_frames.avi".format(len(cam2_list)), 
    fourcc, 
    float(framerate), 
    f_size
)
[cam2_vid.write(i) for i in cam2_list]
cam2_vid.release()

cam1.stop_acquisition()
cam1.close_device()
cam2.stop_acquisition()
cam2.close_device()