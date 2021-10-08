import numpy as np
import cv2
import time
import sys
import os.path as op


try:
    path = str(sys.argv[1])
except:
    print("incorrect path")
    sys.exit()

filename = path.split("/")[-1].split(".")[0]


raw = np.load(path, allow_pickle=True)
f_size = (1280, 1024)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

vid = cv2.VideoWriter(
    "{}.avi".format(filename),
    fourcc,
    float(200),
    f_size
)

for i in raw:
    img = cv2.cvtColor(i, cv2.COLOR_BAYER_BG2BGR)
    vid.write(img)

vid.release()