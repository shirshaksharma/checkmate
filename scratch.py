import numpy as np
import cv2
import glob
import time

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

images = cv2.VideoCapture(0)
ttime = 0
retever = False
while True:
    sta, img = images.read()
    img2 = img
    if (ttime % 5 == 0):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            retever = True
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            corner1 = (corners[0][0][0] - abs(corners[0][0][0] - corners[1][0][0]),
                       corners[0][0][1] - abs(corners[0][0][1] - corners[7][0][1]))
            corner2 = (corners[6][0][0] + abs(corners[6][0][0] - corners[5][0][0]),
                       corners[6][0][1] - abs(corners[6][0][1] - corners[13][0][1]))
            corner3 = (corners[42][0][0] - abs(corners[42][0][0] - corners[43][0][0]),
                       corners[42][0][1] + abs(corners[42][0][1] - corners[35][0][1]))
            corner4 = (corners[48][0][0] + abs(corners[48][0][0] - corners[47][0][0]),
                       corners[48][0][1] + abs(corners[48][0][1] - corners[41][0][1]))

    if retever:
        img2 = cv2.line(img2, corner1, corner2, (255, 0, 0), 5)
        img2 = cv2.line(img2, corner1, corner3, (255, 0, 0), 5)
        img2 = cv2.line(img2, corner4, corner2, (255, 0, 0), 5)
        img2 = cv2.line(img2, corner4, corner3, (255, 0, 0), 5)

        img2 = cv2.line(img2, (corners2[0][0][0], corners2[0][0][1]),
                        (corners2[6][0][0], corners2[6][0][1]), (0, 255, 0), 5)
        img2 = cv2.line(img2, (corners2[6][0][0], corners2[6][0][1]),
                        (corners2[48][0][0], corners2[48][0][1]), (0, 255, 0), 5)
        img2 = cv2.line(img2, (corners2[48][0][0], corners2[48][0][1]),
                        (corners2[42][0][0], corners2[42][0][1]), (0, 255, 0), 5)
        img2 = cv2.line(img2, (corners2[0][0][0], corners2[0][0][1]),
                        (corners2[42][0][0], corners2[42][0][1]), (0, 255, 0), 5)

    cv2.imshow('img', img2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
images.release()
