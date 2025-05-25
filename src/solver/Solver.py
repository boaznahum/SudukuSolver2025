import enum

from data import SudokuBoard

class State(enum.Enum):
    IDLE = "idle"
    NOTES = "creating_notes"
    SOLVING = "solving"

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
        # if we in state IDLE, we move to state NOTES, starting in row,col 0,0
        # if we in state NOTES, we advance to next row col 0,0 -> 0,1 -> 0,2 -> 0,3 -> 0,4 -> 0,5 -> 0,6 -> 0,7 -> 0,8
        #  when we finish we move to state SOLVING

        if self._state == State.IDLE:
            self._state = State.NOTES
            self._current_row = 0
            self._current_col = 0
            print("State changed to NOTES, starting at (0,0)")

        elif self._state == State.NOTES:
            print(f"Current position: ({self._current_row}, {self._current_col})")
            # If we are at the last cell, we finish the notes phase
            if self._current_row == 8 and self._current_col == 8:
                self._state = State.SOLVING
                print("Finished creating notes, moving to SOLVING state.")
                return True

            # Move to the next cell
            if self._current_col < 8:
                self._current_col += 1
            else:
                self._current_col = 0
                self._current_row += 1

        board: SudokuBoard = self._board
        # now operate according to the current state
        if self._state == State.NOTES:
            print("Creating notes for Sudoku...")
            # Here we would implement the logic to create notes for the Sudoku board
            # For now, we will just simulate some notes
            board.get_cell(self._current_row,self._current_col).set_notes(1, 2, 3, 4, 5, 6, 7, 8, 9)
            return True
        if self._state == State.SOLVING:
            print("Solving Sudoku...")
            # Here we would implement the solving logic
            # For now, we will just simulate a solved board
            return True

        return False



