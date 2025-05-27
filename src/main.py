

if __name__ == '__main__':
    from gui.SudokuGUI import SudokuGUI
    from data.SudokuBoard import SudokuBoard
    from data.SudokuBoard import SudokuBoard

    #fill the board with numbers
    board = SudokuBoard.from_string("""
    9 1 ?   3 4 ?  ? ? 7
    ? 8 3   ? 9 7  ? 5 ?
    4 2 7   ? ? ?  ? 1 ?
    
    ? ? 2   6 8 ?  4 ? ?
    7 ? 4   2 ? 9  ? ? ?
    ? ? 8   ? 3 4  1 6 ?
    
    8 ? ?   ? ? ?  ? 4 ?
    ? ? 9   ? ? ?  7 2 6
    ? 5 6   ? ? 3  8 ? 1
    """)


    gui = SudokuGUI(board)
    board = gui.run()

    print(board)

