import numpy as np
import cv2
import glob
import time


def which_square(board, point):
    for key, square in board.items():
        if((abs(square['TL'][0] - point[0]) + abs(square['BR'][0] - point[0]))
                == abs(square['TL'][0] - square['BR'][0])):
            if((abs(square['TL'][1] - point[1]) + abs(square['BR'][1] - point[1]))
                    == abs(square['TL'][1] - square['BR'][1])):
                return key
    return ""


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


def orient_board(board):
    while (board['A1']['TL'][0] > board['H8']['BR'][0]
           or board['A1']['TL'][1] < board['H8']['BR'][1]):
        # rotate board
        board = rotate_board(board)
    return board


def rotate_board(board):
    newboard = {}
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
    for key, square in board.items():
        letteri = letters.index(key[0])
        numberi = numbers.index(key[1])
        # letters[7-numberi]+numbers[letteri]
        newstring = letters[7-numberi]+numbers[letteri]
        if newstring[0] == 'A':
            color = (0, 0, 255)
        elif newstring[0] == 'H':
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)
        newboard[newstring] = {
            'TL': square['TL'],
            'TR': square['TR'],
            'BL': square['BL'],
            'BR': square['BR'],
            'color': color,
            'filled': False
        }
    return newboard


def construct_board(toprow, leftcol, rightcol, botrow, corners):
    board = {}
    leters = ['B', 'C', 'D', 'E', 'F', 'G']
    # First Row
    board['A1'] = {
        'TL': toprow[0],
        'TR': toprow[1],
        'BL': leftcol[0],
        'BR': (corners[0][0][0], corners[0][0][1]),
        'color': (0, 0, 255),
        'filled': False
    }
    for i in range(1, 7):
        board['A'+str(i+1)] = {
            'TL': toprow[i],
            'TR': toprow[i+1],
            'BL': (corners[i-1][0][0], corners[i-1][0][1]),
            'BR': (corners[i][0][0], corners[i][0][1]),
            'color': (0, 0, 255),
            'filled': False
        }
    board['A8'] = {
        'TL': toprow[7],
        'TR': toprow[8],
        'BL': (corners[6][0][0], corners[6][0][1]),
        'BR': rightcol[0],
        'color': (0, 0, 255),
        'filled': False
    }
    # Middle Rows
    for i in range(0, 6):
        leter = leters[i]
        board[(leter + '1')] = {
            'TL': leftcol[i],
            'TR': (corners[i*7][0][0], corners[(i*7)][0][1]),
            'BL': leftcol[i+1],
            'BR': (corners[(i+1)*7][0][0], corners[(i+1)*7][0][1]),
            'color': (0, 255, 0),
            'filled': False
        }
        for j in range(2, 8):
            board[(leter + str(j))] = {
                'TL': (corners[(i*7) + (j-2)][0][0], corners[(i*7) + (j-2)][0][1]),
                'BL': (corners[((i+1)*7) + (j-2)][0][0], corners[((i+1)*7) + (j-2)][0][1]),
                'TR': (corners[(i*7) + (j-1)][0][0], corners[(i*7) + (j-1)][0][1]),
                'BR': (corners[((i+1)*7) + (j-1)][0][0], corners[((i+1)*7) + (j-1)][0][1]),
                'color': (0, 255, 0),
                'filled': False
            }
        board[(leter + '8')] = {
            'TL': (corners[i*7 + 6][0][0], corners[i*7 + 6][0][1]),
            'TR': rightcol[i],
            'BL': (corners[(i + 1)*7 + 6][0][0], corners[(i + 1)*7 + 6][0][1]),
            'BR': rightcol[i+1],
            'color': (0, 255, 0),
            'filled': False
        }
    # Bottom Row
    board['H1'] = {
        'TL': leftcol[6],
        'TR': (corners[42][0][0], corners[42][0][1]),
        'BL': leftcol[7],
        'BR': botrow[0],
        'color': (255, 0, 0),
        'filled': False
    }
    for i in range(0, 6):
        board['H'+str(i+2)] = {
            'TL': (corners[42 + i][0][0], corners[42 + i][0][1]),
            'TR': (corners[42 + i + 1][0][0], corners[42 + i + 1][0][1]),
            'BL': botrow[i],
            'BR': botrow[i+1],
            'color': (255, 0, 0),
            'filled': False

        }
    board['H8'] = {
        'TL': (corners[48][0][0], corners[48][0][1]),
        'TR': rightcol[6],
        'BL': botrow[6],
        'BR': rightcol[7],
        'color': (255, 0, 0),
        'filled': False

    }
    board = orient_board(board)
    return board


# Find the chess board corners


def get_board(gray):

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((7 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)
    toprow = []
    leftcol = []
    rightcol = []
    botrow = []
    ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

    # If found, add object points, image points (after refining them)
    if ret:
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
    else:
        return {}, False
    return board, True


def get_corners(board, img):

    corner_a1 = board['A1']['BL']
    corner_a8 = board['A8']['TL']
    corner_h1 = board['H1']['BR']
    corner_h8 = board['H8']['TR']

    corners = [
        corner_a1,
        corner_h8,
        corner_h1,
        corner_a8
    ]

    x_min = corner_a8
    x_max = corner_h8
    y_min = corner_a1
    y_max = corner_h1

    for i in range(len(corners)):
        if corners[i][0] <= x_min[0]:
            x_min = corners[i]
        if corners[i][0] > x_max[0]:
            x_max = corners[i]
        if corners[i][1] <= y_min[1]:
            y_min = corners[i]
        if corners[i][1] > y_max[1]:
            y_max = corners[i]

    height = abs(y_max[1] - y_min[1])
    width = abs(x_max[0] - x_min[0])

    roi_y_min = y_min[1]
    roi_y_max = y_min[1] + height

    roi_x_min = x_min[0]
    roi_x_max = x_min[0] + width

    # Making it a wider area
    differential = height / 8

    if roi_y_min - differential < 0:
        roi_y_min = 0
    else:
        roi_y_min = roi_y_min - differential

    roi_y_max = roi_y_max + differential

    if roi_x_min - differential < 0:
        roi_x_min = 0
    else:
        roi_x_min = roi_x_min - differential

    roi_x_max = roi_x_max + differential

    board_roi = img[
        int(roi_y_min):int(roi_y_max),
        int(roi_x_min):int(roi_x_max)
    ]

    # height = abs(corner_h8[1] - corner_a1[1])
    # width = abs(corner_h1[0] - corner_a8[0])
    #
    # start_point = corner_a8[0], corner_h8[1]
    # end_point = corner_h1[0], corner_a1[1]
    #
    # print("height range", corner_a8, corner_a1, height)
    # print("width range", corner_h1, corner_a8, width)


    print("roi range", int(corner_h8[1]), int(corner_a1[1]))
    print("roi range", int(corner_h8[0]), int(corner_a1[0]))

    # board_roi = img[
    #     int(corner_h8[1]):int(corner_a1[1]),
    #     int(corner_a1[0]):int(corner_h8[0]),
    # ]

    return board_roi, corner_a1, corner_a8, corner_h1, corner_h8
