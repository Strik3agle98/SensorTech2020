#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:
$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import math
import cv2
import matplotlib.pyplot
import icp


def cartesian():
    data = []
    for i in range(9):
        array = np.load('C:/Users/Strik3agle/Documents/SensorTech/Lidar/data/data'+str(i)+'.npy', allow_pickle=True)
        L = [[], []]
        for d in array:
            # print(d)
            #scan = [({some number}, {angle(deg)}, {distance(mm)}), ...]
            for e in d:
                L[0].append(math.cos(math.radians(e))*d[e])
                L[1].append(math.sin(math.radians(e))*d[e])
            # print(L)
        data.append(L)
    return data


if __name__ == '__main__':
    src = cartesian()
    print("data converted to cartesian")
    for i in range(len(src)):
        src[i] = np.array(src[i])
        for j in range(2):
            src[i][j] = np.array(src[i][j])
        print(src[i].shape)

    accT = np.array([[np.cos(0), -np.sin(0), 0],
                      [np.sin(0), np.cos(0), 0],
                      [0, 0, 1]])
    for i in range(len(src)):
        if i == 0:
            template = src[i]
        else:
            data = src[i]
            # data = cv2.transform(np.array([data.T], copy=True).astype(np.float32), accT).T
            T,error = icp.icp(data,template)

            print(T)
            break