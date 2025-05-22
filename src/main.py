

if __name__ == '__main__':
    from gui.SudokuGUI import SudokuGUI
    from data.SudokuBoard import SudokuBoard
    from data.SudokuBoard import SudokuBoard

    #fill the board with numbers
    board = SudokuBoard()

    board.set_cell_value(0,0, 9)
    board.set_cell_value(8,8, 9)
    board.set_cell_note(0,0, 5)

    gui = SudokuGUI(board)
    board = gui.run()

    print(board)

