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
        src[i] = np.array(src[i]).astype(np.float32)
        for j in range(2):
            src[i][j] = np.array(src[i][j]).astype(np.float32)
        print(src[i].shape)

    accT = np.array([[np.cos(0), -np.sin(0), 0],
                      [np.sin(0), np.cos(0), 0],
                      [0, 0, 1]])
    result = []
    for i in range(len(src)):
        print("ICP iteration: " + str(i))
        if i == 0:
            template = src[0]
        else:
            data = src[i]
            # data = cv2.transform(np.array([data.T], copy=True).astype(np.float32), accT).T
            T,error = icp.icp(data,template, accT)
            #updating accT
            accT[0, 2] += T[0, 2]
            accT[1, 2] += T[1, 2]
            print("local transform: ")
            print(T)
            print("acc transform: ")
            print(accT)
            dx = T[0, 2]
            dy = T[1, 2]
            rotation = np.arcsin(T[0, 1]) * 360 / 2 / np.pi
            result.append(cv2.transform(np.array([data.T], copy=True).astype(np.float32), T).T)
            #all layer as template
            # L0 = []
            # L1 = []
            # for j in range(len(template[0])):
            #     L0.append(template[0][j])
            #     L1.append(template[1][j])
            # for j in range(len(result[i - 1][0])):
            #     L0.append(result[i - 1][0][j][0])
            #     L1.append(result[i - 1][1][j][0])
            # template = np.array([np.array(L0),np.array(L1)])

            # #latest layer as template
            L0 = []
            L1 = []
            for j in range(len(result[i - 1][0])):
                L0.append(result[i - 1][0][j][0])
                L1.append(result[i - 1][1][j][0])
            template = np.array([np.array(L0),np.array(L1)])

            matplotlib.pyplot.scatter(result[i-1][0], result[i-1][1], s=10, label="result: "+str(i)+str(rotation)+"° - "+str([dx,dy]))
    print("Final transformation: ")
    print(accT)

    result.append(cv2.transform(np.array([data.T], copy=True).astype(np.float32), T).T)
    # matplotlib.pyplot.scatter(template[0], template[1], s=10, label="template")
    matplotlib.pyplot.legend(loc="upper left")
    matplotlib.pyplot.axis('square')
    matplotlib.pyplot.show()