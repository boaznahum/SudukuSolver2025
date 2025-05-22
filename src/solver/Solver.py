from data import SudokuBoard


class Solver:


    def solve(self, board: SudokuBoard) -> bool:
        print("Solving Sudoku...")

        board.get_cell(4,5).set_value(5)
        board.get_cell(5,5).set_notes(1, 3, 4, 5, 6, 7, 8, 9)
        return False

