import tkinter as tk

from data.Cell import Cell
from data.SudokuBoard import SudokuBoard

class SudokuGUI:
    def __init__(self, board: SudokuBoard):
        self.board = board
        self.root = tk.Tk()
        self.root.title("Sudoku Board Input")
        self.entries: list[list[tk.Entry | None]] = [[None for _ in range(9)] for _ in range(9)]
        self.notes: list[list[list[list[tk.Label | None]]]] = [
            [[[None for _ in range(3)] for _ in range(3)] for _ in range(9)] for _ in range(9)
        ]
        self.create_widgets()


    def create_widgets(self):
        """
        For cell in board create a:
            - Entry if the cell has a value display the value in an Entry widget
            - otherwise display all the notes in a 3x3 grid of labels

        :return:
        """
        validate_cmd = self.root.register(self.validate_input)

        # Create 3x3 grid of frames for subgrids
        subgrid_frames = [[None for _ in range(3)] for _ in range(3)]

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
