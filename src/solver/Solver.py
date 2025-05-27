import enum
import itertools
from itertools import count
from typing import Generator

from data import SudokuBoard
from data.Cell import Cell


class SolveResult(enum.Enum):
     SOLVED = "solved"
     NOT_SOLVED_YET_CONTINUE = "not_solved_continue"
     NOT_SOLVED_INVALID = "not_solved_invalid"

class UpdateResult(enum.Enum):
     CELL_WITH_NO_NOTES = "cell_with_no_notes"
     ALL_VALUES = "all_values"
     SOME_CELLS_WITH_NOTES = "some_cells_with_notes"


class Solver:

    def __init__(self, board: SudokuBoard):
        super().__init__()
        self._board: SudokuBoard = board
        # self._state: State = State.IDLE
        self._current_row: int = 0
        self._current_col: int = 0

    def solve(self) -> Generator[bool, bool, None]:
        """
        This is iterator generator that solves the Sudoku puzzle step by step.
        ON each step it yields a boolean value indicating whether the Sudoku is solved or not.
        Also, if the caller send it a false value, it will stop the solving process.

        :return:
        """

        # define machine state
        # if we in state IDLE, we move to state NOTES,
        # if we in state NOTES, we advance to state SOLVING
        #  when we finish we move to state SOLVED

        inner_solver: Generator[SolveResult, None, None] = self._solve()

        while True:


            solved_status: SolveResult = next(inner_solver)
            solved = solved_status == SolveResult.SOLVED

            do_continue = yield solved
            if solved:
                print("Sudoku solved, Done.")
                return None

            if solved_status == SolveResult.NOT_SOLVED_INVALID:
                print("Sudoku is not solvable, Done.")
                return None

            if not do_continue:
                print("Stopping the solving process.")
                return None

    def _update_notes(self) -> UpdateResult:
        """
        Update notes for all cells in the Sudoku board.
        return the number of cells that have no value and where notes were updated.
        """
        print("Updating notes for all cells.")
        number_of_cells_with_notes: int = 0
        for row in range(9):
            for col in range(9):
                update_note_result = self._update_cell_notes(row, col)

                if update_note_result >= 0: # a cell with notes
                    if update_note_result == 0:
                        return UpdateResult.CELL_WITH_NO_NOTES  # invalid abort the process
                    else:
                        number_of_cells_with_notes += 1

        if number_of_cells_with_notes == 0:
            return UpdateResult.ALL_VALUES
        else:
            return UpdateResult.SOME_CELLS_WITH_NOTES

    def _update_cell_notes(self, cell_row, cell_col) -> int :
        """
        Update the notes for the current cell.
        return the number of notes in cell
        if less than zero mean it is cell with value
        """

        cell: Cell = self._board.get_cell(cell_row, cell_col)

        value = cell.get_value()

        if value is not None:
            return -1

        # If the cell is empty, we can set some notes

        cells_in_areas: list[int] = self._board.get_values_in_3_areas(cell_row, cell_col)
        number_of_notes: int = 0
        for x in range(1, 10):
            # for current row, col , get all cells in row current_row, in col_current_col, and 3x3 board that contains
            #             # the current cell
            if x not in cells_in_areas:
                cell.set_note(x)
                number_of_notes += 1
            else:
                cell.clear_note(x)

        return number_of_notes

    def _solve(self) -> Generator[SolveResult, None, None] :
        print("Actually Solving Sudoku...")


        while True:

            update_notes_result = self._update_notes()
            if  update_notes_result == UpdateResult.CELL_WITH_NO_NOTES:
                print("Found a cell with no notes, aborting.")
                yield SolveResult.NOT_SOLVED_INVALID
                return
            elif update_notes_result == UpdateResult.ALL_VALUES:
                # if all cells have values, we can assume that the Sudoku is solved
                print("All cells have notes, Sudoku is solved.")
                yield SolveResult.SOLVED
                return
            else:
                yield SolveResult.NOT_SOLVED_YET_CONTINUE

            # search for a cell with a singe not, and set the value of this cell to this note
            if self._replace_single_note_cells():
                # after replacing a single note cell, we need to update notes for all cells
                # this will occur in next iteration of the generator
                yield SolveResult.NOT_SOLVED_YET_CONTINUE
                continue

            # try to solve by recursion
            # now search for a cell with notes and try to replace it with a value
            print("No single note cell found, trying to replace values.")
            yield SolveResult.NOT_SOLVED_YET_CONTINUE  # no single note cell found, we stop the solving process

            # search for a cell with no value but with notes
            # if found a cell with no notes abort the process
            row_col = self._find_cell_with_minimal_number_of_notes()
            if row_col is None:
                print("No cell with notes found, aborting.")
                # this is an internal error, we should not reach this point, see above
                yield SolveResult.NOT_SOLVED_INVALID
                return # stop the solving process, this is an error

            row = row_col[0]
            col = row_col[1]

            cell: Cell = self._board.get_cell(row, col)
            # if the cell has a value, we skip it
            assert cell.get_value() is None

            notes = cell.get_notes()
            if notes.count(None) == 9:
                print(f"Found a cell with no notes at ({row}, {col}), aborting.")
                yield SolveResult.NOT_SOLVED_INVALID
                return # stop the solving process, this is an error

            # if the cell has notes, we try to replace it with a value
            # we can replace this cell with a value
            for note in [ n for n in notes if n is not None ]:

                # set the value of the cell to this note
                print(f"Found a note cell at ({row}, {col} ) going to put  {note}.")
                # let the debugger display before replacing the cell
                yield SolveResult.NOT_SOLVED_YET_CONTINUE
                cell.set_value(note)
                print(f"Set cell at ({row}, {col}) to {note} and updating notes.")
                yield SolveResult.NOT_SOLVED_YET_CONTINUE

                for now_solved in self._solve():
                    if now_solved == SolveResult.SOLVED:
                        print("Sudoku solved after replacing a note cell.")
                        yield SolveResult.SOLVED
                        return # stop the solving process, we solved the Sudoku
                    elif now_solved == SolveResult.NOT_SOLVED_YET_CONTINUE:
                        yield SolveResult.NOT_SOLVED_YET_CONTINUE
                        # and continue next iteration of the inner solver
                        continue


                    assert now_solved == SolveResult.NOT_SOLVED_INVALID

                # not solved, restore the value and continue solving
                print(f"*** Was not able to solve with {note} in cell at ({row}, {col} ), restoring")
                yield SolveResult.NOT_SOLVED_INVALID
                cell.set_value(None)
                self._update_notes() # continue with next note



            # if we reached this point, it means that we didn't find a solution
            yield SolveResult.NOT_SOLVED_INVALID
            # exit the generator
            return

    def _replace_single_note_cells(self) -> bool:
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
                            print(f"Found a single note cell at ({row}, {col}) with note {note} and set it as value.")
                            # update notes for all cells
                            return True
        return False

    def _find_cell_with_minimal_number_of_notes(self) -> tuple[int, int] | None:
        """
        Find a cell with the minimal number of notes.
        Return the row and column of the cell.
        If no such cell found, return (-1, -1).
        """
        min_notes = 10
        min_row = 10000
        min_col = 10000
        found = False
        for row in range(9):
            for col in range(9):
                cell: Cell = self._board.get_cell(row, col)
                if cell.get_value() is not None:
                    # skip cells with value
                    continue

                notes = cell.get_notes()
                # count number of non None notes
                number_of_notes = sum(1 for x in notes if x is not None)
                if number_of_notes < min_notes:
                    min_notes = number_of_notes
                    min_row = row
                    min_col = col
                    found = True
                    if min_notes == 0:
                        # we can stop searching, we found a cell with 0 notes, which is an error
                        return min_row, min_col

        if found:
            return min_row, min_col
        else:
            return None




