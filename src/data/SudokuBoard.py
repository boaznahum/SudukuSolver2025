from data.Cell import Cell


class SudokuBoard:
    _grid: list[list[Cell]]

    def __init__(self):
        self._grid = [[Cell() for _ in range(9)] for _ in range(9)]

    def get_cell(self, row: int, col: int) -> Cell:
        """
            Returns the cell at the given row and column.
            :param row:
            :param col:
            :return:
        """

        if 0 <= row < 9 and 0 <= col < 9:
            return self._grid[row][col]
        else:
            raise IndexError("Row or column index out of range.")

    def set_cell_value(self, row: int, col: int, value: int | None):
        """
            Sets the value of the cell at the given row and column.
            This also clears the notes of the cell.
            throws if row or column index is out of range [0, 9)
            throws ValueError if the value is not between 1 and 9
            :param row:
            :param col:
            :param value:
            :return:
        """
        if 0 <= row < 9 and 0 <= col < 9:
            self._grid[row][col].set_value(value)
        else:
            raise IndexError("Row or column index out of range.")

    def get_cell_value(self, row: int, col: int) -> int | None:
        """
            Returns the value of the cell at the given row and column.
            throws if row or column index is out of range [0, 9)
            :param row:
            :param col:
            :return:
        """
        if 0 <= row < 9 and 0 <= col < 9:
            return self._grid[row][col].get_value()
        else:
            raise IndexError("Row or column index out of range.")

    def set_cell_note(self, row: int, col: int, note: int):
        """
            Sets the note of the cell at the given row and column.
            This clear the value of the cell.

            throws if row or column index is out of range [0, 9)
            throws ValueError if the note is not between 1 and 9

            :param row:
            :param col:
            :param note:
            :return:
        """
        if 0 <= row < 9 and 0 <= col < 9 and 1 <= note <= 9:

            self._grid[row][col].set_note(note)
        else:
            raise IndexError("Row or column index out of range or note out of range.")

    def set_cell_note_by_loc(self, cell_row: int, cell_col: int, note_row: int, note_col):
        """
            Sets the note of the cell at the given row and column.
            This clear the value of the cell.

            throws if row or column index is out of range [0, 9)
            throws ValueError if the note is not between 1 and 9

            :param cell_row:
            :param cell_col:
            :param note_row:
            :param note_col:
            :return:
        """
        if (0 > cell_row or cell_row >= 9) or (0 > cell_col or cell_col >= 9):

            raise IndexError("Cell Row or column index out of range  [0,9).")

        # check the same for note_row and note_col
        if (0 > note_row or note_row >= 3) or (0 > note_col or note_col >= 3):
            raise IndexError("Note Row or column index out of range or note out of range [0,3).")


        else:
            self._grid[cell_row][cell_col].set_note_by_loc(note_row, note_col)

    def get_cell_notes(self, row: int, col: int) -> list[int | None]:
        """
            Returns the notes of the cell at the given row and column.
            throws if row or column index is out of range [0, 9)
            :param row:
            :param col:
            :return:
        """
        if 0 <= row < 9 and 0 <= col < 9:
            return self._grid[row][col].get_notes()
        else:
            raise IndexError("Row or column index out of range.")

    def __str__(self):
        """
        Returns a string representation of the Sudoku board.
        :return:
        """
        board_str = ""
        for row in self._grid:
            for cell in row:
                value = cell.get_value()
                if value is None:
                    board_str += "? "
                else:
                    board_str += str(value) + " "
            board_str += "\n"
        return board_str
