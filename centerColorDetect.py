import cv2

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #swap between frame and HSV for different color space
    print(hsv[240][320])
    cv2.circle(frame, (320, 240), 2, (255, 255, 255), 2)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
cap.release()