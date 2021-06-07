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
cam.set_gain(15)
cam.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
cam.set_framerate(framerate)

cam.set_imgdataformat("XI_RGB32")
cam.enable_auto_wb()

img = xiapi.Image()

cam.start_acquisition()

images = []

try:
    t0 = time.time()
    while True:
        cam.get_image(img)
        data = img.get_image_data_numpy()
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters
        )

        if len(corners) > 15:
            images.append(data)

        detected = [i.reshape((-1, 1, 2)).astype(np.int32) for i in corners]
        cv2.polylines(data, detected, True, (0,255,0), 3)

        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        text = "time: {}".format(np.round(time.time()-t0, 1))
        text1 = "framerate: {}".format(cam.get_framerate())
        text2 = "gain: {} dB".format(cam.get_gain())
        text3 = "exposure: {} s".format(cam.get_exposure() / 1e+6)
        text4 = "ids detected: {}".format(len(corners))
        text5 = "imgs captured: {}".format(len(images))
        cv2.putText(data, text, (20,20), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text1, (20,40), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text2, (20,60), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text3, (20,80), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text4, (20,100), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text5, (20,120), font, 1, (255, 255, 255), 1)

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


def read_chessboards(images):
    """
    Charuco base pose estimation.
    """
    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

    for frame in images:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)

        if len(corners)>0:
            # SUB PIXEL DETECTION
            for corner in corners:
                cv2.cornerSubPix(gray, corner,
                                 winSize = (3,3),
                                 zeroZone = (-1,-1),
                                 criteria = criteria)
            res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,board)
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                allCorners.append(res2[1])
                allIds.append(res2[2])

        decimator+=1

    imsize = gray.shape
    return allCorners, allIds, imsize

board = aruco.CharucoBoard_create(7, 5, 1, .8, aruco_dict)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

allCorners, allIds, imsize = read_chessboards(images)

ix = [ix for ix, i in enumerate(allIds) if i.size > 4]
allCorners = [allCorners[i] for i in ix]
allIds = [allIds[i] for i in ix]

# def calibrate_camera(allCorners,allIds,imsize):
#     """
#     Calibrates the camera using the dected corners.
#     """
#     print("CAMERA CALIBRATION")

#     cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
#                                  [    0., 1000., imsize[1]/2.],
#                                  [    0.,    0.,           1.]])

#     distCoeffsInit = np.zeros((5,1))
#     flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
#     #flags = (cv2.CALIB_RATIONAL_MODEL)
#     (ret, camera_matrix, distortion_coefficients0,
#      rotation_vectors, translation_vectors,
#      stdDeviationsIntrinsics, stdDeviationsExtrinsics,
#      perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
#                       charucoCorners=allCorners,
#                       charucoIds=allIds,
#                       board=board,
#                       imageSize=imsize,
#                       cameraMatrix=cameraMatrixInit,
#                       distCoeffs=distCoeffsInit,
#                       flags=flags,
#                       criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

#     return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors

# ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners, allIds, imsize)



cam.open_device_by_SN("32052251")

framerate = 30.0

cam.set_exposure(int((1/framerate)*1e+6)-100)
cam.set_gain(15)
cam.set_acq_timing_mode("XI_ACQ_TIMING_MODE_FRAME_RATE")
cam.set_framerate(framerate)

cam.set_imgdataformat("XI_RGB32")
cam.enable_auto_wb()

img = xiapi.Image()

cam.start_acquisition()
length_of_axis = 0.1

try:
    t0 = time.time()
    while True:
        cam.get_image(img)
        data = img.get_image_data_numpy()
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters
        )
        for i in range(len(tvecs)):
            imaxis = cv2.aruco.drawAxis(data, mtx, dist, rvecs[i], tvecs[i], length_of_axis)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        text = "time: {}".format(np.round(time.time()-t0, 1))
        text1 = "framerate: {}".format(cam.get_framerate())
        text2 = "gain: {} dB".format(cam.get_gain())
        text3 = "exposure: {} s".format(cam.get_exposure() / 1e+6)

        cv2.putText(data, text, (20,20), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text1, (20,40), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text2, (20,60), font, 1, (255, 255, 255), 1)
        cv2.putText(data, text3, (20,80), font, 1, (255, 255, 255), 1)


        cv2.imshow("cam", imaxis)

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