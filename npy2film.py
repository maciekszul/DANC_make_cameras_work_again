import numpy as np
import lycon
import cv2

frames = np.load("output.npy")

width = 2560
height = 1024
channel = 3
fps = 120
dur = 5


fourcc = cv2.VideoWriter_fourcc(*"MJPG")
video = cv2.VideoWriter("output.avi", fourcc, float(fps), (width, height))

for i in range(frames.shape[0]):
    # filename = "data/{}.jpg".format(str(i).zfill(4))
    # lycon.save(filename, frames[i])
    print(frames[i][:,:,:-1].shape)
    video.write(frames[i][:,:,:-1])
video.release()