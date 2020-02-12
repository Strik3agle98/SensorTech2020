import cv2
import numpy as np
import imutils
import os

acc = 11


cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == 32:
        print('space!!')
        cv2.imwrite(str(acc)+'_cam.jpg', frame)
        acc += 1
        print('image saved: '+str(acc)+'.jpg')

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
cap.release()