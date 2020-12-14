import numpy as np

class Board():
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.board = np.zeros((self.h, self.w), dtype=np.int)

    def __repr__(self):
        string = ''
        for y in range(self.h):
            for x in range(self.w):
                string += '%d ' % self.board[y][x]
            string += '\n'
        return string

class Gomoku():
    def __init__(self, board):
        self.board = board
        self.current_player = 1
        self.won_player = 0

    def reset(self):
        self.board.board = 0
        self.current_player = 1
        self.won_player = 0

    def put(self, x=None, y=None):
        if x is None and y is None:
            while True:
                rand_x = np.random.randint(0, self.board.w)
                rand_y = np.random.randint(0, self.board.h)

                if self.board.board[rand_y][rand_x] == 0:
                    self.board.board[rand_y][rand_x] = self.current_player
                    break
        else:
            self.board.board[y][x] = self.current_player

    def next(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
    
    def check_won(self):
        player = self.current_player

        for y in range(self.board.h):
            for x in range(self.board.w):
                try:
                    if self.board.board[y][x] == player and self.board.board[y+1][x] == player and self.board.board[y+2][x] == player and self.board.board[y+3][x] == player and self.board.board[y+4][x] == player:
                        self.won_player = player
                        break
                except:
                    pass

                try:
                    if self.board.board[y][x] == player and self.board.board[y][x+1] == player and self.board.board[y][x+2] == player and self.board.board[y][x+3] == player and self.board.board[y][x+4] == player:
                        self.won_player = player
                        break
                except:
                    pass

                try:
                    if self.board.board[y][x] == player and self.board.board[y+1][x+1] == player and self.board.board[y+2][x+2] == player and self.board.board[y+3][x+3] == player and self.board.board[y+4][x+4] == player:
                        self.won_player = player
                        break
                except:
                    pass

                try:
                    if x >= 4 and self.board.board[y][x] == player and self.board.board[y+1][x-1] == player and self.board.board[y+2][x-2] == player and self.board.board[y+3][x-3] == player and self.board.board[y+4][x-4] == player:
                        self.won_player = player
                        break
                except:
                    pass

            if self.won_player > 0:
                break
        
        return self.won_player


if __name__ == '__main__':
    board = Board(w=10, h=10)
    game = Gomoku(board=board)

    for i in range(100):
        game.next()
        won_player = game.check_won()

        if won_player > 0:
            print('Won %d' % won_player)
            print(board)
            break

