board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def validate_sudoku_board(board):
    for row in range(9):
        if not validate_sudoku_arr(board[row]):
            return False

    for col in range(9):
        if not validate_sudoku_arr([board[row][col] for row in range(9)]):
            return False

    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            if not validate_sudoku_arr([board[r][c] for r in range(row, row + 3) for c in range(col, col + 3)]):
                return False

    # # diagonals (for Sudoku X / Diagonal Sudoku)
    # if not validate_sudoku_arr([board[i][i] for i in range(9)]):  # Main diagonal
    #     return False
    # if not validate_sudoku_arr([board[i][8 - i] for i in range(9)]):  # Anti diagonal
    #     return False
    
    return True

def validate_sudoku_arr(group):
    group = [num for num in group if num != 0]
    return len(group) == len(set(group))

def validate_sudoku_win(board):
    if any(num == 0 for row in board for num in row):
        return False
    return validate_sudoku_board(board)

def validate_available_position(board, row, column, num):
    if num in board[row]:
        return False
    
    if num in [board[i][column] for i in range(9)]:
        return False
    
    subgrid_row = (row // 3) * 3
    subgrid_col = (column // 3) * 3
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if board[i][j] == num:
                return False
            
    # # # diagonals (for Sudoku X / Diagonal Sudoku)
    # if row == column and num in [board[i][i] for i in range(9)]:
    #     return False

    # if row + column == 8 and num in [board[i][8 - i] for i in range(9)]:
    #     return False
    
    return True

def find_available_positions(board, scan_type, scan_index, num):
    available_positions = []
    
    if scan_type == 'row':
        row = board[scan_index]
        available_positions = [(scan_index, i) for i in range(9) if row[i] == 0 and validate_available_position(board,scan_index, i, num)]
        
    elif scan_type == 'column':
        available_positions = [(i, scan_index) for i in range(9) if board[i][scan_index] == 0 and validate_available_position(board, i, scan_index, num)]
    
    elif scan_type == 'subgrid':
        subgrid_row = (scan_index // 3) * 3
        subgrid_col = (scan_index % 3) * 3
        available_positions = [(r, c) for r in range(subgrid_row, subgrid_row + 3) for c in range(subgrid_col, subgrid_col + 3) if board[r][c] == 0 and validate_available_position(board, r, c, num)]
    
    # # diagonals (for Sudoku X / Diagonal Sudoku)
    # elif scan_type == 'main_diagonal':
    #     available_positions = [(i, i) for i in range(9) if board[i][i] == 0 and validate_available_position(board, i, i, num)]
    
    # elif scan_type == 'anti_diagonal':
    #     available_positions = [(i, 8 - i) for i in range(9) if board[i][8 - i] == 0 and validate_available_position(board, i, 8 - i, num)]
    else:
        print("wtf is this input, i died..")
        exit()

    return available_positions

def move(board):
    for num in range(1, 10):
        # diagonals (for Sudoku X / Diagonal Sudoku)
        # for scan_type in ['row', 'column', 'subgrid', 'main_diagonal', 'anti_diagonal']: 
        for scan_type in ['row', 'column', 'subgrid']:
            for scan_index in range(9):
                available_positions = find_available_positions(board,scan_type, scan_index, num)

                if len(available_positions) == 1:
                    row, col = available_positions[0]
                    board[row][col] = num
                    
                    if validate_sudoku_board(board):
                        return True
                    
                    board[row][col] = 0
    
    return False

def print_board(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        
        row_str = ""
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += " | "
            
            row_str += f"{num} " if num != 0 else ". "
        
        print(row_str)

def auto_game(board):
    while(validate_sudoku_win(board) == False):
        print("\n@@@@@@@@@@@@@@@@@@@@@\n")
        print_board(board)
        if move(board) == False:
            print("can't make a move, there is no simple result")
            exit()

        if(validate_sudoku_board(board) == False):
            print("\n\t\t\t board is broken! \n\t\t\t fix your game! \n\t\t\t Bye Bye..")
            exit()

    print("\n\t\t\t YOU WON! \n\t\t\t GG")        
    print_board(board)
    print(validate_sudoku_board(board))

auto_game(board)