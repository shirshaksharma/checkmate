import numpy as np
import cv2
import glob
import time
from board import get_board, which_square
from chessgame import chessGame

board = {}
filled = ["", 0]
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


while True:
    key = cv2.waitKey(1) & 0xFF
    sta, img = images.read()
    img2 = img
    # Scans the curent image for a board
    if key == ord('s'):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        board, retever = get_board(gray)
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
            elif(key in filledArray):
                img2 = cv2.fillPoly(
                    img2, [pts], (255, 0, 0))
            else:
                img2 = cv2.polylines(img2, [pts], 1, square['color'], 4)
        img2 = cv2.circle(img2, (600, 350), 10, (255, 255, 0))

    cv2.imshow('img', img2)
    cv2.imwrite('./img2.png', img2)

cv2.destroyAllWindows()
images.release()
