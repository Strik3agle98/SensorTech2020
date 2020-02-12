import cv2
import numpy as np
from math import sqrt
import imutils
import os

acc = 0


pink = ([[1.9634703196347034, 1.0, 2.317351598173516], [142, 66, 177]])
purple = np.array([[2.3344827586206898, 1.0, 2.1758620689655173],[137, 58, 124]])
dblue = np.array([[2.9658385093167703, 1.0, 0.43478260869565216], [163, 68, 27]])
blue = np.array([[1.757133956386293, 1.0, 0.33809968847352024], [183, 118, 39]])
lgreen = np.array([[0.3708884688090737, 1.0, 0.6181474480151229], [34, 95, 65]])
dgreen = np.array([[1.068354430379747, 1.0, 0.3848101265822785], [85, 79, 30]])
dgreen2 = np.array([[1.072599531615925, 1.0, 0.43559718969555034],[91, 84, 36]])
yellow = np.array([[0.1394169835234474, 1.0, 1.2065906210392903], [23, 159, 192]])
orange = np.array([[0.5823674911660777, 1.0, 3.3625441696113072], [29, 56, 179]])
red = np.array([[0.8119298245614036, 1.0, 3.4754385964912277], [35, 45, 208]])
brown = np.array([[0.8375, 1.0, 2.1416666666666666], [40, 48, 102]])

colors = [pink, purple, dblue, blue, lgreen, yellow, orange, red, brown, dgreen, dgreen2]
# colors = [pink, purple, dblue, blue, lgreen]
def cal_dist(base, res):
    # print('res')
    # print(res)
    # print('base')
    # print(base)
    s = np.sum(res, axis=0)
    res = [res[0] / res[1], res[1] / res[1], res[2] / res[1]]
    # print(res)
    return int(sqrt((base[0]-res[0])**2+(base[1]-res[1])**2)+(base[2]-res[2])**2)


def process(cap):
    while 1:
        _, frame = cap.read()
        gframe = cv2.GaussianBlur(frame, (5, 5), 0)
        # hsv = cv2.cvtColor(gframe, cv2.COLOR_BGR2HSV_FULL)
        drawing = frame.copy()
        gray = cv2.cvtColor(gframe, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 0, 500, apertureSize=5)
        edges = cv2.dilate(edges, None)
        copy = edges.copy()

        contours, _hierachy = cv2.findContours(copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contours = imutils.grab_contours(contours)
        image = 0

        for cnt in contours:
            cnt_len = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt,0.02*cnt_len,True) #Removes tiny deviations, tries to go for straight lines.
            if len(approx) == 4 and cv2.contourArea(approx) > 1000 and cv2.isContourConvex(approx) and cv2.contourArea(approx) < 10000: #Lines, should be square.
                # print('square1')
                rect = cv2.boundingRect(approx)
                if rect[2] > 10:
                    # print('square0')
                    W = rect[2]
                    H = rect[3]
                    L = []
                    for color in colors:
                        # mask = cv2.inRange(hsv[int(rect[1])+int(H/3):int(rect[1])+2*int(H/3),
                        #                    int(rect[0])+int(W/3):int(rect[0])+2*int(W/3)], color[0], color[1])
                        L.append(cal_dist(color[0], frame[int(rect[1])+int(H/2)][int(rect[0])+int(W/2)]))
                    m = min(L)
                    idx = L.index(m)
                    # print(colors[idx])
                    cv2.rectangle(drawing, (int(rect[0]), int(rect[1])),(int(rect[0] + rect[2]), int(rect[1] + rect[3])),colors[idx][1], -1)
        # drawing = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR_FULL)
        cv2.imshow('image', frame)
        cv2.imshow('drawing', drawing)
        # cv2.imshow('area', image)

        if cv2.waitKey(1) & 0xFF == 27:
            break

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    process(cap)
    cv2.destroyAllWindows()
    cap.release()