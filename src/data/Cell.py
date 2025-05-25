class Cell:
    _value: int | None

    # represents a 3x3 grid of notes, each cell can have a note from 1 to 9
    _notes: list[bool]

    def __init__(self, value: int | None = None):
        self._value = value
        self._notes = [False] * 9


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
        self._notes = [False] * 9

    def get_value(self) -> int | None:
        """
            Returns the value of the cell.
            :return:
        """
        return self._value

    def set_note(self, note: int):

        """
        Sets a note for the cell.

        This method clears the cell's value and sets a note in the notes list at the index corresponding to the given note (1-9).
        Raises a ValueError if the note is not between 1 and 9.

        :param note: The note to set (must be between 1 and 9).
        :raises ValueError: If note is not in the range 1-9.
        :return: None
        """

        if note < 1 or note > 9:
            raise ValueError("Note must be between 1 and 9.")
        self._value = None
        self._notes[note-1] = True

    def clear_note(self, note: int):
        """
        Clears the note of the cell for the given note value.
        This also clears the value of the cell.
        Raises ValueError if the note is not between 1 and 9.

        :param note: The note to clear (must be between 1 and 9).
        :return: None
        """

        if note < 1 or note > 9:
            raise ValueError("Note must be between 1 and 9.")
        self._value = None
        self._notes[note-1] = False

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
            self.set_note(note)

    def get_notes(self) -> list[int | None]:
        """
            Returns the notes of the cell.
            The list contains 9 elements, each element can be None or a number between 1 and 9.
            :return:
        """
        notes: list[int | None ] = []
        for i in range(9):
            if self._notes[i]:
                notes.append(i + 1)
            else:
                notes.append(None)

        return notes

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
            self.set_note(note_row * 3 + note_col + 1)  # +1 because notes are 1-indexed (1-9), not 0-indexed (0-8)

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
            self.clear_note(note_row * 3 + note_col + 1)
