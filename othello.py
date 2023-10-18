board=[['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','B','W','.','.','.'],
    ['.','.','.','W','B','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.']]

def main():
    menu_select = None
    while not menu_select:
        print(" - Welcome to Othello - ")
        menu_select = int(input("\n1. Singleplayer\n2. Multiplayer\n > "))
        match menu_select:
            case 1:
                difficulty = input("\nSingle-player\nSelect difficulty:\n1. Easy\n2. Intermediate\n3. Hard\n > ")
                singleplayer(difficulty)
            case 2:
                multiplayer()


def singleplayer(difficulty):
    '''easy: plays any valid possible move
    intermediate: plays any valid possible move that results in the most flips
    hard: looks 3 layers deep and plays the path that results in the most flips while assuming the opponent will play the path that minimizes losses'''
    pass

def multiplayer():
    turn = "W"
    while not game_over(board, turn):
        for yc, y in enumerate(board):
            print(f'{yc+1} {" ".join(y)}')
        print("\n  A B C D E F G H")
        print("\nIt is " + turn + "'s turn.")
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

def check_flips(board, turn, move):
    flips = []
    directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
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

def place_piece(board, turn, move):
    x, y = move[0], move[1]
    board[y][x] = turn
    for x_, y_ in check_flips(board, turn, move):
        board[y_][x_] = turn

def check_valid_move(board, turn, move):
    x, y = move[0], move[1]
    if board[y][x] == '.':
      if check_flips(board, turn, move) == []:
          return False
      else:
          return True

def get_move():
    move = input("\nPlease enter your move: ")
    if move == 'exit':
        exit()
    else:
        move = list(move.lower())
        move[0] = ord(move[0]) - 97
        move[1] = int(move[1]) - 1
    return move

def count_points(board):
    white = 0
    black = 0
    for y in board:
        for x in y:
            if x == "W":
                white += 1
            elif x == "B":
                black += 1
    print("\nWhite: " + str(white) + "\nBlack: " + str(black))

def game_over(board, turn):
    for yc, y in enumerate(board):
        for xc, x in enumerate(y):
            if x == "." and check_valid_move(board, turn, (xc, yc)):
                return False
    return True

main()
