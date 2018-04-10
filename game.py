import numpy as np
import cv2
import glob
import time
from chessgame import chessGame
from board import get_board, which_square, get_corners
from handdetect import find_largest_contour, find_convex_hull, HSV_MAX, HSV_MIN

board = {}
filled = ["", 0]
farthest_point = (0, 0)
allFarPoints = []
filledArray = []

siq = ""

chess = chessGame()


def fingerclick(points, offset):
    pointDict = {}
    for point in points:
        real_point = [(point[0] + offset[0]), (point[1] + offset[1])]
        square = which_square(board, real_point)
        if square:
            if square in pointDict:
                pointDict[square] += 1
            else:
                pointDict[square] = 1

    maxi = [0, ""]
    for key, value in pointDict.items():
        if value > maxi[0]:
            maxi[0] = value
            maxi[1] = key

    if maxi[0] != 0:
        click("", "", "", "", "", directSquare=maxi[1])


def click(event, x, y, flags, param, directSquare=None):
    global filled
    global filledArray
    global board
    global chess
    global siq
    if board != {}:
        if directSquare:
            current = directSquare
        else:
            current = which_square(board, (x, y))
        last = filled[0]
        filled[0] = current
        if current != "" and filled[1] < 15 and last == current:
            filled[1] += 1
            if (filled[1] >= 15):
                if (current in filledArray):
                    chess.move(siq, current)
                    filledArray = []
                    siq = ""
                else:
                    filledArray = chess.get(current)
                    siq = current
        if last != current:
            filled[1] = 0


cam = input("Enter 1 for external webcam and 0 for internal webcam")
images = cv2.VideoCapture(int(cam))
cv2.namedWindow("img")
cv2.setMouseCallback("img", click)
retever = False

# Initialize the ROI
_, frame = images.read()
board_roi = frame[0:1, 0:1]

while True:
    key = cv2.waitKey(1) & 0xFF
    sta, img = images.read()
    img2 = img
    # Scans the curent image for a board
    if key == ord('s'):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        board, retever = get_board(gray)

        # Get the board ROI
        if board:
            corners_board = get_corners(board, img2)
            board_roi = corners_board[0]

    # Exits the game
    if key == ord('q'):
        break
    if chess.isOver():
        break

    # DRAW PHASE
    if retever:
        # Get the board ROI
        corners_board = get_corners(board, img2)
        board_roi = corners_board[0]

        for key, square in board.items():
            pts = np.array([square['TL'], square['TR'],
                            square['BR'], square['BL']], np.int)
            pts = pts.reshape(-1, 1, 2)
            if key == filled[0] and filled[1] == 15:
                img2 = cv2.fillPoly(
                    img2, [pts], (0, 0, 255))
            elif(key in filledArray):
                img2 = cv2.fillPoly(
                    img2, [pts], (255, 0, 0))
            else:
                img2 = cv2.polylines(img2, [pts], 1, (0, 0, 0), 4)

    # Find the hand and fingertips
    largest_contour = find_largest_contour(board_roi, HSV_MIN, HSV_MAX)[2]
    blur_dilation = find_largest_contour(board_roi, HSV_MIN, HSV_MAX)[1]
    convex_hall = find_convex_hull(board_roi, largest_contour)

    height_small, width_small = board_roi.shape[:2]

    if convex_hall is not 0:
        farthest_point = convex_hall[2]
        allFarPoints = convex_hall[3]
        fingerclick(allFarPoints, corners_board[1])

    cv2.imshow("blur dilation", blur_dilation)
    cv2.imshow("board_roi", board_roi)
    cv2.imshow('img', img2)
    # cv2.imwrite('./img2.png', img2)

cv2.destroyAllWindows()
images.release()
