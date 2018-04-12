import numpy as np
import cv2
import os
from chessgame import chessGame
from board import get_board, which_square, get_corners, rotate_board
from handdetect import find_largest_contour, find_convex_hull, HSV_MAX, HSV_MIN
import webbrowser

# Global variable declarations
board = {}
filled = ["", 0]
farthest_point = (0, 0)
allFarPoints = []
filledArray = []
SENSATIVITY = 5
flipped = False
player1turn = True
path = os.path.dirname(os.path.abspath(__file__))
# Square in Question
siq = ""
chess = chessGame()

# Gets the list of points and determins where most of them lies
# then calls the click function with a direct square


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

# Native mouse function remains for easy reimpimentation
# directSquare allows for easy interaction with the finger
# tracking code


def click(event, x, y, flags, param, directSquare=None):
    global filled
    global filledArray
    global board
    global chess
    global siq
    global player1turn
    if board != {}:
        if directSquare:
            current = directSquare
        else:
            current = which_square(board, (x, y))
        last = filled[0]
        filled[0] = current
        # If there is finger/Mouse is in a square and it has not been in that square
        # for more than the SENSATIVITY amount of frames, adds to the frame count
        # once the object has been in the square for SENSATIVITY frames, it either
        # gets all the posible moves for that square, or if the square is in the array
        # of filledArray then it calles the move by storing the SIQ of what the
        # possible moves are from. If a move is made, it flips which players turn it is
        if current != "" and filled[1] < SENSATIVITY and last == current:
            filled[1] += 1
            if (filled[1] >= SENSATIVITY):
                if (current in filledArray):
                    chess.move(siq, current)
                    player1turn = not player1turn
                    filledArray = []
                    siq = ""
                else:
                    filledArray = chess.get(current)
                    siq = current
        if last != current:
            filled[1] = 0


# If the player has a secondary camera installed, allows them to pick it
cam = input("Enter 1 for external webcam and 0 for internal webcam\n")
images = cv2.VideoCapture(int(cam))
retever = False

# Initialize the ROI
_, frame = images.read()
board_roi = frame[0:1, 0:1]

# Opens the game board html
webbrowser.open("file://" + path + '/game.html')

# Game Loop
while True:
    # Gets the Key Press
    keyp = cv2.waitKey(1) & 0xFF
    # Gets the current frame
    sta, img = images.read()
    img2 = img.copy()
    # Scans the curent image for a board
    if keyp == ord('s'):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        board, retever = get_board(gray)

        # Get the board ROI
        if board:
            corners_board = get_corners(board, img)
            board_roi = corners_board[0]
    # Rotates the board
    if keyp == ord('r'):
        board = rotate_board(board)
    # Flips the board
    if keyp == ord('f'):
        flipped = not flipped

    # Undoes last move
    if keyp == ord('u'):
        if(chess.undo()):
            player1turn = not player1turn

    # Exits the game
    if keyp == ord('q'):
        break
    if chess.isOver():
        break

    # DRAW PHASE (if the board was found)
    if retever:
        # Get the board ROI
        corners_board = get_corners(board, img)
        board_roi = corners_board[0]

        # Draws the board
        for key, square in board.items():
            pts = np.array([square['TL'], square['TR'],
                            square['BR'], square['BL']], np.int)
            pts = pts.reshape(-1, 1, 2)
            if key == filled[0] and filled[1] == SENSATIVITY:
                img2 = cv2.polylines(
                    img2, [pts], 1, (0, 0, 255), 10)
            elif(key in filledArray):
                img2 = cv2.polylines(
                    img2, [pts], 1, (0, 255, 0), 10)
            else:
                if('1' in key and not player1turn):
                    img2 = cv2.polylines(img2, [pts], 1, (0, 0, 0), 4)
                elif('8' in key and player1turn):
                    img2 = cv2.polylines(img2, [pts], 1, (0, 0, 0), 4)
                else:
                    img2 = cv2.polylines(img2, [pts], 1, square['color'], 4)

    # Find the hand and fingertips
    largest_contour = find_largest_contour(board_roi, HSV_MIN, HSV_MAX)[2]
    blur_dilation = find_largest_contour(board_roi, HSV_MIN, HSV_MAX)[1]
    convex_hall = find_convex_hull(board_roi, largest_contour)

    height_small, width_small = board_roi.shape[:2]

    if convex_hall is not 0:
        farthest_point = convex_hall[2]
        allFarPoints = convex_hall[3]
        fingerclick(allFarPoints, corners_board[1])
    # Flips before showing
    if (flipped):
        img2 = cv2.flip(img2, 1)

    # Prints the image
    if keyp == ord('p'):
        print('writing to ' + path + '/image2.png')
        cv2.imwrite(path + '/image2.png', img2)

    cv2.imshow('Check Mate', img2)


cv2.destroyAllWindows()
images.release()
