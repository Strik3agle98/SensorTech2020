#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:
$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import pandas as pd

df = pd.DataFrame(columns=['0'])

PORT_NAME = 'COM7'


def run():
    global df
    i = 0
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    data = []
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for scan in lidar.iter_scans():
            data.append(np.array(scan))
            deg0 = scan[0][2]-4500
            print('iteration: ' + str(i))
            i+=1
            df2 = pd.DataFrame([[deg0]], columns=['0'])
            df = pd.concat([df, df2])
            if(len(df) > 700):
                df.to_csv('0_450.csv')
                break
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    # print(data)
    # np.save(path, np.array(data))

if __name__ == '__main__':
    run()