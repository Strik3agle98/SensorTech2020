import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    #print(frame.shape)

    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([10,150,170])
    upper = np.array([32,255,255])
    
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    # res = cv2.cvtColor(res, cv2.COLOR_HS)

    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 200, param1=100, param2=11, minRadius=10)
    if circles is not None:
        print(circles)
        for circle in circles:
            x, y, radius = np.around(circle, decimals=1)[0]
            if radius > 10:
                color = (255,0,255)
                color2 = (0,255,0)
                cv2.circle(frame, (x, y), radius, color, 2)
                cv2.circle(frame, (x, y), 2, color2, 2)

    # print(frame.shape)
    frame = cv2.vconcat([frame, res])
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
cap.release()