import numpy as np
from ximea import xiapi
import cv2
from subprocess import call
import os

cam1 = xiapi.Camera()
cam1.open_device_by_SN("32052251")
cam2 = xiapi.Camera()
cam2.open_device_by_SN("06955451")

framerate = 120.0
shutter = int((1/framerate)*1e+6)-100
gain = 5

cam1.set_exposure(shutter)
cam1.set_gain(gain)
cam1.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
cam1.set_framerate(framerate)
cam1.set_imgdataformat("XI_RGB32")
cam1.enable_auto_wb()

cam2.set_exposure(shutter)
cam2.set_gain(gain)
cam2.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
cam2.set_framerate(framerate)
cam2.set_imgdataformat("XI_RGB32")
cam2.enable_auto_wb()

img1 = xiapi.Image()
img2 = xiapi.Image()

cam1.start_acquisition()
cam2.start_acquisition()

font = cv2.FONT_HERSHEY_COMPLEX_SMALL



fr = 0
try:
    while True:
        cam1.get_image(img1)
        cam1_data = img1.get_image_data_numpy()
        cam2.get_image(img2)
        cam2_data = img2.get_image_data_numpy()

        data = np.hstack([cam1_data, cam2_data])
        cv2.putText(data, "cam1: ca 30 deg", (20,20), font, 1, (255, 255, 255), 1)
        cv2.putText(data, "cam2: perpendicular", (1300,20), font, 1, (255, 255, 255), 1)

        cv2.imshow("cam", data)
        cv2.imwrite("data/mov-{}.jpg".format(str(fr).zfill(8)), data)
        fr += 1
        cv2.waitKey(1)

except KeyboardInterrupt:
    cv2.destroyAllWindows()

output_path = "/home/mszul/git/DANC_make_cameras_work_again"
data_path = os.path.join(output_path, "data")

# os.chdir(data_path)
# call([
#     "ffmpeg", 
#     "-framerate", str(framerate), 
#     "-i", "mov-%08d.jpg", 
#     os.path.join(output_path, "movie.mp4")])

# call(["rm", data_path + "*"])

cam1.stop_acquisition()
cam2.stop_acquisition()
cam1.close_device()
cam2.close_device()