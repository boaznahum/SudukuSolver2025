import Samples

if __name__ == '__main__':
    from gui.SudokuGUI import SudokuGUI
    from data.SudokuBoard import SudokuBoard
    from data.SudokuBoard import SudokuBoard

    #fill the board with numbers
    # board = SudokuBoard.from_string(Samples.EXPERT_1)
    board = SudokuBoard.from_string(Samples.EVIL_1)


    gui = SudokuGUI(board)
    board = gui.run()

    print(board)

