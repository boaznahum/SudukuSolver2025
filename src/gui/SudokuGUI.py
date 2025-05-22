import tkinter as tk
from data.SudokuBoard import SudokuBoard

class SudokuGUI:
    def __init__(self, board: SudokuBoard):
        self.board = board
        self.root = tk.Tk()
        self.root.title("Sudoku Board Input")
        self.entries: list[list[tk.Entry | None]] = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        validate_cmd = self.root.register(self.validate_input)

        subgrid_frames = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=2, bd=0)
                frame.grid(row=i, column=j, padx=2, pady=2)
                subgrid_frames[i][j] = frame

        for i in range(9):
            for j in range(9):
                subgrid_row, subgrid_col = i // 3, j // 3
                e = tk.Entry(subgrid_frames[subgrid_row][subgrid_col], width=2, font=('Arial', 18), justify='center',
                             validate="key", validatecommand=(validate_cmd, "%P"))
                e.grid(row=i % 3, column=j % 3, padx=1, pady=1)
                if self.board.grid[i][j].value:
                    e.insert(0, str(self.board.grid[i][j].value))
                self.entries[i][j] = e

        solve_button = tk.Button(self.root, text="Solve", command=self.on_solve)
        solve_button.grid(row=9, column=0, columnspan=4, pady=10, sticky="w")
        ok_button = tk.Button(self.root, text="OK", command=self.on_ok)
        ok_button.grid(row=9, column=5, columnspan=4, pady=10, sticky="e")

    def refresh_gui(self):
        for i in range(9):
            for j in range(9):
                val = self.board.grid[i][j].value
                self.entries[i][j].delete(0, tk.END)
                if val is not None:
                    self.entries[i][j].insert(0, str(val))


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
                val = self.entries[i][j].get()
                self.board.grid[i][j].value = int(val) if val.isdigit() and 1 <= int(val) <= 9 else None

    def run(self) -> SudokuBoard:
        self.root.mainloop()
        return self.board
