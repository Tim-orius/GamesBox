import numpy as np

from shuffler import BoardShuffler
from masker import MaskCreator
from solver import SudokuSolver


class SudokuCreator:

    masker = None
    shuffler = None

    def __init__(self, solver, start_entries=20):
        """ """

        self.masker = MaskCreator()
        self.shuffler = BoardShuffler()
        self.solver = solver
        self.start_entries = start_entries

    def generate(self):
        self.shuffler.shuffle()
        self.masker.generate_start_mask(start_entries=self.start_entries)

        solution_board = self.shuffler.board

        sudoku_board = np.zeros_like(solution_board)
        sudoku_board[self.masker.mask == 1] = solution_board[self.masker.mask == 1]

        unique = False
        while not unique:
            self.solver.set_board(sudoku_board)
            solution_count = self.solver.count_solutions()
            if solution_count > 1:
                self.masker.add_mask_entry()
                sudoku_board[self.masker.mask == 1] = solution_board[self.masker.mask == 1]
            else:
                unique = True

        return sudoku_board


def main():
    # start entries ( max. 81)
    start_entries = 70
    sudoku_solver = SudokuSolver()
    creator = SudokuCreator(solver=sudoku_solver, start_entries=start_entries)
    sudoku = creator.generate()

    print(sudoku)
    print("")
    print("x-x-x-x-x-x-x")
    print("")
    print("Solution:")
    print(creator.shuffler.board)
    print(sudoku_solver.solved_board)

    print(sudoku_solver.compare_solution(creator.shuffler.board))

if __name__ == "__main__":
    main()
