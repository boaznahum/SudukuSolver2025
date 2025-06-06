import tkinter as tk
from tkinter import Button
from typing import Generator
import copy

from data.Cell import Cell
from data.SudokuBoard import SudokuBoard
from solver import Solver


class SudokuGUI:
    """
    A graphical user interface (GUI) for displaying and editing a Sudoku board.

    Structure:
    - The main window displays a 9x9 Sudoku board, organized as a 3x3 grid of larger sub grids (big boards).
    - Each big board (subgrid) is itself a 3x3 grid of cells.
    - Each cell can either:
        - Contain a value (1-9), shown as a large Entry widget for user input.
        - If the cell has no value, it displays a smaller 3x3 grid of labels, each representing a possible note (1-9).
    - The GUI allows users to input values or notes, and provides buttons for solving the puzzle or confirming input.
    - The class maintains references to all Entry widgets and note label widgets for synchronizing the GUI with the underlying Sudoku board model.
    """
    _solver_gen: Generator[bool, bool, None] | None
    ok_button: Button
    abort_button: Button
    next_button: Button
    solve_button: Button
    reset_button: Button
    debug_check:tk.Checkbutton


    def __init__(self, board: SudokuBoard):
        self.board = board
        self._initial_board = copy.deepcopy(board)  # Store initial state
        self.root = tk.Tk()
        self.root.title("Sudoku Board Input")
        self.entries: list[list[tk.Entry | None]] = [[None for _ in range(9)] for _ in range(9)]
        self.notes_labels: list[list[list[list[tk.Label]] | None]] = [
            [ None for _ in range(9)] for _ in range(9)
        ]

        self._debug_var = tk.BooleanVar(value=False)

        self._solver_gen = None  # Will hold the generator

        self._debug_mode = False  # Set to True to enable debug mode single step mode

        self._solving= False  # Flag to indicate if the solver is currently running
        self._solver = Solver(board)
        self.create_widgets()




    def create_widgets(self) -> None:
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
                    self.notes_labels[i][j] = None
                else:
                    # Create a 3x3 grid of labels for notes
                    frame = tk.Frame(subgrid_frames[subgrid_row][subgrid_col], width=40, height=40, bd=1, relief="solid")
                    frame.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
                    self.entries[i][j] = None  # No single entry for this cell
                    labels_list = [] # we don't fill directly self._notes_labels[i][j] we can't initialize it with None due to type checker
                    for ni in range(3):
                        label_row = []
                        for nj in range(3):
                            note_val = cell.get_note(ni, nj)
                            note = tk.Label(frame, text=str(note_val) if note_val else "", font=('Arial', 6), width=2, height=1)
                            note.grid(row=ni, column=nj, sticky="nsew")
                            label_row.append(note)
                        labels_list.append(label_row)
                    self.notes_labels[i][j] = labels_list
                    for ni in range(3):
                        frame.grid_rowconfigure(ni, weight=1)
                        frame.grid_columnconfigure(ni, weight=1)

        self.solve_button = tk.Button(self.root, text="Solve", command=self.on_solve)
        self.solve_button.grid(row=9, column=0, columnspan=2, pady=10, sticky="w")

        # noinspection PyTypeChecker
        self.next_button = tk.Button(self.root, text="Next", command=self.on_next, state=tk.DISABLED)
        self.next_button.grid(row=9, column=2, columnspan=2, pady=10, sticky="w")

        # noinspection PyTypeChecker
        self.abort_button = tk.Button(self.root, text="Abort", command=self.on_abort, state=tk.DISABLED)
        self.abort_button.grid(row=9, column=4, columnspan=2, pady=10, sticky="w")

        self.ok_button = tk.Button(self.root, text="OK", command=self.on_ok)
        self.ok_button.grid(row=9, column=6, columnspan=3, pady=10, sticky="e")

        self.debug_check = tk.Checkbutton(self.root, text="Debug Mode", variable=self._debug_var)
        self.debug_check.grid(row=10, column=0, columnspan=3, pady=5, sticky="w")

        self.reset_button = tk.Button(self.root, text="Reset", command=self.on_reset)
        self.reset_button.grid(row=10, column=3, columnspan=3, pady=5, sticky="e")
        #

    def refresh_gui(self) -> None:
        """
        Efficiently synchronizes the GUI with the current state of the Sudoku board.
        Only updates or recreates widgets if the cell type (value/notes) has changed.
        Ensures that self.entries and self.notes are mutually exclusive for each cell.
        """
        for i in range(9):
            for j in range(9):
                cell: Cell = self.board.get_cell(i, j)
                cell_value = cell.get_value()
                subgrid_row, subgrid_col = i // 3, j // 3
                parent_frame = self.root.grid_slaves(row=subgrid_row, column=subgrid_col)[0]

                if cell_value:
                    # If Entry already exists, just update its value
                    entry = self.entries[i][j]
                    if entry is not None:
                        current_val = entry.get()
                        if current_val != str(cell_value):
                            entry.delete(0, tk.END)
                            entry.insert(0, str(cell_value))
                    else:
                        # Remove note widgets if present
                        notes_at_i_j = self.notes_labels[i][j]
                        if notes_at_i_j is not None:
                            for ni in range(3):
                                for nj in range(3):
                                    note_label = notes_at_i_j[ni][nj]
                                    if note_label is not None:
                                        note_label.master.destroy()
                            self.notes_labels[i][j] = None
                        # Create Entry widget
                        e = tk.Entry(parent_frame, width=4, font=('Arial', 18), justify='center',
                                     validate="key", validatecommand=(self.root.register(self.validate_input), "%P"))
                        e.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
                        e.insert(0, str(cell_value))
                        self.entries[i][j] = e
                    # Always nullify notes if Entry exists
                    self.notes_labels[i][j] = None
                else:
                    # If notes grid already exists, just update note labels
                    entry_at_i_j = self.entries[i][j]
                    if entry_at_i_j is not None:
                        entry_at_i_j.destroy()
                        self.entries[i][j] = None
                    notes_at_i_j = self.notes_labels[i][j]
                    if notes_at_i_j is not None:
                        all_none = True
                        for ni in range(3):
                            for nj in range(3):
                                note_label = notes_at_i_j[ni][nj]
                                assert note_label  # must be not None
                                note_val = cell.get_note(ni, nj)
                                note_label.config(text=str(note_val) if note_val else "")
                                if note_val:
                                    all_none = False
                        # if all notes are None, set background to red
                        for ni in range(3):
                            for nj in range(3):
                                note_label = notes_at_i_j[ni][nj]
                                if all_none and self._solving:
                                    note_label.config(bg="red")
                                else:
                                    note_label.config(bg="SystemButtonFace")
                    else:
                        # Create 3x3 grid of labels for notes
                        frame = tk.Frame(parent_frame, width=40, height=40, bd=1, relief="solid")
                        frame.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky="nsew")
                        notes_at_i_j = []
                        all_none = True
                        for ni in range(3):
                            notes_row = []
                            for nj in range(3):
                                note_val = cell.get_note(ni, nj)
                                note = tk.Label(frame, text=str(note_val) if note_val else "", font=('Arial', 6),
                                                width=2, height=1)
                                note.grid(row=ni, column=nj, sticky="nsew")
                                if note_val:
                                    all_none = False
                                notes_row.append(note)
                            notes_at_i_j.append(notes_row)
                        self.notes_labels[i][j] = notes_at_i_j
                        # Set background color based on notes
                        for ni in range(3):
                            for nj in range(3):
                                note_label = notes_at_i_j[ni][nj]
                                if all_none and self._solving:
                                    note_label.config(bg="red")
                                else:
                                    note_label.config(bg="SystemButtonFace")

                        for ni in range(3):
                            frame.grid_rowconfigure(ni, weight=1)
                            frame.grid_columnconfigure(ni, weight=1)
                    # Always nullify entry if notes exist
                    self.entries[i][j] = None

    # noinspection PyMethodMayBeStatic
    def validate_input(self, value: str) -> bool:
        return value == "" or (value.isdigit() and 1 <= int(value) <= 9)

    def on_ok(self):
        self.refresh_model()
        self.root.destroy()

    def on_solve(self):

        self.refresh_model()

        self._solver = Solver(self.board)
        self._solver_gen = self._solver.solve()
        self._step_solver(first=True)

        self._solving = True

        if not self._debug_var.get():
            # If not in debug mode, automatically solve the puzzle
            # This will run the solver until it finishes or is aborted

            self._auto_solve_step()

    def _auto_solve_step(self):
        try:
            self._step_solver(first=False, continue_solving=True)
            self.refresh_gui()
            # Schedule the next step after a short delay (e.g., 10 ms)
            # noinspection PyTypeChecker
            self.root.after(10, self._auto_solve_step)
        except StopIteration:
            self._exit_solving_mode()




    def _step_solver(self, first=False, continue_solving=True):
        try:
            if first:
                result = next(self._solver_gen)
            else:
                result = self._solver_gen.send(continue_solving)
        except StopIteration:
            # noinspection PyTypeChecker
            self._exit_solving_mode()
            self.refresh_gui()
            return

        self.refresh_gui()
        if not result:
            # noinspection PyTypeChecker
            self.next_button.config(state=tk.NORMAL)
            # noinspection PyTypeChecker
            self.abort_button.config(state=tk.NORMAL)
            # noinspection PyTypeChecker
            self.solve_button.config(state=tk.DISABLED)
            # noinspection PyTypeChecker
            self.solve_button.config(state=tk.DISABLED)
        else:
            # noinspection PyTypeChecker
            self._exit_solving_mode()

    def on_next(self):
        if not  self._debug_var.get():  # switch back to auto-solve mode
            # In debug mode, step through the solver
            self._auto_solve_step()
        else:
            self._step_solver(first=False, continue_solving=True)

    def on_abort(self):
        self._step_solver(first=False, continue_solving=False)
        # noinspection PyTypeChecker
        self._exit_solving_mode()

    def _exit_solving_mode(self):
        """
        Enable solve and disable next and abort buttons.
        :return:
        """
        # noinspection PyTypeChecker
        self.next_button.config(state=tk.DISABLED)
        # noinspection PyTypeChecker
        self.abort_button.config(state=tk.DISABLED)
        # noinspection PyTypeChecker
        self.reset_button.config(state=tk.NORMAL)
        # noinspection PyTypeChecker
        self.solve_button.config(state=tk.NORMAL)

        self._solving = False  # Reset solving flag

    def on_reset(self):
        self.board = copy.deepcopy(self._initial_board)
        self.refresh_gui()
        self._exit_solving_mode()

    def refresh_model(self):
        for i in range(9):
            for j in range(9):
                cell = self.board.get_cell(i, j)
                if self.entries[i][j] is not None:
                    val = self.entries[i][j].get()
                    cell.set_value(int(val) if val.isdigit() and 1 <= int(val) <= 9 else None)
                elif self.notes_labels[i][j] is not None:
                    for ni in range(3):
                        for nj in range(3):
                            note_label = self.notes_labels[i][j][ni][nj]
                            note_val = note_label.cget("text") if note_label else ""
                            if note_val.isdigit():
                                cell.set_note_by_loc(ni, nj)
                            else:
                                cell.clear_note_by_loc(ni, nj)

    def run(self) -> SudokuBoard:
        self.root.mainloop()
        return self.board
