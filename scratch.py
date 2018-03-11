import numpy as np
import cv2
import glob
import time


def get_points_around(corners, a, b, c):
    ax = (corners[a][0][0] - (corners[b][0][0] - corners[a][0][0]))
    ay = (corners[a][0][1] - (corners[b][0][1] - corners[a][0][1]))
    bx = (corners[a][0][0] - (corners[c][0][0] - corners[a][0][0]))
    by = (corners[a][0][1] - (corners[c][0][1] - corners[a][0][1]))

    cx = corners[a][0][0] - \
        (corners[a][0][0] - ax) - (corners[a][0][0] - bx)
    cy = corners[a][0][1] - \
        (corners[a][0][1] - ay) - (corners[a][0][1] - by)
    return (cx, cy)


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
    if cv2.waitKey(1) & 0xFF == ord('s'):
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

            lt = get_points_around(corners, 0, 1, 7)
            rt = get_points_around(corners, 6, 5, 13)
            lb = get_points_around(corners, 42, 43, 35)
            rb = get_points_around(corners, 48, 47, 41)

    if retever:

        # img2 = cv2.line(img2, (corners2[0][0][0], corners2[0][0][1]),
        #                 (corners2[6][0][0], corners2[6][0][1]), (0, 255, 0), 5)
        # img2 = cv2.line(img2, (corners2[6][0][0], corners2[6][0][1]),
        #                 (corners2[48][0][0], corners2[48][0][1]), (0, 255, 0), 5)
        # img2 = cv2.line(img2, (corners2[48][0][0], corners2[48][0][1]),
        #                 (corners2[42][0][0], corners2[42][0][1]), (0, 255, 0), 5)
        # img2 = cv2.line(img2, (corners2[0][0][0], corners2[0][0][1]),
        #                 (corners2[42][0][0], corners2[42][0][1]), (0, 255, 0), 5)

        # img2 = cv2.circle(img2, lt, 10, (0, 0, 255))
        # img2 = cv2.circle(img2, rt, 10, (0, 0, 255))
        # img2 = cv2.circle(img2, lb, 10, (0, 0, 255))
        # img2 = cv2.circle(img2, rb, 10, (0, 0, 255))

        img2 = cv2.line(img2, lt, rt, (255, 0, 0), 5)
        img2 = cv2.line(img2, lt, lb, (0, 255, 255), 5)
        img2 = cv2.line(img2, rb, rt, (0, 255, 0), 5)
        img2 = cv2.line(img2, lb, rb, (255, 255, 0), 5)

    cv2.imshow('img', img2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
images.release()
