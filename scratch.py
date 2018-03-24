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


def construct_board(toprow, leftcol, rightcol, botrow, corners):
    board = {}
    leters = ['B', 'C', 'D', 'E', 'F', 'G']
    # First Row
    board['A1'] = {
        'TL': toprow[0],
        'TR': toprow[1],
        'BL': leftcol[0],
        'BR': (corners[0][0][0], corners[0][0][1])
    }
    for i in range(1, 7):
        board['A'+str(i+1)] = {
            'TL': toprow[i],
            'TR': toprow[i+1],
            'BL': (corners[i-1][0][0], corners[i-1][0][1]),
            'BR': (corners[i][0][0], corners[i][0][1])
        }
    board['A8'] = {
        'TL': toprow[7],
        'TR': toprow[8],
        'BL': (corners[6][0][0], corners[6][0][1]),
        'BR': rightcol[0]
    }
    # Middle Rows
    for i in range(0, 6):
        leter = leters[i]
        board[(leter + '1')] = {
            'TL': leftcol[i],
            'TR': (corners[i*7][0][0], corners[(i*7)][0][1]),
            'BL': leftcol[i+1],
            'BR': (corners[(i+1)*7][0][0], corners[(i+1)*7][0][1])
        }
        for j in range(2, 8):
            board[(leter + str(j))] = {
                'TL': (corners[(i*7) + (j-2)][0][0], corners[(i*7) + (j-2)][0][1]),
                'BL': (corners[((i+1)*7) + (j-2)][0][0], corners[((i+1)*7) + (j-2)][0][1]),
                'TR': (corners[(i*7) + (j-1)][0][0], corners[(i*7) + (j-1)][0][1]),
                'BR': (corners[((i+1)*7) + (j-1)][0][0], corners[((i+1)*7) + (j-1)][0][1])
            }
        board[(leter + '8')] = {
            'TL': (corners[i*7 + 6][0][0], corners[i*7 + 6][0][1]),
            'TR': rightcol[i],
            'BL': (corners[(i + 1)*7 + 6][0][0], corners[(i + 1)*7 + 6][0][1]),
            'BR': rightcol[i+1]
        }
    # Bottom Row
    board['H1'] = {
        'TL': leftcol[6],
        'TR': (corners[42][0][0], corners[42][0][1]),
        'BL': leftcol[7],
        'BR': botrow[0]
    }
    for i in range(0, 6):
        board['H'+str(i+2)] = {
            'TL': (corners[42 + i][0][0], corners[42 + i][0][1]),
            'TR': (corners[42 + i + 1][0][0], corners[42 + i + 1][0][1]),
            'BL': botrow[i],
            'BR': botrow[i+1]
        }
    board['H8'] = {
        'TL': (corners[48][0][0], corners[48][0][1]),
        'TR': rightcol[6],
        'BL': botrow[6],
        'BR': rightcol[7]
    }
    return board


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
toprow = []
leftcol = []
rightcol = []
botrow = []
board = {}
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
            toprow = []
            leftcol = []
            rightcol = []
            botrow = []
            # top row
            for i in range(0, 6):
                toprow.append(get_points_around(corners, i, i+1, i+7))
            for i in range(4, 7):
                toprow.append(get_points_around(corners, i, i-1, i+7))
            # left col
            for i in range(1, 6):
                leftcol.append(get_points_around(
                    corners, 0 + i*7, 1 + i*7, 7 + i*7))
            for i in range(4, 7):
                leftcol.append(get_points_around(
                    corners, 0 + i*7, 1 + i*7, i*7 - 7))
            # right col
            for i in range(1, 6):
                rightcol.append(get_points_around(
                    corners, 6 + i*7, 5 + i*7, 13 + i*7))
            for i in range(5, 8):
                rightcol.append(get_points_around(
                    corners, i*7 - 1, i*7 - 2, i*7 - 8))
            # bot row
            for i in range(43, 47):
                botrow.append(get_points_around(corners, i, i+1, i-7))
            for i in range(45, 48):
                botrow.append(get_points_around(corners, i, i-1, i-7))

            board = construct_board(toprow, leftcol, rightcol, botrow, corners)

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
        # for point in toprow:
        #     img2 = cv2.circle(img2, point, 10, (0, 0, 255))
        # for point in leftcol:
        #     img2 = cv2.circle(img2, point, 10, (0, 255, 0))
        # for point in rightcol:
        #     img2 = cv2.circle(img2, point, 10, (255, 255, 0))
        # for point in botrow:
        #     img2 = cv2.circle(img2, point, 10, (255, 0, 0))
        # for point in corners:
        #     img2 = cv2.circle(
        #         img2, (point[0][0], point[0][1]), 10, (255, 255, 255))
        # img2 = cv2.line(img2, lt, rt, (255, 0, 0), 5)
        # img2 = cv2.line(img2, lt, lb, (0, 255, 255), 5)
        # img2 = cv2.line(img2, rb, rt, (0, 255, 0), 5)
        # img2 = cv2.line(img2, lb, rb, (255, 255, 0), 5)

        for key, square in board.items():
            img2 = cv2.line(img2, square['TL'], square['TR'], (255, 0, 0), 5)
            img2 = cv2.line(img2, square['TL'], square['BL'], (255, 0, 0), 5)
            img2 = cv2.line(img2, square['TR'], square['BR'], (255, 0, 0), 5)
            img2 = cv2.line(img2, square['BL'], square['BR'], (255, 0, 0), 5)

    cv2.imshow('img', img2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
images.release()
