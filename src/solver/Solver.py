from data import SudokuBoard


class Solver:


    def solve(self, board: SudokuBoard) -> bool:
        print("Solving Sudoku...")

        board.get_cell(8,8).value = 9
        return False

