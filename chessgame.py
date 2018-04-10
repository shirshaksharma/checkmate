import chess
import chess.svg
from IPython.display import SVG, display


class chessGame():
    global board
    global squares

    def __init__(self):
        global board
        board = chess.Board()
        global squares
        squares = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1',
                   'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'c1', 'c2',
                   'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'd1', 'd2', 'd3',
                   'd4', 'd5', 'd6', 'd7', 'd8', 'e1', 'e2', 'e3', 'e4',
                   'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'f3', 'f4', 'f5',
                   'f6', 'f7', 'f8', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6',
                   'g7', 'g8', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7',
                   'h8']
        self.show()

    def show(self):
        img = chess.svg.board(board=board)
        with open("board.svg", 'w') as file:
            for line in img:
                file.write(line)

    def isOver(self):
        return board.is_game_over()

    def move(self, start, end):
        mov = chess.Move.from_uci(start.lower() + end.lower())
        board.push(mov)
        self.show()

    def get(self, sqaure):
        global squares
        posMoves = []
        for possquare in squares:
            if (chess.Move.from_uci(sqaure.lower() + possquare)) in board.legal_moves:
                posMoves.append(possquare.upper())
        return posMoves
