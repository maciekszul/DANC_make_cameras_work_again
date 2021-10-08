from utilities import files
import numpy as np
import cv2
import time
import sys
import os.path as op
import json
from joblib import Parallel, delayed


try:
    path = str(sys.argv[1])
except:
    print("incorrect path")
    sys.exit()

print(path)

files_npy = files.get_files(path, "", ".npy")[2]
files_npy.sort()
files_json = files.get_files(path, "", ".json")[2]
files_json.sort()

# files_npy_json = list(zip(files_npy, files_json))

# print(files_npy_json)

def convert(file):
    filename = file.split("/")[-1].split(".")[0]
    raw = np.load(file, allow_pickle=True)
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

Parallel(n_jobs=3)(delayed(convert)(file) for file in files_npy)
