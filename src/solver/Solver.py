import enum

from data import SudokuBoard
from data.Cell import Cell


class State(enum.Enum):
    IDLE = "idle"
    NOTES = "creating_notes"
    SOLVING = "solving"
    SOLVED = "solved"

class Solver:




    def __init__(self, board: SudokuBoard):
        super().__init__()
        self._board: SudokuBoard = board
        self._state: State = State.IDLE
        self._current_row: int = 0
        self._current_col: int = 0

    def solve(self) -> bool:
        print("Solving Sudoku..., state is", self._state)

        # define machine state
        # if we in state IDLE, we move to state NOTES,
        # if we in state NOTES, we advance to state SOLVING
        #  when we finish we move to state SOLVED

        if self._state == State.IDLE:
            self._state = State.NOTES
            self._update_notes()

        elif self._state == State.NOTES:
            self._state = State.SOLVING

        if self._state == State.SOLVING:
            # if we are in state SOLVING, we try to solve the Sudoku
            # if we found a single note cell, we replace it and update notes
            # if we didn't find a single note cell, we stop the solving process
            self._solve()





        return False

    def _update_notes(self):
        """
        Update notes for all cells in the Sudoku board.
        """
        print("Updating notes for all cells.")
        for row in range(9):
            for col in range(9):
                self._update_cell_notes(row, col)

    def _update_cell_notes(self, cell_row, cell_col):
        """
        Update the notes for the current cell.
        """

        cell: Cell = self._board.get_cell(cell_row, cell_col)

        value = cell.get_value()

        if value is not None:
            return

        # If the cell is empty, we can set some notes

        cells_in_areas: list[int] = self._board.get_values_in_3_areas(cell_row, cell_col)
        for x in range(1, 10):
            # for current row, col , get all cells in row current_row, in col_current_col, and 3x3 board that contains
            #             # the current cell
            if x not in cells_in_areas:
                cell.set_note(x)
            else:
                cell.clear_note(x)

    def _solve(self):
        print("Actually Solving Sudoku...")

        # search for a cell with a singe not, and set the value of this cell to this note
        if self._replace_single_note_cells():
            print("Found a single note cell and replaced it.")
            # after replacing a single note cell, we need to update notes for all cells
            self._update_notes()
        else:
            print("No single note cell found, stopping the solving process.")

    def _replace_single_note_cells(self):
        """
        Replace cells with a single note with that note.
        Return true when found one and replaced it, false otherwise.
        """
        for row in range(9):
            for col in range(9):
                cell: Cell = self._board.get_cell(row, col)
                # if the cell has a value, we skip it
                if cell.get_value() is not None:
                    continue
                notes = cell.get_notes()
                if notes.count(None) == 8:

                    # this means that the cell has only one note
                    for note in range(1, 10):
                        if notes[note - 1] is not None:
                            # set the value of the cell to this note
                            cell.set_value(note)
                            print(f"Found a single note cell at ({row}, {col}) with note {note}.")
                            # update notes for all cells
                            return True
        return False










