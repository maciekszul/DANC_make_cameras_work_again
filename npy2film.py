import numpy as np
import lycon
import cv2
import sys


try:
    path = str(sys.argv[1])
except:
    print("incorrect arguments")
    sys.exit()


frames = np.load(path)

width = 1280
height = 1024
fps = 200
dur = 4


fourcc = cv2.VideoWriter_fourcc(*"MJPG")
video = cv2.VideoWriter("output.avi", fourcc, float(fps), (width, height))

for i in range(frames.shape[0]):
    print(frames[i][:,:,:-1].shape)
    video.write(frames[i][:,:,:-1])
video.release()
