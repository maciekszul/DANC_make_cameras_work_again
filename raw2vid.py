import numpy as np
import cv2
import time

raw = np.load("frames_999_duration_5.npy")
f_size = (1280, 1024)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

vid = cv2.VideoWriter(
    "frames_999_duration_5.avi",
    fourcc,
    float(200),
    f_size
)

for i in raw:
    img = cv2.cvtColor(i, cv2.COLOR_BAYER_BG2BGR)
    vid.write(img)

vid.release()