import chess
import chess.svg
import os


class chessGame():
    # Global variable declaration
    global board
    global squares
    global path

    # Class Setup
    def __init__(self):
        global board
        global squares
        global path
        global moves

        path = os.path.dirname(os.path.abspath(__file__))
        board = chess.Board()
        moves = 0
        squares = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1',
                   'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'c1', 'c2',
                   'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'd1', 'd2', 'd3',
                   'd4', 'd5', 'd6', 'd7', 'd8', 'e1', 'e2', 'e3', 'e4',
                   'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'f3', 'f4', 'f5',
                   'f6', 'f7', 'f8', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6',
                   'g7', 'g8', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7',
                   'h8']
        self.show()

    # Writes the current board to board.svg

    def show(self):
        img = chess.svg.board(board=board)
        with open(path + "/board.svg", 'w') as file:
            for line in img:
                file.write(line)

    # Calls the native python-chess is_game_over function to end the game

    def isOver(self):
        return board.is_game_over()

    # Converts the syntax that the board is stored in, into uci syntax that can be used by
    # python-chess, re-writes the board

    def move(self, start, end):
        global moves
        mov = chess.Move.from_uci(start.lower() + end.lower())
        board.push(mov)
        moves += 1
        self.show()

    # Undoes any move

    def undo(self):
        global moves
        if moves > 0:
            board.pop()
            self.show()
            moves -= 1
            return True
        return False

    # Gets all possible moves for a given square by itterating over all squares
    # and seeing if that move is valid

    def get(self, sqaure):
        global squares
        posMoves = []
        for possquare in squares:
            if (chess.Move.from_uci(sqaure.lower() + possquare)) in board.legal_moves:
                posMoves.append(possquare.upper())
        return posMoves
