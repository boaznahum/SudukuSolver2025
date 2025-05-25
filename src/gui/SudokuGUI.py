import tkinter as tk

from data.Cell import Cell
from data.SudokuBoard import SudokuBoard

class SudokuGUI:
    """
    A graphical user interface (GUI) for displaying and editing a Sudoku board.

    Structure:
    - The main window displays a 9x9 Sudoku board, organized as a 3x3 grid of larger subgrids (big boards).
    - Each big board (subgrid) is itself a 3x3 grid of cells.
    - Each cell can either:
        - Contain a value (1-9), shown as a large Entry widget for user input.
        - If the cell has no value, it displays a smaller 3x3 grid of labels, each representing a possible note (1-9).
    - The GUI allows users to input values or notes, and provides buttons for solving the puzzle or confirming input.
    - The class maintains references to all Entry widgets and note label widgets for synchronizing the GUI with the underlying Sudoku board model.
    """
    def __init__(self, board: SudokuBoard):
        self.board = board
        self.root = tk.Tk()
        self.root.title("Sudoku Board Input")
        self.entries: list[list[tk.Entry | None]] = [[None for _ in range(9)] for _ in range(9)]
        self.notes: list[list[list[list[tk.Label | None]] | None]] = [
            [[[None for _ in range(3)] for _ in range(3)] for _ in range(9)] for _ in range(9)
        ]
        self.create_widgets()


    def create_widgets(self):
        """
        Initializes and arranges all widgets for the Sudoku board GUI.

        Description:
        - Constructs the visual 9x9 Sudoku board as a 3x3 grid of subgrid frames (big boards), each containing a 3x3 grid of cells.
        - For each cell:
            - If the cell has a value, creates a single Entry widget for user input, displays the value, and stores a reference in self.entries.
            - If the cell is empty, creates a 3x3 grid of Label widgets (for notes) inside a Frame, and stores references in self.notes.
        - Adds "Solve" and "OK" buttons at the bottom of the board.

        Class Field Relations:
        - self.entries: 9x9 list of Entry widgets or None. Each [i][j] holds the Entry for cell (i, j) if it has a value, else None.
        - self.notes: 9x9x3x3 list of Label widgets or None.
        - For empty cells, self.notes[i][j][ni][nj] holds the Label for note (ni, nj) in cell (i, j); for value cells, self.notes[i][j] is None.
        - subgrid_frames: Local 3x3 list of Frame widgets, each representing a 3x3 subgrid in the main board.

        Logic:
        1. Registers input validation for Entry widgets.
        2. Creates a 3x3 grid of subgrid frames and arranges them in the main window.
        3. Iterates over all 81 cells:
            a. Determines the subgrid for each cell.
            b. If the cell has a value:
                - Creates an Entry widget, inserts the value, and places it in the correct subgrid.
                - Updates self.entries[i][j] with the Entry; sets self.notes[i][j] to None.
            c. If the cell is empty:
                - Creates a Frame for the cell, then a 3x3 grid of Label widgets for notes.
                - Each Label displays a note if present.
                - Updates self.notes[i][j][ni][nj] with each Label; sets self.entries[i][j] to None.
        4. Adds "Solve" and "OK" buttons below the board.

        This method ensures the GUI structure matches the logical board, and that all widgets are accessible for later updates or synchronization.
        """

        validate_cmd = self.root.register(self.validate_input)

        # Create 3x3 grid of frames for sub grids
        subgrid_frames: list[list[tk.Frame | None]] = [[None for _ in range(3)] for _ in range(3)]

        for y in range(3):
            for x in range(3):
                frame = tk.Frame(self.root, bd=2, relief="groove")
                frame.grid(row=y, column=x, padx=2, pady=2, sticky="nsew")
                subgrid_frames[y][x] = frame

        for i in range(9):
            for j in range(9):
                subgrid_row, subgrid_col = i // 3, j // 3
                cell: Cell = self.board.get_cell(i, j)
                cell_value = cell.get_value()

                if cell_value:
                    # Create Entry widget spanning the entire cell area
                    e = tk.Entry(subgrid_frames[subgrid_row][subgrid_col], width=4, font=('Arial', 18), justify='center',
                                 validate="key", validatecommand=(validate_cmd, "%P"))
                    e.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
                    e.insert(0, str(cell_value))
                    self.entries[i][j] = e
                    self.notes[i][j] = None
                else:
                    # Create a 3x3 grid of labels for notes
                    frame = tk.Frame(subgrid_frames[subgrid_row][subgrid_col], width=40, height=40, bd=1, relief="solid")
                    frame.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
                    self.entries[i][j] = None  # No single entry for this cell
                    self.notes[i][j] = [[None for _ in range(3)] for _ in range(3)]
                    for ni in range(3):
                        for nj in range(3):
                            note_val = cell.get_note(ni, nj)
                            note = tk.Label(frame, text=str(note_val) if note_val else "", font=('Arial', 6), width=2, height=1)
                            note.grid(row=ni, column=nj, sticky="nsew")
                            self.notes[i][j][ni][nj] = note
                    for ni in range(3):
                        frame.grid_rowconfigure(ni, weight=1)
                        frame.grid_columnconfigure(ni, weight=1)



        solve_button = tk.Button(self.root, text="Solve", command=self.on_solve)
        solve_button.grid(row=9, column=0, columnspan=4, pady=10, sticky="w")
        ok_button = tk.Button(self.root, text="OK", command=self.on_ok)
        ok_button.grid(row=9, column=5, columnspan=4, pady=10, sticky="e")

    def refresh_gui(self):
        """
        Synchronizes the GUI with the current state of the Sudoku board.

        Logic:
        - Iterates over all 9x9 cells in the board.
        - For each cell:
            - Determines its parent subgrid frame based on its position.
            - Removes any existing widgets (Entry or note labels) from the cell's location in the GUI.
            - If the cell has a value:
                - Creates a new Entry widget, inserts the value, and places it in the correct position.
                - Updates the internal reference to the Entry widget.
            - If the cell does not have a value:
                - Creates a new Frame to hold a 3x3 grid of note labels.
                - For each possible note (1-9), creates a Label widget displaying the note if present.
                - Arranges the labels in a 3x3 grid within the cell's frame.
                - Updates the internal references to the note label widgets.
        - Ensures the GUI always reflects the current state of the board, including both values and notes.
        """
        for i in range(9):
            for j in range(9):
                cell: Cell = self.board.get_cell(i, j)
                cell_value = cell.get_value()
                subgrid_row, subgrid_col = i // 3, j // 3
                parent_frame = self.root.grid_slaves(row=subgrid_row, column=subgrid_col)[0]
                cell_widgets = parent_frame.grid_slaves(row=i % 3, column=j % 3)
                # Remove all widgets in the cell
                for widget in cell_widgets:
                    widget.destroy()
                if cell_value:
                    # Create Entry widget
                    e = tk.Entry(parent_frame, width=4, font=('Arial', 18), justify='center',
                                 validate="key", validatecommand=(self.root.register(self.validate_input), "%P"))
                    e.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
                    e.insert(0, str(cell_value))
                    self.entries[i][j] = e
                    self.notes[i][j] = [[None for _ in range(3)] for _ in range(3)]
                else:
                    # Create 3x3 grid of labels for notes
                    frame = tk.Frame(parent_frame, width=40, height=40, bd=1, relief="solid")
                    frame.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
                    self.entries[i][j] = None
                    self.notes[i][j] = [[None for _ in range(3)] for _ in range(3)]
                    for ni in range(3):
                        for nj in range(3):
                            note_val = cell.get_note(ni, nj)
                            note = tk.Label(frame, text=str(note_val) if note_val else "", font=('Arial', 6), width=2,
                                            height=1)
                            note.grid(row=ni, column=nj, sticky="nsew")
                            self.notes[i][j][ni][nj] = note
                    for ni in range(3):
                        frame.grid_rowconfigure(ni, weight=1)
                        frame.grid_columnconfigure(ni, weight=1)

    # noinspection PyMethodMayBeStatic
    def validate_input(self, value: str) -> bool:
        return value == "" or (value.isdigit() and 1 <= int(value) <= 9)

    def on_ok(self):
        self.refresh_model()
        self.root.destroy()

    def on_solve(self):

        self.refresh_model()
        # Call your solve function here, e.g. solve_sudoku(board)
        from solver.Solver import Solver  # adjust import as needed
        solver = Solver()
        solver.solve(self.board)
        # Refresh GUI with solution
        self.refresh_gui()

    def refresh_model(self):
        for i in range(9):
            for j in range(9):
                cell = self.board.get_cell(i, j)
                if self.entries[i][j] is not None:
                    val = self.entries[i][j].get()
                    cell.set_value(int(val) if val.isdigit() and 1 <= int(val) <= 9 else None)
                elif self.notes[i][j] is not None:
                    for ni in range(3):
                        for nj in range(3):
                            note_label = self.notes[i][j][ni][nj]
                            note_val = note_label.cget("text") if note_label else ""
                            if note_val.isdigit():
                                cell.set_note_by_loc(ni, nj)
                            else:
                                cell.clear_note_by_loc(ni, nj)
                            self.board.set_cell_note(i, j, int(note_val) if note_val.isdigit() else None)
    def run(self) -> SudokuBoard:
        self.root.mainloop()
        return self.board
