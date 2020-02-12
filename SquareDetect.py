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

while(1):
    _, frame = cap.read()
    print(frame.shape)
    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    drawing = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)

    for i, e in enumerate(colors):
        lower, upper = e[0:2]
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        if i == 7 or i == 9:
            lower, upper = colors[i+1][0:2]
            mask2 = cv2.inRange(hsv, lower, upper)
            mask2 = cv2.erode(mask2, None, iterations=2)
            mask = mask | mask2
            # cv2.imshow('mask', mask)

        res = cv2.bitwise_and(frame,frame, mask= mask)
        # res = cv2.cvtColor(res, cv2.COLOR_HS)


        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 50 and cv2.contourArea(c) < 6000:
                contours_poly = cv2.approxPolyDP(c, 3, True)
                if len(contours_poly) == 4:
                    rect = cv2.boundingRect(contours_poly)
                    cv2.rectangle(drawing, (int(rect[0]), int(rect[1])), \
                                  (int(rect[0] + rect[2]), int(rect[1] + rect[3])), (int(e[2][0]), int(e[2][1]), int(e[2][2])), -1)
                    cv2.rectangle(hsv, (int(rect[0]), int(rect[1])), \
                                  (int(rect[0] + rect[2]), int(rect[1] + rect[3])),
                                  (int(e[2][0]), int(e[2][1]), int(e[2][2])), -1)

    drawing = cv2.cvtColor(drawing, cv2.COLOR_HSV2BGR)
    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    framee = cv2.vconcat([frame, drawing])
    cv2.imshow('frame',framee)
    if cv2.waitKey(1) & 0xFF == 32:
        print('space!!')
        cv2.imwrite('frame'+str(acc)+'.jpg', frame)
        cv2.imwrite('draw'+str(acc)+'.jpg', drawing)
        acc += 1

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
cap.release()