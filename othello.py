import time
import threading
import random

board = [['.' for _ in range(8)] for _ in range(8)]    # Creates the board
board[3][3] = 'W'
board[4][4] = 'W'
board[3][4] = 'B'
board[4][3] = 'B'

directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))    # All the directions that are used to check for flips

def main():
    print(" - Welcome to Othello - ")
    menu()

def menu():    # Asks the user which mode they want to play
    menu_select = int(input("\n1. Singleplayer\n2. Multiplayer\n3. How to play\n > "))
    if menu_select == 1:
        difficulty = input("\nSingle-player\nSelect difficulty:\n1. Easy\n2. Intermediate\n > ")
        game_loop("singleplayer", int(input("Time limit in seconds (0 for unlimited): ")), "W", difficulty)
    if menu_select == 2:
        time_limit = int(input("Time limit in seconds (0 for unlimited): "))
        multiplayer(time_limit)
    if menu_select == 3:
        print("\nHow to play:\n\nThe game is played on a board with 8 rows and 8 columns, with a total of 64 squares.\nEach player has 32 pieces, either white or black.\nThe game starts with 2 white pieces and 2 black pieces in the center of the board.\n\nThe goal of the game is to have the most pieces on the board when the game ends.\nThis is done by placing pieces on the board in such a way that you flip your opponent's pieces.\n\nA move is valid if it results in at least one piece being flipped.\nA move is invalid if it results in no pieces being flipped.\n\nA piece is flipped if it is between two of you pieces on opposing sides, the same applies if multiple pieces are surrounded.\n\nThe game ends when there are no more valid moves left.\n\nTo place a piece, enter the coordinates of the square you want to place your piece on.\nFor example, to place a piece on the top left square, enter 'a1'.\n")
        menu()



def singleplayer(difficulty):    # Singleplayer mode with 3 difficulties
    if difficulty == "1":
        easy(board)
    if difficulty == "2":
        intermediate(board)

    '''easy: plays any valid possible move
    intermediate: plays any valid possible move that results in the most flips
    hard: looks 3 layers deep and plays the path that results in the most flips while assuming the opponent will play the path that minimizes losses. not complete'''
    pass

def multiplayer(time_limit):    # Multiplayer mode's main function, changes turns and calls other functions

    turn = "W"

    game_loop("multiplayer", time_limit, turn)

    if game_over(board, turn):
        count_points(board)
        print("\nGame over!")


def print_board(board, turn):    # Prints the board
    for ycount, row in enumerate(board):
        print(f'{ycount+1} {" ".join(row)}')
    print("\n  A B C D E F G H")
    print("\nIt is " + turn + "'s turn.")

def get_flippable_pieces(board, turn, move):    # Checks and returns a list if there are any possible flips given the board, turn and move
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

    for x_, y_ in get_flippable_pieces(board, turn, move):
        board[y_][x_] = turn


def get_points(board, turn, move):    # Returns the total number of pieces that will be flipped if a piece is placed on the board
    x, y = move[0], move[1]
    flipped = 0

    for depthx, depthy in directions:
        distance = 1
        while True:
            x_ = x + depthx * distance
            y_ = y + depthy * distance

            if x_ < 0 or x_ > 7 or y_ < 0 or y_ > 7 or board[y_][x_] == '.':
                break

            if board[y_][x_] == turn:
                flipped += distance - 1
                break

            distance += 1

    return flipped

def check_valid_move(board, turn, move):    # Uses get_flippable_pieces to check if a move is valid and is within the board

    x, y = move[0], move[1]

    if board[y][x] == '.':
      return get_flippable_pieces(board, turn, move)


def mover(turn):    # Gets the move from the user and converts it into coordinates

    move = input("\nPlease enter your move: ").lower()

    move = list(move)
    move[0] = ord(move[0]) - 97
    move[1] = int(move[1]) - 1

    while not check_valid_move(board, turn, move):
        print("\nInvalid move.")
        move = input("\nPlease enter your move: ").lower()

        move = list(move)
        move[0] = ord(move[0]) - 97
        move[1] = int(move[1]) - 1

    place_piece(board, turn, move)

def time_input(time_limit, turn):
    exit_event = threading.Event()
    def move_wrapper():
        while not exit_event.is_set():
            if mover(turn) == 0:
                break

    input_thread = threading.Thread(target = move_wrapper)
    input_thread.start()
    input_thread.join(timeout = time_limit)

    if input_thread.is_alive():
        exit_event.set()
        print("Time's up! Next player!")

def game_loop(mode, time_limit, turn, difficulty = None):
    if mode == "singleplayer":
        if time_limit > 0:
            while not game_over(board, turn):
                if turn == "W":

                    print_board(board, turn)

                    time_input(time_limit, turn)

                else:
                    singleplayer(difficulty)
                turn = "B" if turn == "W" else "W"

        else:
            while not game_over(board, turn):
                if turn == "W":

                    print_board(board, turn)

                    mover(turn)

                else:
                    singleplayer(difficulty)
                turn = "B" if turn == "W" else "W"

    else:
        if time_limit > 0:
            while not game_over(board, turn):

                print_board(board, turn)

                time_input(time_limit, turn)

                turn = "B" if turn == "W" else "W"

        else:
            while not game_over(board, turn):

                print_board(board, turn)

                mover(turn)

                turn = "B" if turn == "W" else "W"

def get_moves(board, turn):
    moves = []
    for yc, y in enumerate(board):
        for xc, x in enumerate(y):

            if x == "." and check_valid_move(board, turn, (xc, yc)):
                moves.append([xc, yc])

    return False if len(moves) == 0 else moves

def easy(board):
    move = random.choice(get_moves(board, "B")) # pick random from possible moves
    place_piece(board, "B", move)

def intermediate(board):
    moves = {}
    for pmovec, pmove in enumerate(get_moves(board, "B")):
        moves[pmovec] = get_points(board, "B", pmove)

    move = max(moves.values())
    key = list(moves.keys())[list(moves.values()).index(move)]
    move = get_moves(board, "B")[key]
    place_piece(board, "B", move)

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
