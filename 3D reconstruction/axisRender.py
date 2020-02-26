import cameraCalibration as cc
import cv2 as cv
import numpy as np

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((9*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:9].T.reshape(-1,2)
axis = np.float32([[0,0,0], [0,8,0], [6,8,0], [6,0,0],
                   [0,0,-3],[0,8,-3],[6,8,-3],[6,0,-3] ])

def draw(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)
    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)
    return img

def renderBox(mtx, dist):
    cap = cv.VideoCapture(0)
    while True:
        _, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (7, 9), None)
        if ret == True:
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            # Find the rotation and translation vectors.
            ret, rvecs, tvecs = cv.solvePnP(objp, corners2, mtx, dist)
            # project 3D points to image plane
            imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)
            frame = draw(frame, corners2, imgpts)
        cv.imshow('res', frame)
        if cv.waitKey(1) & 0xFF == 27:
            break
    cv.destroyAllWindows()

if __name__ == '__main__':
    mtx, dist, rvecs, tvecs = cc.calibrateCamera(cc.loadImage())
    renderBox(mtx, dist)