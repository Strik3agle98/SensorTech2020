#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:
$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import pandas as pd
import math

PORT_NAME = 'COM7'


def run():
    data = []
    i = 0
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for scan in lidar.iter_scans():
            L = {}
            #scan = [({some number}, {angle(deg)}, {distance(mm)}), ...]
            for e in scan:
                L[e[1]] = e[2]
            # print(L)
            data.append(L)
            i+=1
            print("iteration: "+str(i))
            if(i>=100):
                print('Stoping.')
                break
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    data = np.array(data)
    print(data.shape)
    name = "data8.npy"
    np.save('C:/Users/Strik3agle/Documents/SensorTech/Lidar/data/'+name, np.array(data))
    print("saved to "+name)

if __name__ == '__main__':
    run()