import numpy as np
from ximea import xiapi
from cv2 import cv2
import time

cam = xiapi.Camera()

cam.open_device_by_SN("32052251") # init with serial number useful when many

resolution = (1280, 1024) # open cv indexing starts at top left of the image
cam.set_exposure(50000)
cam.set_exp_priority(1)
# rgb32 or mono8 produce 2d array instead of 3d
cam.set_imgdataformat("XI_RGB32")
# cam.set_imgdataformat("XI_MONO8")
# cam.set_imgdataformat("XI_RAW8") #up to 210fps

cam.enable_auto_wb()
# cam.enable_aeag()

img = xiapi.Image()

cam.start_acquisition()

try:
    t0 = time.time()
    while True:
        cam.get_image(img)
        data = img.get_image_data_numpy()
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        text = "time: {}".format(np.round(time.time()-t0, 1))
        text1 = str(cam.get_imgdataformat())
        text2 = str(cam.get_shutter_type())
        text3 = "resolution: {}x{}".format(cam.get_width(), cam.get_height())
        cv2.putText(
            data, text, (20,20), font, 1, (255, 255, 255), 1
            )
        cv2.putText(
            data, text1, (20,40), font, 1, (255, 255, 255), 1
            )
        cv2.putText(
            data, text2, (20,60), font, 1, (255, 255, 255), 1
            )
        cv2.putText(
            data, text3, (20,80), font, 1, (255, 255, 255), 1
            )
        cv2.imshow("cam", data)

        cv2.waitKey(1)
        
except KeyboardInterrupt:
    cv2.destroyAllWindows()

cam.stop_acquisition()
cam.close_device()