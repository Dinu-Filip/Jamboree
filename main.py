import math
import random
from itertools import product
from sys import stdout


def detriment_x(whites, blacks, N, R):
    total = 0
    for i in range(N):
        for k in range(R):
            total += abs(whites[i][k] - blacks[i][k])
    return total


def detriment_y(up_floats, down_floats, N):
    total = 0
    for i in range(N):
        up_total = sum(up_floats[i])
        down_total = sum(down_floats[i])
        total += abs(up_total - down_total)
    return total


def detriment_z(whites, B, R, N):
    total = 0
    factor = 4 / (R * B * (B + 1))
    for i in range(N):
        board_count = 0
        for l in range(B):
            board_count += l * whites[i][l]
        prod = factor * board_count
        total += abs(1 - prod)
    return total


class Board:
    def __init__(self, sz: int):
        self.m = [[0 for _ in range(sz)] for __ in range(sz)]
        self.whites = [0 for _ in range(sz)]
        self.blacks = [0 for _ in range(sz)]
        self.white_sum = 0
        self.black_sum = 0

    def get_whites(self, n: int) -> int:
        return self.whites[n]

    def get_blacks(self, n: int) -> int:
        return self.blacks[n]

    def increment_at(self, offset: int, w: int, b: int):
        self.m[w][b] += offset
        self.whites[w] += offset
        self.blacks[b] += offset
        self.white_sum += offset
        self.black_sum += offset


def generate_boards(b: int):
    board: Board = Board(b)

    def add_row(board, row_i):
        if row_i == b:
            good = True
            for i in range(b):
                if board.get_whites(i) + board.get_blacks(i) != 3:
                    good = False
                    break
            if board.white_sum != 9 or board.black_sum != 9:
                good = False
            if good:
                yield board
            return
        for black in range(b):
            if board.m[black][row_i] == 1:
                continue
            if board.get_whites(row_i) == 2 or board.get_blacks(black) == 2:
                continue
            board.increment_at(1, row_i, black)
            for black2 in range(b):
                if black2 == black:
                    continue
                if board.m[black2][row_i] == 1:
                    continue
                if board.get_blacks(black2) == 2:
                    continue
                board.increment_at(1, row_i, black2)
                for _board in add_row(board, row_i + 1):
                    yield _board
                board.increment_at(-1, row_i, black2)
            for _board in add_row(board, row_i + 1):
                yield _board
            board.increment_at(-1, row_i, black)

    for _board in add_row(board, 0):
        yield _board


for board in generate_boards(12):
    stdout.write(str(board.m) + "\n")
