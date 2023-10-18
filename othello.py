board = [['.' for x in range(8)] for y in range(8)]    # Creates the board
board[3][3] = 'W'
board[4][4] = 'W'
board[3][4] = 'B'
board[4][3] = 'B'

turn = "W"    # Sets the starting turn

directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))    # All the directions that are used to check for flips

def main():
    print(" - Welcome to Othello - ")
    menu()
    
def menu():    # Asks the user which mode they want to play
    menu_select = None
    while not menu_select:
        menu_select = int(input("\n1. Singleplayer\n2. Multiplayer\n > "))
        match menu_select:
            case 1:
                difficulty = input("\nSingle-player\nSelect difficulty:\n1. Easy\n2. Intermediate\n3. Hard\n > ")
                singleplayer(difficulty)
            case 2:
                multiplayer()

def singleplayer(difficulty):    # Singleplayer mode with 3 difficulties
    '''easy: plays any valid possible move
    intermediate: plays any valid possible move that results in the most flips
    hard: looks 3 layers deep and plays the path that results in the most flips while assuming the opponent will play the path that minimizes losses'''
    pass

def multiplayer():    # Multiplayer mode's main function, changes turns and calls other functions
    while not game_over(board, turn):
        
        print_board(board)
        
        move = get_move()
        
        while not check_valid_move(board, turn, move):
            print("\nInvalid move.")
            move = get_move()
        place_piece(board, turn, move)
        
        if turn == "W":
            turn = "B"
        else:
            turn = "W"
    
    if game_over(board, turn):
        count_points(board)
        print("\nGame over!")
        
def print_board(board):    # Prints the board
    for ycount, row in enumerate(board):
        print(f'{ycount+1} {" ".join(row)}')
    print("\n  A B C D E F G H")
    print("\nIt is " + turn + "'s turn.")

def check_flips(board, turn, move):    # Checks and returns a list if there are any possible flips given the board, turn and move
    flips = []
    x, y = move[0], move[1]
    
    for depthx, depthy in directions:
    
        to_flip = []
        distance = 1
    
        while True:
    
            x_ = x + depthx * distance
            y_ = y + depthy * distance
            
            if x_ < 0 or x_ > 7 or y_ < 0 or y_ > 7 or board[y_][x_] == '.':
                break
    
            if board[y_][x_] == turn:
                flips.extend(to_flip)
                break
    
            else:
                to_flip.append((x_, y_))
                distance += 1
    
    return flips

def place_piece(board, turn, move):    # Places a piece on the board and flips the pieces that need to be flipped
    
    x, y = move[0], move[1]
    board[y][x] = turn
    
    for x_, y_ in check_flips(board, turn, move):
        board[y_][x_] = turn

def check_valid_move(board, turn, move):    # Uses check_flips to check if a move is valid and is within the board
    
    x, y = move[0], move[1]
    
    if board[y][x] == '.':
      if check_flips(board, turn, move) == []:
          return False
    
      else:
          return True

def get_move():    # Gets the move from the user and converts it into coordinates
    
    move = input("\nPlease enter your move: ")
    if move == 'exit':
        exit()
        
    else:
        move = list(move.lower())
        move[0] = ord(move[0]) - 97
        move[1] = int(move[1]) - 1
        
    return move

def count_points(board):    # Counts the points of each player and prints it
    
    white = 0
    black = 0
    
    for y in board:
        for x in y:
            
            if x == "W":
                white += 1
                
            elif x == "B":
                black += 1
                
    if white > black:
        print(f"\White wins with {white} points! ({white} - {black})")
        
    if black > white:
        print(f"\Black wins with {black} points! ({black} - {white})")
        
    if white == black:
        print(f"\nIt's a tie! ({white} - {black})")

def game_over(board, turn):    # Checks if the game is over by checking if there are any valid moves left
    
    for yc, y in enumerate(board):
        for xc, x in enumerate(y):
            
            if x == "." and check_valid_move(board, turn, (xc, yc)):
                return False
            
    return True

if __name__ == "__main__":    # Runs the main function
    main()
