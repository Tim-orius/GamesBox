import random

import numpy as np

class BoardShuffler:

    board = np.array([
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 1, 5, 6, 4, 8, 9, 7],
        [5, 6, 4, 8, 9, 7, 2, 3, 1],
        [8, 9, 7, 2, 3, 1, 5, 6, 4],
        [3, 1, 2, 6, 4, 5, 9, 7, 8],
        [6, 4, 5, 9, 7, 8, 3, 1, 2],
        [9, 7, 8, 3, 1, 2, 6, 4, 5]
    ])

    def __init__(self):
        """ """

    def cycle_index(self, idx, max_cycle=9):
        return idx % max_cycle

    def shuffle(self):
        self.shuffle_numbers()
        self.shuffle_rows()
        self.shuffle_cols()
        self.shuffle_row_block()
        self.shuffle_col_block()

    def shuffle_numbers(self):
        for ii in range(1, 10):
            random_number = random.randint(1, 9)
            self.swap_numbers(ii, random_number)

    def swap_numbers(self, n1, n2):
        """ """
        for yy in range(9):
            for xx in range(9):
                if self.board[xx][yy] == n1:
                    self.board[xx][yy] = n2
                elif self.board[xx][yy] == n2:
                    self.board[xx][yy] = n1

    def shuffle_rows(self):
        """ """
        for ii in range(9):
            random_number = random.randint(0, 2)
            block_number = ii // 3
            self.swap_rows(ii, block_number * 3 + random_number)

    def swap_rows(self, row1, row2):
        """ """
        row = np.copy(self.board[row1])
        self.board[row1] = self.board[row2]
        self.board[row2] = row

    def shuffle_cols(self):
        """ """

        for ii in range(9):
            random_number = random.randint(0, 2)
            block_number = ii // 3
            self.swap_cols(ii, block_number * 3 + random_number)

    def swap_cols(self, col1, col2):
        """ """
        column = np.copy(self.board[:, col1])
        self.board[:, col1] = self.board[:, col2]
        self.board[:, col2] = column

    def shuffle_row_block(self):
        for ii in range(3):
            random_number = random.randint(0, 2)
            self.swap_row_blocks(ii, random_number)

    def swap_row_blocks(self, row_block1, row_block2):
        for ii in range(3):
            self.swap_rows(row_block1 * 3 + ii, row_block2 * 3 + ii)

    def shuffle_col_block(self):
        for ii in range(3):
            random_number = random.randint(0, 2)
            self.swap_col_blocks(ii, random_number)

    def swap_col_blocks(self, col_block1, col_block2):
        for ii in range(3):
            self.swap_rows(col_block1 * 3 + ii, col_block2 * 3 + ii)