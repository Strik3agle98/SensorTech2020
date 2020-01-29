import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    #print(frame.shape)

    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([10,150,170])
    upper = np.array([32,255,255])
    
    mask = cv2.inRange(hsv, lower, upper)
    #mask = cv2.erode(mask, None, iterations=2)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 200, param1=100, param2=1, minRadius=10)
    if circles is not None:
        print(circles)
        for circle in circles:
            x, y, radius = np.around(circle, decimals=1)[0]
            if radius > 10:
                color = (255,0,255)
                cv2.circle(frame, (x, y), radius, color, 2)

    # contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	# 	cv2.CHAIN_APPROX_SIMPLE)
    # contours = imutils.grab_contours(contours)
    #
    # if len(contours) > 0:
    #     c = max(contours, key=cv2.contourArea)
    #     contours_poly = cv2.approxPolyDP(c, 3, True)
    #     centers, radius = cv2.minEnclosingCircle(contours_poly)
    #     if radius > 10:
    #         color = (255,0,255)
    #         cv2.circle(frame, (int(centers[0]), int(centers[1])), int(radius), color, 2)


    # print(frame.shape)
    frame = cv2.vconcat([frame, res])
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
cap.release()