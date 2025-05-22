class Cell:
    _value: int | None

    # represents a 3x3 grid of notes, each cell can have a note from 1 to 9
    _notes: list[int | None]

    def __init__(self, value: int | None = None):
        self._value = value
        self._notes = [None] * 10


    def set_value(self,  value: int | None):
        """
            Sets the value of the cell
            This also clears the notes of the cell.

            throws ValueError if the value is not between 1 and 9
            :param value:
            :return:
        """
        if value is not None and (value < 1 or value > 9):
            raise ValueError("Value must be between 1 and 9 or None.")
        self._value = value
        self._notes = [None] * 10

    def get_value(self) -> int | None:
        """
            Returns the value of the cell.
            :return:
        """
        return self._value

    def set_note(self, note: int):
        """
            Sets the note of the cell.
            This clear the value of the cell.
            throws ValueError if the note is not between 1 and 9


            :param note:
            :return:
        """
        if note < 1 or note > 9:
            raise ValueError("Note must be between 1 and 9.")
        self._value = None
        self._notes[note-1] = note

    def set_notes(self, *notes: int):
        """
            Sets the notes of the cell.
            This clear the value of the cell.
            throws ValueError if the note is not between 1 and 9
            :param notes:
            :return:
        """
        self._value = None
        for note in notes:
            if note < 1 or note > 9:
                raise ValueError("Note must be between 1 and 9.")
            self._notes[note-1] = note

    def get_notes(self) -> list[int | None]:
        """
            Returns the notes of the cell.
            :return:
        """
        return self._notes

    def get_note(self, i, j) -> int | None:
        """
            Returns the note of the cell at the given row and column.
            :param i:
            :param j:
            :return:
        """
        if 0 <= i < 3 and 0 <= j < 3:
            return self._notes[i * 3 + j]
        else:
            raise IndexError("Row or column index out of range.")

    def set_note_by_loc(self, note_row: int, note_col:int):
        """
            Sets the note of the cell at the given row and column.
            This clear the value of the cell.
            throws ValueError if the note is not between 1 and 9
            :param note_row:
            :param note_col:
            :return:
        """
        if (0 > note_row or note_row >= 3) or (0 > note_col or note_col >= 3):
            raise IndexError("Note Row or column index out of range or note out of range [0,3).")
        else:
            self._notes[note_row * 3 + note_col] = note_row * 3 + note_col + 1

    def clear_note_by_loc(self, note_row: int, note_col:int):
        """
            Sets the note of the cell at the given row and column.
            This clear the value of the cell.
            throws ValueError if the note is not between 1 and 9
            :param note_row:
            :param note_col:
            :return:
        """
        if (0 > note_row or note_row >= 3) or (0 > note_col or note_col >= 3):
            raise IndexError("Note Row or column index out of range or note out of range [0,3).")
        else:
            self._notes[note_row * 3 + note_col] = None
