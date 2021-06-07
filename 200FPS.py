from ximea import xiapi
import cv2


cam1 = xiapi.Camera()
cam1.open_device_by_SN("32052251")

framerate = 120.0
shutter = int((1/framerate)*1e+6)-100
gain = 5

# cam1.set_sensor_feature_value(1)
cam1.set_exposure(shutter)
cam1.set_gain(gain)
cam1.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
cam1.set_framerate(framerate)
# cam1.set_imgdataformat("XI_RGB32")
cam1.set_imgdataformat("XI_MONO8")
cam1.enable_auto_wb()


img1 = xiapi.Image()

cam1.start_acquisition()

font = cv2.FONT_HERSHEY_COMPLEX_SMALL

try:
    while True:
        cam1.get_image(img1)
        data = img1.get_image_data_numpy()
        # print(cam1.get_framerate())
        cv2.putText(data, "cam1: ca 30 deg", (20,20), font, 1, (0, 0, 0), 1)
        text1 = "framerate: {}".format(cam1.get_framerate())
        cv2.putText(data, text1, (20,40), font, 1, (0, 0, 0), 1)
        cv2.imshow("cam", data)
        cv2.waitKey(1)

except KeyboardInterrupt:
    cv2.destroyAllWindows()

cam1.stop_acquisition()
cam1.close_device()