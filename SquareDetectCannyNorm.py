import cv2
import numpy as np
from math import sqrt
import imutils
import os


pink = ([[0.36883117, 0.17142857, 0.45974026], [142, 66, 177]])
purple = np.array([[0.42946708, 0.18181818, 0.38871473],[137, 58, 124]])
dblue = np.array([[0.61057692, 0.26923077, 0.12019231], [109, 43, 16]])
blue = np.array([[0.53823529, 0.34705882, 0.11470588], [141, 92, 30]])
lgreen = np.array([[0.17525773, 0.48969072, 0.33505155], [34, 95, 65]])
forest = np.array([[0.39156627, 0.42168675, 0.18674699], [85, 79, 30]])
dgreen = np.array([[0.40972222, 0.42361111, 0.16666667],[91, 84, 36]])
yellow = np.array([[0.06149733, 0.42513369, 0.51336898], [23, 159, 192]])
orange = np.array([[0.15,       0.22307692, 0.62692308], [30, 56, 175]])
red = np.array([[0.18584071, 0.18584071, 0.62831858], [42, 42, 142]])
brown = np.array([[0.23316062, 0.2642487, 0.50259067], [45, 51, 97]])

colors = [pink, purple, dblue, blue, lgreen, yellow, orange, red, brown, forest, dgreen]
text = ["pink", "purple", "darkblue", "blue", "green", "yellow", "orange", "red", "brown", "forest", "darkgreen"]
# colors = [pink, purple, dblue, blue, lgreen]
def cal_dist(base, res):
    # print('res')
    # print(res)
    # print('base')
    # print(base)
    s = np.sum(res, axis=0)
    res = [res[0] / s, res[1] / s, res[2] / s]
    # print(res)
    # print(res)
    return sqrt((base[0]-res[0])**2+(base[1]-res[1])**2+(base[2]-res[2])**2)


def process(cap):
    acc = 0
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
                    if W/H >= 0.8 and W/H <= 1.2:
                        L = []
                        for color in colors:
                            # mask = cv2.inRange(hsv[int(rect[1])+int(H/3):int(rect[1])+2*int(H/3),
                            #                    int(rect[0])+int(W/3):int(rect[0])+2*int(W/3)], color[0], color[1])
                            L.append(cal_dist(color[0], frame[int(rect[1])+int(H/2)][int(rect[0])+int(W/2)]))
                        m = min(L)
                        idx = L.index(m)
                        # print(colors[idx])
                        cv2.putText(drawing, text[idx], (int(rect[0]), int(rect[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, colors[idx][1], 2, cv2.LINE_AA)
                        cv2.rectangle(drawing, (int(rect[0]), int(rect[1])),(int(rect[0] + rect[2]), int(rect[1] + rect[3])),colors[idx][1], -1)
        # drawing = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR_FULL)
        cv2.imshow('image', frame)
        cv2.imshow('drawing', drawing)
        # cv2.imshow('area', image)
        if cv2.waitKey(1) & 0xFF == 32:
            cv2.imwrite('frame' + str(acc) + '.jpg', frame)
            cv2.imwrite('draw' + str(acc) + '.jpg', drawing)
            print('saved: '+str(acc))
            acc += 1
        if cv2.waitKey(1) & 0xFF == 27:
            break

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    process(cap)
    cv2.destroyAllWindows()
    cap.release()