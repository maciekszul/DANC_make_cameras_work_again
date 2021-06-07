import numpy as np
from ximea import xiapi
import cv2
from cv2 import aruco
import time

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters_create()


cam = xiapi.Camera()

cam.open_device_by_SN("32052251")

framerate = 30.0

cam.set_exposure(int((1/framerate)*1e+6)-100)
cam.set_gain(5)
cam.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
cam.set_framerate(framerate)

cam.set_imgdataformat("XI_RGB32")
cam.enable_auto_wb()

img = xiapi.Image()

cam.start_acquisition()

try:
    t0 = time.time()
    while True:
        cam.get_image(img)
        data = img.get_image_data_numpy()
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters
        )

        detected = [i.reshape((-1, 1, 2)).astype(np.int32) for i in corners]

        cv2.polylines(data, detected, True, (0,255,0), 3)

        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        text = "time: {}".format(np.round(time.time()-t0, 1))
        text1 = "framerate: {}".format(cam.get_framerate())
        text2 = "gain: {} dB".format(cam.get_gain())
        text3 = "exposure: {} s".format(cam.get_exposure() / 1e+6)
        text4 = "chip temp: {}*C".format(cam.get_chip_temp())
        cv2.putText(data, text, (20,20), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text1, (20,40), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text2, (20,60), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text3, (20,80), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text4, (20,100), font, 1, (255, 255, 255), 1)

        cv2.imshow("cam", data)

        cv2.waitKey(1)

except KeyboardInterrupt:
    cv2.destroyAllWindows()

except:
    cam.stop_acquisition()
    cam.close_device()

try:
    cam.stop_acquisition()
    cam.close_device()
except:
    print("done")
