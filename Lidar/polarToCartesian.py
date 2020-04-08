#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:
$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import pandas as pd
import math

df = pd.DataFrame(columns=['0'])

PORT_NAME = 'COM7'
data = []

def run():
    global df
    i = 0
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for scan in lidar.iter_scans():
            L = [[],[]]
            #scan = [({some number}, {angle(deg)}, {distance(mm)}), ...]
            for e in scan:
                L[0].append(math.cos(math.radians(e[1]))*e[2])
                L[1].append(math.sin(math.radians(e[1]))*e[2])
            print(L)
            data.append(L)
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    # print(data)
    # np.save(path, np.array(data))

if __name__ == '__main__':
    run()