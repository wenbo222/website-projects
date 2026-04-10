# Chess
# Wenbo

import copy

# Define constants
ROW=8 # There are 8 rows, labelled 0-7.
COLUMN=8 # There are 8 columns, labelled 0-7.
INDENT=3 # Number of tabs for the chess board during playing.

# Define global variables
# Special characters
special=["○", "●", "CC"]
# Initial Board, and board will always contain the current board
board=[["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
       ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
       ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
       ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
       ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
       ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
       ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
       ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]]
prev_boards=[] # Stores the previous boards
log="" # Move log
log_f="" # Move log (figurine)
count=0 # Full move counts (white and black)
rep_boards_w=[] # Stores possible repetition positions when it's white's turn
rep_counts_w=[] # Stores respective counts for above
rep_boards_b=[] # Stores possible repetition positions when it's black's turn
rep_counts_b=[] # Stores respective counts for above
castling_right_kw=True # The castling right of white kingside
castling_right_qw=True # The castling right of white queenside
castling_right_kb=True # The castling right of black kingside
castling_right_qb=True # The castling right of black queenside
en_passant_right_w=False # The en passant right of white
en_passant_right_b=False # The en passant right of black
castling_kw=False # Whether the move is a white kingside castle
castling_qw=False # Whether the move is a white queenside castle
castling_kb=False # Whether the move is a black kingside castle
castling_qb=False # Whether the move is a black queenside castle
promotion=False # Whether the move is a promotion
en_passant=False # Whether the move is en passant
turn="W" # Whose turn it is
draw_count=0 # If reaches 50, draw


def wait():
    """
    wait() -> None
    
    Tells the user to press enter to continue reading.
    """
    
    input("Press Enter to continue ...")


def is_number(s): # Determine whether the input is a number or not
    """
    is_number(string) -> boolean

    If string can be converted into float, returns True; otherwise, returns False.
    """
    
    try:
        float(s)
        return True # If s is a number, return True
    except ValueError:
        return False # Otherwise, return False


def draw():
    """
    draw() -> (string, string)

    Returns the two global strings, log and log_f, with "1/2-1/2" added to their ends.
    """
    
    return (log+"1/2-1/2", log_f+"1/2-1/2")


def input_yn():
    """
    input_yn() -> "yes" or "no"

    Returns "yes" or "no" depending on user input.
    """
    
    response=input().lower().strip(".,?! ")
    while response not in ["yes", "no"]:
        print("You can only enter yes or no.")
        response=input().lower().strip(".,?! ")
    return response


def th(number):
    """
    th(int) -> string

    Returns the appropriate number and suffix for the int.
    """
    
    if number%100 in [11, 12, 13]:
        return str(number)+"th"
    if number%10==1:
        return str(number)+"st"
    if number%10==2:
        return str(number)+"nd"
    if number%10==3:
        return str(number)+"rd"
    return str(number)+"th"


def end_game():
    """
    end_game() -> None

    Asks the user(s) whether they want to see the move log. If so, print it.
    Asks the user(s) whether they want to see a recap of the game. If so, print previous boards.
    Print a goodbye message.
    """

    # Move log question
    print("Congratulations on finishing the game! Would you like to see the move log?")
    response=input_yn()
    if response=="yes":
        print("PGN: "+log)
        print("")
        print("Figurine Algebraic Notation: "+log_f)
        print("")
        wait()

    # Recap question
    print("Would you like a recap of the game? This will involve printing the board under the perspective of white.")
    response=input_yn()
    if response=="yes":
        for i in range(len(prev_boards)):
            print("After "+th(i+1)+" half-move: ", end="")

            # Checks whether it's white or black
            if i%2==0:
                print("(White's "+th(i//2+1)+")")
            else:
                print("(Black's "+th(i//2+1)+")")
            print_board(prev_boards[i], "W", INDENT)
            wait()
                
    exit()

    
def input_two_numbers_float():
    """
    input_two_numbers_float() -> float

    Ask the user for two float inputs; if the user inputs are not numbers, asks the user to input again until the inputs are numbers.
    However, if the input is draw or resign, a message is outputted and the program is exitted. Modifies log and log_f if necessary.
    Returns the floats inputted.
    """

    global log
    global log_f
    
    s=input().lower().strip("!.,? ").split()

    # If the user(s) decided to draw or resign
    if s==["draw"]:
        if len(prev_boards)<2:
            print("You can only draw by agreement after each player made one move!")
        
        else:
            print("Draw by agreement!")
            log, log_f=draw()
            end_game()
        
    if s==["resign"]:
        if turn=="W":
            if no_material(board, "B"):
                print("Draw by insufficient material!")
                log, log_f=draw()
            else:
                print("Black won by resignation!")
                log+="0-1"
                log_f+="0-1"
        
        else:
            if no_material(board, "W"):
                print("Draw by insufficient material!")
                log, log_f=draw()
            else:
                print("White won by resignation!")
                log+="1-0"
                log_f+="1-0"
        
        end_game()

    while len(s)!=2 or is_number(s[0])==False or is_number(s[1])==False:
        print("Please enter two numbers, separated by a space: ")
        s=input().lower().strip("!.,? ").split()
        
    return [float(s[0]), float(s[1])]


def input_two_numbers_int():
    """
    input_two_numbers_float() -> float

    Ask the user for two int inputs; if the user inputs are not integers, asks the user to input again until the inputs are integers.
    However, if the input is draw or resign, a message is outputted and the program is exitted.
    Returns the integers inputted.
    """
    
    s=input_two_numbers_float()
    
    while s[0].is_integer()==False or s[1].is_integer()==False:
        print("Please enter two integers, separated by a space: ")
        s=input_two_numbers_float()
        
    return [int(s[0]), int(s[1])]


def rev(side):
    """
    rev(string) -> string

    If side is "W", return "B". Otherwise, return "W".
    """
    
    if side=="W":
        return "B"
    return "W"


def print_number(turn, tabs):
    """
    print_board(turn) -> None

    Prints out the horizontal labelling based on the turn.
    """
    
    print("\t"*tabs+" ", end="")
    if turn=="W":
        for i in range(ROW):
            print(" "+str(i)+" ", end="")

    else:
        for i in range(ROW-1, -1, -1):
            print(" "+str(i)+" ", end="")
    
    print("")

def to_graph_piece(piece):
    """
    to_graph_piece(piece) -> string

    Returns the graphical display of the piece, if there is one.
    """
    
    if piece=="WP":
        return "♙"
    elif piece=="BP":
        return "♟"
    
    elif piece=="WN":
        return "♘"
    elif piece=="BN":
        return "♞"
    
    elif piece=="WB":
        return "♗"
    elif piece=="BB":
        return "♝"

    elif piece=="WR":
        return "♖"
    elif piece=="BR":
        return "♜"
    
    elif piece=="WK":
        return "♔"
    elif piece=="BK":
        return "♚"
    
    elif piece=="WQ":
        return "♕"
    elif piece=="BQ":
        return "♛"

    elif piece=="WC":
        return "○"
    elif piece=="BC":
        return "●"
    elif piece=="CC":
        return "✕"

    else:
        return piece

def print_board(board, turn, tabs):
    """
    print_board(2-D list, turn, int) -> None

    Prints out the board based on the turn.
    """

    print_number(turn, tabs)
    print("\t"*tabs+" "+"-"*(3*COLUMN+1))
    
    if turn=="W":
        for i in range(len(board)):
            print("\t"*tabs, end="")
            print(i, end="")
            print("|", end="")
            for piece in board[i]:
                print(piece, end="|")
            print(i)
            print("\t"*tabs+" "+"-"*(3*COLUMN+1))
            
    else:
        for i in range(len(board)-1, -1, -1):
            print("\t"*tabs, end="")
            print(i, end="")
            print("|", end="")
            for j in range(len(board[i])-1, -1, -1):
                print(board[i][j], end="|")
            print(i)
            print("\t"*tabs+" "+"-"*(3*COLUMN+1))
        
    print_number(turn, tabs)


# The following five articles are from: https://handbook.fide.com/chapter/E012023
def article_1():
    """
    article_1() -> None

    Prints out the article 1 of FIDE Laws of Chess.
    """

    print("")
    print("Article 1: The Nature and Objectives of the Game of Chess")
    print("")
    print("1.1     The game of chess is played between two opponents who move their pieces on a square board called a \"chessboard\".")
    print("")
    print("1.2     The player with the light-coloured pieces (White) makes the first move, then the players move alternately, with the player with the dark-coloured pieces (Black) making the next move.")
    print("")
    print("1.3     A player is said to \"have the move\" when his/her opponent\'s move has been \"made\".")
    print("")
    print("1.4     The objective of each player is to place the opponent\'s king \"under attack\" in such a way that the opponent has no legal move.")
    print("\t1.4.1    The player who achieves this goal is said to have \"checkmated\" the opponent’s king and to have won the game. Leaving one\'s own king under attack, exposing one\'s own king to attack and also \"capturing\" the opponent\'s king is not allowed.")
    print("\t1.4.2    The opponent whose king has been checkmated has lost the game.")
    print("")
    print("1.5     If the position is such that neither player can possibly checkmate the opponent\'s king, the game is drawn (see Article 5.2.2).")
    wait()
    

def article_2():
    """
    article_2() -> None

    Prints out the article 2 of FIDE Laws of Chess.
    """

    print("")
    print("Article 2: The Initial Position of the Pieces on the Chessboard")
    print("")
    print("2.1     The chessboard is composed of an 8 x 8 grid of 64 equal squares alternately light (the \"white\" squares) and dark (the \"black\" squares).")
    print("\tThe chessboard is placed between the players in such a way that the near corner square to the right of the player is white.")
    print("")
    print("2.2     At the beginning of the game White has 16 light-coloured pieces (the \"white\" pieces); Black has 16 dark-coloured pieces (the \"black\" pieces).")
    print("\t\tThese pieces are as follows:")
    print("\t\tA white king	\tusually indicated by the symbol ♔(K)")
    print("\t\tA white queen	\tusually indicated by the symbol ♕(Q)")
    print("\t\tTwo white rooks	\tusually indicated by the symbol ♖(R)")
    print("\t\tTwo white bishops\tusually indicated by the symbol ♗(B)")
    print("\t\tTwo white knights\tusually indicated by the symbol ♘(N)")
    print("\t\tEight white pawns\tusually indicated by the symbol ♙")
    print("\t\tA black king	\tusually indicated by the symbol ♚(K)")
    print("\t\tA black queen	\tusually indicated by the symbol ♛(Q)")
    print("\t\tTwo black rooks	\tusually indicated by the symbol ♜(R)")
    print("\t\tTwo black bishops\tusually indicated by the symbol ♝(B)")
    print("\t\tTwo black knights\tusually indicated by the symbol ♞(N)")
    print("\t\tEight black pawns\tusually indicated by the symbol ♟")
    wait()
    print("")
    print("2.3     The initial position of the pieces on the chessboard is as follows:")
    board=[["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
           ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
           ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
           ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
           ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
           ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
           ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
           ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]]
    print_board(board, "W", 1)
    print("")
    print("2.4     The eight vertical columns of squares are called \"files\". The eight horizontal rows of squares are called \"ranks\". A straight line of squares of the same colour, running from one edge of the board to an adjacent edge, is called a \"diagonal\".")
    wait()


def article_3():
    """
    article_3() -> None

    Prints out the article 3 of FIDE Laws of Chess.
    """

    print("")
    print("Article 3: The Moves of the Pieces")
    print("")
    print("3.1     It is not permitted to move a piece to a square occupied by a piece of the same colour.")
    print("\t3.1.1    If a piece moves to a square occupied by an opponent\'s piece the latter is captured and removed from the chessboard as part of the same move.")
    print("\t3.1.2    A piece is said to attack an opponent\'s piece if the piece could make a capture on that square according to Articles 3.2 to 3.8.")
    print("\t3.1.3    A piece is considered to attack a square even if this piece is constrained from moving to that square because it would then leave or place the king of its own colour under attack.")
    print("")
    print("3.2     The bishop may move to any square along a diagonal on which it stands.")
    demo_board_b=[["BC", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "BC", "  ", "  ", "  ", "  ", "  ", "BC"],
                  ["  ", "  ", "BC", "  ", "  ", "  ", "BC", "  "],
                  ["  ", "  ", "  ", "BC", "  ", "BC", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "BB", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "BC", "  ", "BC", "  ", "  "],
                  ["  ", "  ", "BC", "  ", "  ", "  ", "BC", "  "],
                  ["  ", "BC", "  ", "  ", "  ", "  ", "  ", "BC"]]
    print_board(demo_board_b, "W", 1)
    wait()
    
    print("")
    print("3.3     The rook may move to any square along the file or the rank on which it stands.")
    demo_board_r=[["  ", "  ", "  ", "BC", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "BC", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "BC", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "BC", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "BC", "  ", "  ", "  ", "  "],
                  ["BC", "BC", "BC", "BR", "BC", "BC", "BC", "BC"],
                  ["  ", "  ", "  ", "BC", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "BC", "  ", "  ", "  ", "  "]]
    print_board(demo_board_r, "W", 1)
    wait()
    
    print("")
    print("3.4     The queen may move to any square along the file, the rank or a diagonal on which it stands.")
    demo_board_q=[["BC", "  ", "  ", "  ", "BC", "  ", "  ", "  "],
                  ["  ", "BC", "  ", "  ", "BC", "  ", "  ", "BC"],
                  ["  ", "  ", "BC", "  ", "BC", "  ", "BC", "  "],
                  ["  ", "  ", "  ", "BC", "BC", "BC", "  ", "  "],
                  ["BC", "BC", "BC", "BC", "BQ", "BC", "BC", "BC"],
                  ["  ", "  ", "  ", "BC", "BC", "BC", "  ", "  "],
                  ["  ", "  ", "BC", "  ", "BC", "  ", "BC", "  "],
                  ["  ", "BC", "  ", "  ", "BC", "  ", "  ", "BC"]]
    print_board(demo_board_q, "W", 1)
    wait()
    
    print("")
    print("3.5     When making these moves, the bishop, rook or queen may not move over any intervening pieces.")
    print("")
    print("3.6     The knight may move to one of the squares nearest to that on which it stands but not on the same rank, file or diagonal.")
    demo_board_n=[["  ", "  ", "  ", "  ", "  ", "BB", "BN", "BR"],
                  ["  ", "  ", "  ", "  ", "BC", "BP", "BP", "BP"],
                  ["  ", "  ", "  ", "  ", "  ", "BC", "  ", "BC"],
                  ["  ", "WC", "  ", "WC", "  ", "  ", "  ", "  "],
                  ["WC", "  ", "  ", "  ", "WC", "  ", "  ", "  "],
                  ["  ", "  ", "WN", "  ", "  ", "  ", "  ", "  "],
                  ["WC", "  ", "  ", "  ", "WC", "  ", "  ", "  "],
                  ["  ", "WC", "  ", "WC", "  ", "  ", "  ", "  "]]
    print_board(demo_board_n, "W", 1)
    wait()
    
    print("")
    print("3.7     The pawn:")
    print("\t3.7.1    The pawn may move forward to the square immediately in front of it on the same file, provided that this square is unoccupied, or")
    print("\t3.7.2    on its first move the pawn may move as in 3.7.1 or alternatively it may advance two squares along the same file, provided that both squares are unoccupied, or")
    print("\t3.7.3    the pawn may move to a square occupied by an opponent\'s piece diagonally in front of it on an adjacent file, capturing that piece.")
    demo_board_p=[["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "BP", "  "],
                  ["  ", "  ", "WC", "  ", "  ", "CC", "BC", "CC"],
                  ["  ", "CC", "WC", "CC", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "WP", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]]
    print_board(demo_board_p, "W", 2)
    wait()

    print("")
    print("\t\t3.7.3.1    A pawn occupying a square on the same rank as and on an adjacent file to an opponent\'s pawn which has just advanced two squares in one move from its original square may capture this opponent\'s pawn as though the latter had been moved only one square.")
    print("\t\t3.7.3.2    This capture is only legal on the move following this advance and is called an \'en passant\' capture.")
    demo_board_e=[["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "BP", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "CC", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "WP", "BC", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]]
    print_board(demo_board_e, "W", 3)
    wait()
    
    print("")
    print("\t\t3.7.3.3    When a player, having the move, plays a pawn to the rank furthest from its starting position, he/she must exchange that pawn as part of the same move for a new queen, rook, bishop or knight of the same colour on the intended square of arrival. This is called the square of \"promotion\".")
    print("\t\t3.7.3.4    The player\'s choice is not restricted to pieces that have been captured previously.")
    print("\t\t3.7.3.5    This exchange of a pawn for another piece is called promotion, and the effect of the new piece is immediate.")
    print("")
    print("3.8     There are two different ways of moving the king:")
    print("\t3.8.1    by moving to an adjoining square")
    demo_board_k=[["  ", "  ", "  ", "BC", "BK", "BC", "  ", "  "],
                  ["  ", "  ", "  ", "BC", "BC", "BC", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                  ["  ", "WC", "WC", "WC", "  ", "  ", "  ", "  "],
                  ["  ", "WC", "WK", "WC", "  ", "  ", "  ", "  "],
                  ["  ", "WC", "WC", "WC", "  ", "  ", "  ", "  "],
                  ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]]
    print_board(demo_board_e, "W", 2)
    wait()
    
    print("")
    print("\t3.8.2    by \'castling\'. This is a move of the king and either rook of the same colour along the player\'s first rank, counting as a single move of the king and executed as follows: the king is transferred from its original square two squares towards the rook on its original square, then that rook is transferred to the square the king has just crossed.")
    demo_board_c1=[["BR", "  ", "  ", "  ", "BK", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "WK", "  ", "  ", "WR"]]
    print_board(demo_board_c1, "W", 2)
    print("\t\tBefore white kingside castling")
    print("\t\tBefore black queenside castling")
    print("")
    
    demo_board_c2=[["  ", "  ", "BK", "BR", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "WR", "WK", "  "]]
    print_board(demo_board_c2, "W", 2)
    print("\t\tAfter white kingside castling")
    print("\t\tAfter black queenside castling")
    wait()
    print("")
    
    demo_board_c3=[["  ", "  ", "  ", "  ", "BK", "  ", "  ", "BR"],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["WR", "  ", "  ", "  ", "WK", "  ", "  ", "  "]]
    print_board(demo_board_c3, "W", 2)
    print("\t\tBefore white queenside castling")
    print("\t\tBefore black kingside castling")
    print("")
    
    demo_board_c4=[["  ", "  ", "  ", "  ", "  ", "BR", "BK", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                   ["  ", "  ", "WK", "WR", "  ", "  ", "  ", "  "]]
    print_board(demo_board_c4, "W", 2)
    print("\t\tAfter white queenside castling")
    print("\t\tAfter black kingside castling")
    wait()
    print("")
    
    print("\t\t3.8.2.1    The right to castle has been lost:")
    print("\t\t\t\t1) If the king has already moved, or")
    print("\t\t\t\t2) With a rook that has already moved.")
    print("\t\t3.8.2.2    Castling is prevented temporarily:")
    print("\t\t\t\t3) If the square on which the king stands, or the square which it must cross, or the square which it is to occupy, is attacked by one or more of the opponent\'s pieces, or")
    print("\t\t\t\t4) If there is any piece between the king and the rook with which castling is to be effected.")
    wait()
    print("")
    print("3.9     The king in check:")
    print("\t3.9.1    The king is said to be \'in check\' if it is attacked by one or more of the opponent\'s pieces, even if such pieces are constrained from moving to the square occupied by the king because they would then leave or place their own king in check.")
    print("\t3.9.2    No piece can be moved that will either expose the king of the same colour to check or leave that king in check.")
    print("")
    print("3.10   Legal and illegal moves; illegal positions:")
    print("\t3.10.1    A move is legal when all the relevant requirements of Articles 3.1–3.9 have been fulfilled.")
    print("\t3.10.2    A move is illegal when it fails to meet the relevant requirements of Articles 3.1–3.9.")
    print("\t3.10.3    A position is illegal when it cannot have been reached by any series of legal moves.")
    wait()
    

def article_4():
    """
    article_4() -> None

    Prints out the article 4 of FIDE Laws of Chess.
    """

    print("")
    print("Please note that the article 4 doesn\'t apply to this online chess game since there are no physical pieces, but it may apply in offline chess games.")
    print("")
    print("Article 4: The Act of Moving the Pieces")
    print("")
    print("4.1     Each move must be played with one hand only.")
    print("")
    print("4.2     Adjusting the pieces or other physical contact with a piece:")
    print("\t4.2.1    Only the player having the move may adjust one or more pieces on their squares, provided that he/she first expresses his/her intention (for example by saying \"j\'adoube\" or \"I adjust\").")
    print("\t4.2.2    Any other physical contact with a piece, except for clearly accidental contact, shall be considered to be intent.")
    wait()
    print("")
    print("4.3     Except as provided in Article 4.2.1, if the player having the move touches on the chessboard, with the intention of moving or capturing:")
    print("\t4.3.1    one or more of his/her own pieces, he/she must move the first piece touched that can be moved.")
    print("\t4.3.2    one or more of his/her opponent\'s pieces, he/she must capture the first piece touched that can be captured.")
    print("\t4.3.3    one or more pieces of each colour, he/she must capture the first touched opponent\'s piece with his/her first touched piece or, if this is illegal, move or capture the first piece touched that can be moved or captured. If it is unclear whether the player\'s own piece or his/her opponent\'s piece was touched first, the player\'s own piece shall be considered to have been touched before his/her opponent\'s.")
    print("")
    print("4.4     If a player having the move:")
    print("\t4.4.1    touches his/her king and a rook he/she must castle on that side if it is legal to do so.")
    print("\t4.4.2    deliberately touches a rook and then his/her king he/she is not allowed to castle on that side on that move and the situation shall be governed by Article 4.3.1.")
    print("\t4.4.3    intending to castle, touches the king and then a rook, but castling with this rook is illegal, the player must make another legal move with his/her king (which may include castling with the other rook). If the king has no legal move, the player is free to make any legal move.")
    print("\t4.4.4    promotes a pawn, the choice of the piece is finalised when the piece has touched the square of promotion.")
    wait()
    print("")
    print("4.5     If none of the pieces touched in accordance with Article 4.3 or Article 4.4 can be moved or captured, the player may make any legal move.")
    print("")
    print("4.6     The act of promotion may be performed in various ways:")
    print("\t4.6.1    the pawn does not have to be placed on the square of arrival.")
    print("\t4.6.2    removing the pawn and putting the new piece on the square of promotion may occur in any order.")
    print("\t4.6.3    If an opponent\'s piece stands on the square of promotion, it must be captured.")
    wait()
    print("")
    print("4.7     When, as a legal move or part of a legal move, a piece has been released on a square, it cannot be moved to another square on this move. The move is considered to have been made in the case of:")
    print("\t4.7.1    A capture, when the captured piece has been removed from the chessboard and the player, having placed his/her own piece on its new square, has released this capturing piece from his/her hand.")
    print("\t4.7.2    Castling, when the player\'s hand has released the rook on the square previously crossed by the king. When the player has released the king from his/her hand, the move is not yet made, but the player no longer has the right to make any move other than castling on that side, if this is legal. If castling on this side is illegal, the player must make another legal move with his/her king (which may include castling with the other rook). If the king has no legal move, the player is free to make any legal move.")
    print("\t4.7.3    Promotion, when the player\'s hand has released the new piece on the square of promotion and the pawn has been removed from the board.")
    print("")
    print("4.8     A player forfeits his/her right to claim against his/her opponent\'s violation of Articles 4.1 – 4.7 once the player touches a piece with the intention of moving or capturing it.")
    print("")
    print("4.9     If a player is unable to move the pieces, an assistant, who shall be acceptable to the arbiter, may be provided by the player to perform this operation.")
    wait()
    

def article_5():
    """
    article_5() -> None

    Prints out the article 5 of FIDE Laws of Chess.
    """

    print("")
    print("Article 5: The Completion of the Game")
    print("")
    print("\t5.1.1    The game is won by the player who has checkmated his/her opponent\'s king. This immediately ends the game, provided that the move producing the checkmate position was in accordance with Article 3 and Articles 4.2–4.7.")
    print("\t5.1.2    The game is lost by the player who declares he/she resigns (this immediately ends the game), unless the position is such that the opponent cannot checkmate the player\'s king by any possible series of legal moves. In this case the result of the game is a draw.")
    print("")
    print("\t5.2.1    The game is drawn when the player to move has no legal move and his/her king is not in check. The game is said to end in \'stalemate\'. This immediately ends the game, provided that the move producing the stalemate position was in accordance with Article 3 and Articles 4.2–4.7.")
    print("\t5.2.2    The game is drawn when a position has arisen in which neither player can checkmate the opponent’s king with any series of legal moves. The game is said to end in a \'dead position\'. This immediately ends the game, provided that the move producing the position was in accordance with Article 3 and Articles 4.2–4.7.")
    print("\t5.2.3    The game is drawn upon agreement between the two players during the game, provided both players have made at least one move. This immediately ends the game.")
    wait()
    

def initial_messages():
    """
    initial_messages() -> None

    Prints out the initial messages for the user.
    Asks the user whether to read about chess rules. If so, prints out the chess rules.
    """
    
    print("Thanks for playing chess!")
    print("Here are some information you need to know:")
    print("For each move, you need to indicate the coordinate of the piece you want to move and the coordinate of where you want to move it to.")
    print("For castling, enter your king's current position (coordinate) and your king's position after castling (coordinate).")
    print("For en passant, enter your pawn's current position (coordinate) and your pawn's position after castling (coordinate).")
    print("For pawn promotions, enter the coordinates as usual, and you will be asked to indicate which piece you want to replace the pawn.")
    print("Note that all coordinates should be separated by a space, with the row/rank number first and column/file number second. For example, \"1 7\" is a valid input.")
    wait()
    print("")
    print("At any time, if both players agreed to a draw, type \"draw\" when the program asks you for the coordinate.")
    print("Similarly, if one player resigns, type \"resign\" in the player's turn when the program asks you for the coordinate.")
    wait()
    print("")
    print("Invalid moves will be catched, and you will see \"Invalid move!\" on the screen.")
    wait()
    print("")
    print("This program uses threefold repetition rule, and there will be a draw by repetition if there is a threefold repetition without the need of claiming a draw.")
    print("This programs also uses 50-move rule, and the program will end with a draw by 50-move rule without the need of claiming a draw.")
    wait()
    print("")
    print("Would you like to learn more about chess rules? Enter yes or no.")
    response=input_yn()

    while response=="yes":
        print("Which articles do you want to see? Enter the respective number.")
        print("1. The Nature and Objectives of the Game of Chess")
        print("2. The Initial Position of the Pieces on the Chessboard")
        print("3. The Moves of the Pieces")
        print("4. The Act of Moving the Pieces")
        print("5. The Completion of the Game")
        print("6. All")
        response=input().lower().strip(".,?! ")
        
        while response not in ["1", "2", "3", "4", "5", "6"]:
            print("You can only enter 1, 2, 3, 4, 5, or 6!")
            response=input().lower().strip(".,?! ")

        if response in ["1", "6"]:
            article_1()
        if response in ["2", "6"]:
            article_2()
        if response in ["3", "6"]:
            article_3()
        if response in ["4", "6"]:
            article_4()
        if response in ["5", "6"]:
            article_5()

        print("")
        print("Do you want to view more chess rules? Enter yes or no.")
        response=input_yn()


def in_check(board, piece, side, flag):
    """
    in_check(2-D list, string, string, boolean) -> boolean

    Returns True if the piece in list's position can be attacked by side; Otherwise, returns False.
    The boolean determines whether it is necessary to modify global variables, if any.
    """

##    knight_attacks=[[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]] # Possible knight attacks
##
##    # Check for possible knight attacks
##    for attack in knight_attacks:
##        if isvalid(board, [piece[0]+attack[0], piece[1]+attack[1]], piece, side, False)==True:
##            return True
##    
##    # Check for possible horizontal attacks
##    for i in range(0, ROW):
##        if isvalid(board, [i, piece[1]], piece, side, False)==True:
##            return True
##    
##    # Check for possible vertical attacks
##    for j in range(0, COLUMN):
##        if isvalid(board, [piece[0], j], piece, side, False)==True:
##            return True
##
##    # Check for possible diagonal attacks
##    for x in range(1, min(piece[0], piece[1])+1): # Searching for attacks up and left
##        if isvalid(board, [piece[0]-x, piece[1]-x], piece, side, False)==True:
##            return True
##        
##    for x in range(1, min(ROW-piece[0], piece[1]+1)): # Searching for attacks up and right
##        if isvalid(board, [piece[0]+x, piece[1]-x], piece, side, False)==True:
##            return True
##        
##    for x in range(1, min(piece[0]+1, COLUMN-piece[1])): # Searching for attacks down and left
##        if isvalid(board, [piece[0]-x, piece[1]+x], piece, side, False)==True:
##            return True
##        
##    for x in range(1, min(ROW-piece[0], COLUMN-piece[1])): # Searching for attacks down and right
##        if isvalid(board, [piece[0]+x, piece[1]+x], piece, side, False)==True:
##            return True
##    
##    return False

    side_pieces=pieces(board, side)
    for attack_piece in side_pieces:
        if isvalid_piece(board, attack_piece, piece, side, False)==True and isvalid_move(board, attack_piece, piece, side, False)==True:
            return True
    return False


def isvalid_pawn(board, start, end, turn, flag):
    """
    isvalid_pawn(2-D list, list, list, string) -> boolean

    If the pawn move is possible, return True. Otherwise, return False.
    If the move is en_passant, modifies the global variable en_passant to True.
    If the move is a promotion, modifies the global variable promotion to True.
    If white has en passant right, modifies the global variable en_passant_right_w to True.
    If black has en passant right, modifies the global variable en_passant_right_b to True.
    The boolean determines whether it is necessary to modify global variables, if any.
    """

    global en_passant
    global promotion
    global en_passant_right_w
    global en_passant_right_b
    
    if turn=="W":
        # Pawns can't go backwards or move more than 2 rows and 1 column
        if end[0]>=start[0] or end[0]<start[0]-2 or abs(end[1]-start[1])>1:
            return False
        
        # Pawns can only move 2 rows straight at the starting point
        if start[0]-end[0]==2 and (start[0]!=6 or start[1]!=end[1]):
            return False

        # Pawns can't move forward if it is blocked
        if start[1]==end[1]:
            for i in range(end[0]+1, start[0]):
                if board[i][start[1]]!="  ":
                    return False
        
        else:

            # Check for possible en passant
            if en_passant_right_w==True and end[0]!=ROW-1 and board[end[0]+1][end[1]]=="BP":
                if flag:
                    en_passant=True

            # Pawns can't move diagonally if there is no piece there
            elif board[end[0]][end[1]]=="  ":
                return False

        # Check for possible promotion
        if end[0]==0:
            if flag:
                promotion=True

        # Modify en passant right if needed
        if start[0]-end[0]==2 and (end[1]!=COLUMN-1 and board[end[0]][end[1]+1]=="BP" or end[1]!=0 and board[end[0]][end[1]-1]=="BP"):
            if flag:
                en_passant_right_b=True
            
    else:
        # Pawns can't go backwards or move more than 2 rows and 1 column
        if end[0]<=start[0] or end[0]>start[0]+2 or abs(end[1]-start[1])>1:
            return False
        
        # Pawns can only move 2 rows straight at the starting point
        if end[0]-start[0]==2 and (start[0]!=1 or start[1]!=end[1]):
            return False

        # Pawns can't move forward if it is blocked
        if start[1]==end[1]:
            for i in range(start[0]+1, end[0]):
                if board[i][start[1]]!="  ":
                    return False
        
        else:
            # Check for possible en passant
            if en_passant_right_b==True and end[0]!=0 and board[end[0]-1][end[1]]=="WP":
                if flag:
                    en_passant=True

            # Pawns can't move diagonally if there is no piece there
            elif board[end[0]][end[1]]=="  ":
                return False

        # Check for possible promotion
        if end[0]==ROW-1:
            if flag:
                promotion=True

        # Modify en passant right if needed
        if end[0]-start[0]==2 and (end[1]!=COLUMN-1 and board[end[0]][end[1]+1]=="WP" or end[1]!=0 and board[end[0]][end[1]-1]=="WP"):
            if flag:
                en_passant_right_w=True

    return True


def isvalid_king(board, start, end, turn, flag):
    """
    isvalid_king(2-D list, list, list, string, boolean) -> boolean

    If the king move is possible, return True. Otherwise, return False.
    The boolean determines whether it is necessary to modify global variables, if any.
    """

    global castling_kw
    global castling_qw
    global castling_kb
    global castling_qb
    
    if abs(end[0]-start[0])>1 or abs(end[1]-start[1])>1: # Not in any possible move of King except castling
        # White kingside castling check
        if start==[7, 4] and end==[7, 6] and castling_right_kw==True:
            for j in range(4, 7):
                if (j!=4 and board[7][j]!="  ") or in_check(board, [7, j], "B", False)==True:
                    return False
            if flag:
                castling_kw=True
            return True

        # White queenside castling check
        elif start==[7, 4] and end==[7, 2] and castling_right_qw==True:
            for j in range(2, 5):
                if (j!=4 and board[7][j]!="  ") or in_check(board, [7, j], "B", False)==True:
                    return False
            if board[7][1]!="  ":
                return False
            if flag:
                castling_qw=True
            return True

        # Black kingside castling check
        elif start==[0, 4] and end==[0, 6] and castling_right_kb==True:
            for j in range(4, 7):
                if (j!=4 and board[0][j]!="  ") or in_check(board, [0, j], "W", False)==True:
                    return False
            if flag:
                castling_kb=True
            return True

        # Black queenside castling check
        elif start==[0, 4] and end==[0, 2] and castling_right_qb==True:
            for j in range(2, 5):
                if (j!=4 and board[0][j]!="  ") or in_check(board, [0, j], "W", False)==True:
                    return False
            if board[0][1]!="  ":
                return False
            if flag:
                castling_qb=True
            return True

        else:
            return False
            
    return True


def isvalid_knight(board, start, end, turn, flag):
    """
    isvalid_knight(2-D list, list, list, string) -> boolean

    If the knight move is possible, return True. Otherwise, return False.
    The boolean determines whether it is necessary to modify global variables, if any.
    """
    
    if abs(end[0]-start[0]) in [1, 2] and abs(end[1]-start[1]) in [1, 2]: # Not in any possible move of Knight
        return True
    
    return False


def isvalid_bishop(board, start, end, turn, flag):
    """
    isvalid_bishop(2-D list, list, list, string) -> boolean

    If the bishop move is possible, return True. Otherwise, return False.
    The boolean determines whether it is necessary to modify global variables, if any.
    """
    
    if abs(end[0]-start[0])!=abs(end[1]-start[1]): # Not in the same diagonal
        return False
    
    if start[0]<end[0]: # If moving down
        # If moving down and right
        if start[1]<end[1]:
            for increase in range(1, end[0]-start[0]):
                if board[start[0]+increase][start[1]+increase]!="  ":
                    return False

        # If moving down and left
        else:
            for increase in range(1, end[0]-start[0]):
                if board[start[0]+increase][start[1]-increase]!="  ":
                    return False
            
    else: # If moving up
        # If moving up and left
        if start[1]>end[1]:
            for increase in range(1, start[0]-end[0]):
                if board[start[0]-increase][start[1]-increase]!="  ":
                    return False

        # If moving up and right
        else:
            for increase in range(1, start[0]-end[0]):
                if board[start[0]-increase][start[1]+increase]!="  ":
                    return False
                
    return True

def isvalid_rook(board, start, end, turn, flag):
    """
    isvalid_rook(2-D list, list, list, string) -> boolean

    If the rook move is possible, return True. Otherwise, return False.
    The boolean determines whether it is necessary to modify global variables, if any.
    """
    
    if end[0]!=start[0] and end[1]!=start[1]: # Not in the same row/column
        return False
    
    # Check for possible pieces between start and end positions
    if start[0]==end[0]: # If the rook is moving horizontally
        
        if start[1]<end[1]: # If the rook is moving right, in the view of white
            for j in range(start[1]+1, end[1]): 
                if board[start[0]][j]!="  ":
                    return False
        
        else: # start[1]>end[1]: If the rook is moving left, in the view of white
            for j in range(end[1]+1, start[1]):
                if board[start[0]][j]!="  ":
                    return False
    
    else: # start[1]=end[1], if the rook is moving vertically
        
        if start[0]<end[0]: # If the rook is moving up, in the view of white
            for i in range(start[0]+1, end[0]): 
                if board[i][start[1]]!="  ":
                    return False
        
        else: # start[0]>end[0]: If the rook is moving down, in the view of white
            for i in range(end[0]+1, start[0]): 
                if board[i][start[1]]!="  ":
                    return False
                
    return True


def isvalid_queen(board, start, end, turn, flag):
    """
    isvalid_queen(2-D list, list, list, string) -> boolean

    If the queen move is possible, return True. Otherwise, return False.
    The boolean determines whether it is necessary to modify global variables, if any.
    """
    
    if isvalid_rook(board, start, end, turn, flag) or isvalid_bishop(board, start, end, turn, flag):
        return True
    return False


def isvalid_bounds(board, start, end, turn, flag):
    """
    isvalid_start(2-D list, list, list, string) -> boolean

    Returns True if nothing is out of bounds; Otherwise, return False.
    The boolean determines whether it is necessary to modify global variables, if any.
    """
    
    temp_list=[start[0], start[1], end[0], end[1]]
    for x in temp_list:
        if x<0 or x>7:
            return False
        
    return True


def isvalid_piece(board, start, end, turn, flag): 
    """
    isvalid_start(2-D list, list, list, string) -> boolean

    Returns True if the starting and end pieces are correct; Otherwise, return False.
    The boolean determines whether it is necessary to modify global variables, if any.
    """
    
    start_p=board[start[0]][start[1]]
    end_p=board[end[0]][end[1]]
    if start_p=="  ": # Can't move nothing
        return False
    
    if turn=="W":
        if start_p[0]=="B" or end_p[0]=="W": # Can't move others' pieces or take own pieces
            return False
        
    else:
        if start_p[0]=="W" or end_p[0]=="B": # Can't move others' pieces or take own pieces
            return False
        
    return True


def king_pos(board, side):
    """
    king_pos(board, side) -> list

    Returns the side's king position as a list.
    """
    
    if side=="W":
        # Search from bottom to top since the white King is usually at the bottom
        for i in range(ROW-1, -1, -1):
            for j in range(COLUMN-1, -1, -1):
                if board[i][j]=="WK":
                    return [i, j]
                
    else:
        # Search from top to bottom since the black King is usually at the top
        for i in range(ROW):
            for j in range(COLUMN):
                if board[i][j]=="BK":
                    return [i, j]


def isvalid_check(board, start, end, turn, flag):
    """
    isvalid_start(2-D list, list, list, string, boolean) -> boolean

    Returns True if the turn side is not in check after moving; Otherwise, return False.
    If after the move, the opponent King is in check, modifies the global check variable.
    The boolean determines whether it is necessary to modify global variables, if any.
    """
    global check
    
    # Creates a temporary board to mimic the move
    temp_board=copy.deepcopy(board)
    temp_board[end[0]][end[1]]=temp_board[start[0]][start[1]]
    temp_board[start[0]][start[1]]="  "
    
    if in_check(temp_board, king_pos(temp_board, turn), rev(turn), False):
        return False
    return True


def isvalid_move(board, start, end, turn, flag):
    """
    isvalid_move(2-D list, list, list, string) -> boolean

    Checks whether the piece can move to the place indicated by the arguments of this function.
    The boolean determines whether it is necessary to modify global variables, if any.
    """
    
    start_p=board[start[0]][start[1]]
    if start_p[1]=="P":
        return isvalid_pawn(board, start, end, turn, flag)
    
    elif start_p[1]=="K":
        return isvalid_king(board, start, end, turn, flag)
    
    elif start_p[1]=="N":
        return isvalid_knight(board, start, end, turn, flag)
    
    elif start_p[1]=="B":
        return isvalid_bishop(board, start, end, turn, flag)
    
    elif start_p[1]=="R":
        return isvalid_rook(board, start, end, turn, flag)
    
    else:
        return isvalid_queen(board, start, end, turn, flag)


# All functions here are under assumption that previous functions in valid_functions return True
valid_functions=[isvalid_bounds, isvalid_piece, isvalid_move, isvalid_check]


def isvalid(board, start, end, turn, flag):
    """
    isvalid(2-D list, list, list, string, boolean) -> boolean

    Checks whether a move is valid or not.
    The boolean determines whether it is necessary to modify global variables, if any.
    """
    
    for function in valid_functions:
        if function(board, start, end, turn, flag)==False:
            return False
    return True


def rep_w(board):
    """
    rep_w(2-D list) -> int/None

    If the board is same as one of boards stored in rep_boards_w, return the index.
    Otherwise, return None.
    """
    
    for i in range(len(rep_boards_w)):
        if rep_boards_w[i]==board:
            return i
        
    return None


def rep_b(board):
    """
    rep_w(2-D list) -> int/None

    If the board is same as one of boards stored in rep_boards_b, return the index.
    Otherwise, return None.
    """

    for i in range(len(rep_boards_b)):
        if rep_boards_b[i]==board:
            return i
        
    return None


def pieces(board, side):
    """
    pieces(board, side) -> list

    Returns the side's pieces.
    """
    
    list_pieces=[]
    for i in range(ROW):
        for j in range(COLUMN):
            if board[i][j][0]==side:
                list_pieces.append([i, j])
                
    return list_pieces

                
def is_nomove(board, side): # Algorithm updates?
    """
    is_nomove(2-D list, string) -> boolean

    If the string side don't have any legal moves, return True. Otherwise, return False.
    """
    
    list_pieces=pieces(board, side)
    for piece in list_pieces:
        for i in range(ROW):
            for j in range(COLUMN):
                if isvalid(board, piece, [i, j], side, False):
                    return False
                
    return True


def no_material(board, side):
    """
    no_material(2-D list, string) -> string

    Returns True if the string's side has insufficient material. Otherwise, return False.
    """
    
    piece="  "

    # Loop through the board to see whether side has more than 1 piece except King
    for i in range(ROW):
        for j in range(COLUMN):
            if board[i][j]!="  " and board[i][j][1]!="K" and board[i][j][0]==side:
                if piece!="  ":
                    return False
                piece=board[i][j]

    # If the piece is knight, bishop, or nothing, insufficient material occurs.
    if piece[1]=="N" or piece[1]=="B" or piece=="  ":
        return True
    
    return False

    
def status(board, turn):
    """
    status(board, turn) -> string

    If white won, returns "W".
    If black won, returns "B".
    If there is a draw, returns "D" along with explanation of drawing.
    If the game doesn't end, returns "G".
    """
    
    # Draw checks
    if draw_count==50:
        return "D-50"
    
    if rep_counts_w is not None:
        if max(rep_counts_w, default=0)>=3:
            return "D-R"
    if rep_counts_b is not None:
        if max(rep_counts_b, default=0)>=3:
            return "D-R"
    
    if no_material(board, "W") and no_material(board, "B"):
        return "D-I"

    # If no legal moves are possible
    if is_nomove(board, rev(turn)):
        if in_check(board, king_pos(board, rev(turn)), turn, False):
            return turn
        return "D-S"
    return "G"


def clear_rep():
    """
    clear_rep() -> None

    Clears all repetition boards and counts.
    """
    
    global rep_boards_w
    global rep_counts_w
    global rep_boards_b
    global rep_counts_b
    
    rep_boards_w=[]
    rep_counts_w=[]
    rep_boards_b=[]
    rep_counts_b=[]


def to_cor_x(x):
    """
    to_cor_x(int) -> string

    Returns the algebraic notation for row/rank x.
    """
    
    return str(8-x)


def to_cor_y(y):
    """
    to_cor_x(int) -> string

    Returns the algebraic notation for column/file x.
    """
    
    return chr(y+97)


def dup(board, start, end, turn):
    """
    dup(2-D list, list, list, string) -> string/None

    If their is another piece same as the second list (coordinate form) on the 2-D list and can legally move to the third list (coordinate form), return the algebraic notation needed.
    Otherwise, return None.
    """
    
    start_p=board[start[0]][start[1]]
    for i in range(ROW):
        for j in range(COLUMN):
            if (i!=start[0] or j!=start[1]) and board[i][j]==board[start[0]][start[1]]:
                if isvalid(board, [i, j], end, turn, False):
                    if j!=start[1]:
                        return to_cor_y(j)
                    else:
                        return to_cor_x(i)
                else:
                    return None

    
def game_log(board, start, end, turn):
    """
    game_log(2-D list, list, list, string) -> string

    Returns the algebraic notation needed to be added to the global log string.
    """
    
    start_p=board[start[0]][start[1]]
    end_p=board[end[0]][end[1]]
    s=""

    # Kingside castling
    if castling_kw==True or castling_kb==True:
        s="O-O"

    # Queenside castling
    elif castling_qw==True or castling_qb==True:
        s="O-O-O"

    # Pawn movements
    elif start_p[1]=="P":
        s+=""
        if end_p!="  " or en_passant==True:
            s+=to_cor_y(start[1])+"x"
        s+=to_cor_y(end[1])+to_cor_x(end[0])

    # Other pieces movements
    else:
        s+=start_p[1]
        temp=dup(board, start, end, turn)
        if temp is not None:
            s+=temp
        if end_p!="  ":
            s+="x"
        s+=to_cor_y(end[1])+to_cor_x(end[0])

    return s


def game_log_f(board, start, end, turn):
    """
    game_log_f(2-D list, list, list, string) -> string

    Returns the figurine algebraic notation needed to be added to the global log_f string.
    """
    
    s=game_log(board, start, end, turn)
    
    # If no change is needed
    if s[0] not in ["N", "B", "Q", "K", "R"]:
        return s

    # If change is needed
    piece=to_graph_piece(turn+s[0])
    s=s[1:]
    
    return piece+s


if __name__=="__main__":
    initial_messages()
    print_board(board, turn, INDENT)

    # Note: No break statements is used because once the game ends, end_game() is activated, and the program will exit using exit() after this function ends.
    while True:
        # Prints out whose turn it is
        if turn=="W":
            print("White's turn!")
        else:
            print("Black's turn!")

        # Asks user for input of coordinates
        print("Input the coordinate of the piece you want to move from, separated by a space:")
        start=input_two_numbers_int()
        print("Input the coordinate of the piece you want to move to, separated by a space:")
        end=input_two_numbers_int()

        if isvalid(board, start, end, turn, True):

            # Add the number of full moves and add it to the logs
            if turn=="W":
                count+=1
                log+=str(count)+"."
                log_f+=str(count)+"."
        
            # Modify castling rights
            if start==[7, 4] and (castling_right_kw==True or castling_right_qw==True):
                clear_rep()
                castling_right_kw=False
                castling_right_qw=False
            
            if start==[7, 7] and castling_right_kw==True:
                castling_right_kw=False
                clear_rep()
            
            if start==[7, 0] and castling_right_qw==True:
                castling_right_qw=False
                clear_rep()
            
            if start==[0, 4] and (castling_right_kb==True or castling_right_qb==True):
                castling_right_kb=False
                castling_right_qb=False
                clear_rep()
            
            if start==[0, 7] and castling_right_kb==True:
                castling_right_kb=False
                clear_rep()
            
            if start==[0, 0] and castling_right_qb==True:
                castling_right_qb=False
                clear_rep()
        
            # Modify draw variables
            if board[end[0]][end[1]]!="  " or board[start[0]][start[1]][1]=="P":
                draw_count=0
                clear_rep()
            else:
                draw_count+=1

            # Modify logs
            log+=game_log(board, start, end, turn)
            log_f+=game_log_f(board, start, end, turn)
        
            # Move pieces
            board[end[0]][end[1]]=board[start[0]][start[1]]
            board[start[0]][start[1]]="  "

            # Check for promotion
            if promotion==True:
            
                # Asks the user for piece
                print("Which piece do you want the pawn promote to?")
                print("Enter R for rook, N for knight, B for bishop, and Q for queen.")
                response=input().upper().strip(",.!? ")
                while response not in ["R", "N", "B", "Q"]:
                    print("You can only choose between rook, knight, bishop, and queen!")
                    print("Enter R for rook, N for knight, B for bishop, and Q for queen.")
                    response=input().upper().strip(",.!? ")

                # Update the board and logs
                board[end[0]][end[1]]=turn+response
                log+="="+response
                log_f+="="+to_graph_piece(turn+response)

                # Reset
                promotion=False

            # Check for en passant
            if en_passant==True:
            
                # Update boards
                if turn=="W":
                    board[end[0]+1][end[1]]="  "
                else:
                    board[end[0]-1][end[1]]="  "

                # Reset
                en_passant=False

            # Check for castling
            if castling_kw==True:
                board[7][5]="WR"
                board[7][7]="  "
                castling_kw=False

            if castling_qw==True:
                board[7][3]="WR"
                board[7][0]="  "
                castling_qw=False

            if castling_kb==True:
                board[0][5]="BR"
                board[0][7]="  "
                castling_kb=False

            if castling_qb==True:
                board[0][3]="BR"
                board[0][0]="  "
                castling_qb=False
            
            # Remove en passant rights if one move has passed
            if turn=="W" and en_passant_right_w==True:
                en_passant_right_w=False
                clear_rep()
            if turn=="B" and en_passant_right_b==True:
                en_passant_right_b=False
                clear_rep()

            # Store boards
            prev_boards.append(copy.deepcopy(board))
            if turn=="W":
                index=rep_w(board)
                if index is not None:
                    rep_counts_w[index]+=1
                else:
                    rep_boards_w.append(copy.deepcopy(board))
                    rep_counts_w.append(1)
        
            else:
                index=rep_b(board)
                if index is not None:
                    rep_counts_b[index]+=1
                else:
                    rep_boards_b.append(copy.deepcopy(board))
                    rep_counts_b.append(1)

            # Do further modification of logs, (+ and space)
            if in_check(board, king_pos(board, rev(turn)), turn, False):
                log+="+"
                log_f+="+"
        
            log+=" "
            log_f+=" "

            # Print out board before ending game
            print_board(board, rev(turn), INDENT)
        
            # Check whether game ends
            temp=status(board, turn)
            if temp=="W":
                print("White won by checkmate!")
                log=log[:-2]
                log_f=log_f[:-2]
                log+="# 1-0"
                log_f+="# 1-0"
        
            elif temp=="B":
                print("Black won by checkmate!")
                log=log[:-2]
                log_f=log_f[:-2]
                log+="# 0-1"
                log_f+="# 0-1"
        
            elif temp=="D-50":
                print("Draw by 50-move rule!")
                log, log_f=draw()
        
            elif temp=="D-R":
                print("Draw by threefold repetition!")
                log, log_f=draw()
        
            elif temp=="D-S":
                print("Draw by stalemate!")
                log, log_f=draw()
        
            elif temp=="D-I":
                print("Draw by insufficient material!")
                log, log_f=draw()
        
            if temp!="G":
                end_game()
        
            # Switch turns
            if turn=="W":
                turn="B"
            else:
                turn="W"
        
        else:
            print("Invalid Move!")

            # Remove the possible side effects of isvalid_pawn and isvalid_check.
            en_passant=False
            promotion=False
            check=False
            if turn=="W":
                en_passant_right_b=False
            else:
                en_passant_right_w=False

            # Print out board again for user to check
            print_board(board, turn, INDENT)
    


