import numpy as np
import cv2
import glob
import time
from board import get_board, which_square, get_corners

board = {}
filled = ["", 0]

def click(event, x, y, flags, param):
    global filled
    global board
    if board != {}:
        current = which_square(board, (x, y))
        last = filled[0]
        filled[0] = current
        if current != "" and filled[1] < 15 and last == current:
            filled[1] += 1
        if last != current:
            filled[1] = 0


images = cv2.VideoCapture(0)
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
        for key, square in board.items():
            pts = np.array([square['TL'], square['TR'],
                            square['BR'], square['BL']], np.int)
            pts = pts.reshape(-1, 1, 2)
            if(key == filled[0] and filled[1] == 15):
                img2 = cv2.fillPoly(
                    img2, [pts], square['color'])
            else:
                img2 = cv2.polylines(img2, [pts], 1, square['color'], 4)
        img2 = cv2.circle(img2, (600, 350), 10, (255, 255, 0))

    cv2.imshow("board roi", board_roi)
    cv2.imshow('img', img2)

cv2.destroyAllWindows()
images.release()
