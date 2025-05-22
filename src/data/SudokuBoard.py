from data.Cell import Cell


class SudokuBoard:
    grid: list[list[Cell]]

    def __init__(self):
        self.grid = [[Cell() for _ in range(9)] for _ in range(9)]

    def get_cell(self, row: int, col: int) -> Cell:
        """
            Returns the cell at the given row and column.
            :param row:
            :param col:
            :return:
        """

        if 0 <= row < 9 and 0 <= col < 9:
            return self.grid[row][col]
        else:
            raise IndexError("Row or column index out of range.")

    def __str__(self):
        """
        Returns a string representation of the Sudoku board.
        :return:
        """
        board_str = ""
        for row in self.grid:
            for cell in row:
                if cell.value is None:
                    board_str += "? "
                else:
                    board_str += str(cell.value) + " "
            board_str += "\n"
        return board_str
