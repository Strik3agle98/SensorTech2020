import numpy as np
import cv2 as cv
# import glob
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((9*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:9].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
# images = glob.glob('*.jpg')
def loadImage():
    images = []
    for i in range(24):
        images.append(str(i)+'_cam.jpg')
    return images

def calibrateCamera(images):
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (7,9), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            # cv.drawChessboardCorners(img, (7,9), corners2, ret)
            # cv.imshow('img', img)
            # cv.waitKey(0) & 0xFF == 27
    # cv.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print('mtx: '+str(mtx) + '\ndist: '+str(dist))
    return mtx, dist, rvecs, tvecs

def testDistortion(mtx, dist):
    img = cv.imread('0_cam.jpg')
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    cap = cv.VideoCapture(0)
    while True:
        _, frame = cap.read()
        dst = cv.undistort(frame, mtx, dist, None, newcameramtx)
        # crop the image
        x, y, w, h = roi
        # dst = dst[y:y + h, x:x + w]

        mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
        rmp = cv.remap(frame , mapx, mapy, cv.INTER_LINEAR)
        # crop the image
        x, y, w, h = roi
        # rmp = rmp[y:y + h, x:x + w]

        print(frame.shape)
        print(dst.shape)
        # frame = cv.vconcat([frame, dst])
        cv.imshow('frame', frame)
        cv.imshow('dst', dst)
        cv.imshow('rmp', rmp)

        if cv.waitKey(1) & 0xFF == 27:
            break

    cv.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    mtx, dist, rvecs, tvecs = calibrateCamera(loadImage())
    testDistortion(mtx, dist)
