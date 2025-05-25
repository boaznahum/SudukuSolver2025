

if __name__ == '__main__':
    from gui.SudokuGUI import SudokuGUI
    from data.SudokuBoard import SudokuBoard
    from data.SudokuBoard import SudokuBoard

    #fill the board with numbers
    board = SudokuBoard.from_string("""
    5 3 ? ? 7 ? ? ? ?
    6 ? ? 1 9 5 ? ? ?
    ? 9 8 ? ? ? ? 6 ?
    8 ? ? ? 6 ? ? ? 3
    4 ? ? 8 ? 3 ? ? 1
    7 ? ? ? 2 ? ? ? 6
    ? 6 ? ? ? ? 2 8 ?
    ? ? ? 4 1 9 ? ? 5
    ? ? ? ? 8 ? ? 7 9
    """)

    board.set_cell_value(0,0, 9)
    board.set_cell_value(8,8, 8)
    board.set_cell_note(1,1, 5)

    gui = SudokuGUI(board)
    board = gui.run()

    print(board)

