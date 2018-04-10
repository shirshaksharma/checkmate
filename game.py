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
filledArray = []
siq = ""

chess = chessGame()


def click(event, x, y, flags, param):
    global filled
    global filledArray
    global board
    global chess
    global siq
    if board != {}:
        current = which_square(board, (x, y))
        last = filled[0]
        filled[0] = current
        if current != "" and filled[1] < 15 and last == current:
            filled[1] += 1
            if (filled[1] >= 15):
                print(current)
                if (current in filledArray):
                    print(siq, current)
                    chess.move(siq, current)
                    filledArray = []
                    siq = ""
                else:
                    filledArray = chess.get(current)
                    siq = current
        if last != current:
            filled[1] = 0


images = cv2.VideoCapture(1)
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
                    img2, [pts], square['color'])
            elif key in filledArray:
                img2 = cv2.fillPoly(
                    img2, [pts], (255, 0, 0))
            else:
                img2 = cv2.polylines(img2, [pts], 1, square['color'], 4)
        img2 = cv2.circle(img2, (600, 350), 10, (255, 255, 0))

    # Find the hand and fingertips
    largest_contour = find_largest_contour(board_roi, HSV_MIN, HSV_MAX)[2]
    blur_dilation = find_largest_contour(board_roi, HSV_MIN, HSV_MAX)[1]
    convex_hall = find_convex_hull(board_roi, largest_contour)

    if convex_hall is not 0:
        farthest_point = convex_hall[2]

    cv2.imshow("blur dilation", blur_dilation)

    cv2.imshow('img', img2)
    cv2.imwrite('./img2.png', img2)

cv2.destroyAllWindows()
images.release()
