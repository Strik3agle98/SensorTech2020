import cv2
import numpy as np
import imutils
import os

acc = 0

#index0=lower, index1=upper, index3=displaycolorHSV
pink = np.array([[140,130,150], [170,255,255], [155,255,255]])
purple = np.array([[130,110,100], [160,255,200], [135,160,160]])
dblue = np.array([[100,130,150], [130,255,255], [120,255,255]])
blue = np.array([[90,130,150], [110,255,255], [100,255,255]])
lgreen = np.array([[40,60,20], [75,255,255], [60,255,255]])
dgreen = np.array([[80,60,40], [105,255,140], [100,255,120]])
dgreen2 = np.array([[80,60,10], [95,255,100], [88,255,255]])
yellow = np.array([[20,70,150], [40,255,255], [30,255,255]])
orange = np.array([[4,70,170], [20,255,255], [10,255,255]])
red = np.array([[0,70,150], [4,255,255], [0,255,255]])
red2 = np.array([[175,70,150], [179,255,255], [0,255,255]])
brown = np.array([[175,70,100], [179,230,200], [0,150,150]])
brown2 = np.array([[0,100,100], [10,230,200], [0,150,150]])

colors = [pink, purple, dblue, blue, lgreen, yellow, orange, red, red2, brown, brown2, dgreen, dgreen2]

cap = cv2.VideoCapture(0)

for i in range(12):
    frame = cv2.imread(str(i)+'.jpg')
    gframe = cv2.GaussianBlur(frame, (5, 5), 0)
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
        if len(approx) == 4 and cv2.contourArea(approx) > 1000 and cv2.isContourConvex(approx): #Lines, should be square.
            print('square1')
            rect = cv2.boundingRect(cnt)
            if rect[2] > 10:
                print('square0')
                cv2.rectangle(frame, (int(rect[0]), int(rect[1])),
                              (int(rect[0] + rect[2]), int(rect[1] + rect[3])),
                              (0,255,0), -1)



    cv2.imshow('image', frame)
    cv2.imshow('edges', edges)
    # cv2.imshow('area', image)
    cv2.waitKey(0)



cv2.destroyAllWindows()
cap.release()