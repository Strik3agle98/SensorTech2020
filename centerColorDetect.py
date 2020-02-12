import cv2
import numpy as np

cap = cv2.VideoCapture(0)
L = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]])
acc = 0
while(1):
    _, frame = cap.read()
    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    #swap between frame and HSV for different color space
    L[acc] = frame[240][320]
    res = np.mean(L, axis=0)
    res2 = [res[0]/res[1], res[1]/res[1], res[2]/res[1]]
    print(res)
    print(res2)
    cv2.circle(frame, (320, 240), 2, (255, 255, 255), 2)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
    if acc == 9:
        acc = 0
    else:
        acc += 1

cv2.destroyAllWindows()
cap.release()