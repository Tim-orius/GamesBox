import numpy as np

class SudokuSolver:
    def __init__(self):
        """Initialize the SudokuSolver with an empty board."""
        self.board = None
        self.solved_board = None

    def set_board(self, board):
        """
        Set the board for solving.

        :param board: 2D array representing the Sudoku board
        """
        self.board = board

    def print_board(self):
        """Print the Sudoku board in a readable format."""
        for row in self.board:
            print(" ".join(str(num) for num in row))

    def is_valid(self, row, col, digit):
        """
        Check if a given digit can be placed at the board's (row, col) position.

        :param row: Row index
        :param col: Column index
        :param digit: Number to be placed
        :return: True if valid placement, False otherwise
        """
        # Check the row and column
        if digit in self.board[row] or digit in [self.board[i][col] for i in range(9)]:
            return False

        # Check the 3x3 grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == digit:
                    return False

        return True

    def solve_sudoku(self):
        """Solve the Sudoku puzzle using backtracking."""
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            self.solved_board = [row[:] for row in self.board]  # Store the solved board
            return True  # Puzzle is solved
        row, col = empty_cell

        for digit in range(1, 10):
            if self.is_valid(row, col, digit):
                self.board[row][col] = digit  # Place digit
                if self.solve_sudoku():
                    return True  # Puzzle solved
                self.board[row][col] = 0  # Reset and backtrack

        return False  # Trigger backtracking

    def count_solutions(self):
        """Count the number of possible solutions for the Sudoku puzzle."""
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return 1  # Found one valid solution

        row, col = empty_cell
        solution_count = 0

        for digit in range(1, 10):
            if self.is_valid(row, col, digit):
                self.board[row][col] = digit  # Place digit
                solution_count += self.count_solutions()
                self.board[row][col] = 0  # Reset

        return solution_count

    def find_empty_cell(self):
        """Find the next empty cell in the Sudoku board (represented by 0)."""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return None

    def compare_solution(self, solution):
        """
        Compare the computed solution stored in solved_board
        with the provided solution.

        :param solution: 2D array representing a solution to check against
        :return: True if solutions are equal, False otherwise
        """
        if self.solved_board is None:
            return False  # No solution computed yet

        return np.array_equal(self.solved_board, solution)

    def validate_board(self):
        """Validate the initial board to check if it's a valid Sudoku setup."""
        if self.board is None or len(self.board) != 9 or any(len(row) != 9 for row in self.board):
            raise ValueError("Board must be a 9x9 grid.")
        # Further validation can be added to check for duplicates in rows, columns and boxes.