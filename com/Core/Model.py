# Import dell librerie
import random
import pyautogui

# Define settings and constants
pyautogui.PAUSE = 0.03
pyautogui.FAILSAFE = True

DeepLines = 0
pause = False
APPNAME = "DiscoTetris"
MEDIAPATH = "com/raw/"
#MEDIAPATH = "C://Users/matti/PyCharmProjects/DiscoTetris/com/raw/"
FPS = 50  ### framerate del gioco (PAL 50FPS)
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20  ### Dimensione singolo blocco
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '0'
MOVESIDEWAYSFREQ = 0.075  ### frequenza di movimento laterale
# MOVEDOWNFREQ = 0.05         ### frequenza di discesa
MOVEDOWNFREQ = 1
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

# Define learning parameters

MAX_GAMES = 1

# weights = [-1, -1, -1, -30]  # Initial weight vector
# weights = [-0.0009, -0.0292, -0.7492, -99.2209]  # Best weight record

weights = [1.8, 1.0, 0.5, 0.02, 0.01, 0.2, 0.3]

# Define Color triplets in RGB
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = (0, 155, 0)
LIGHTGREEN = (20, 175, 20)
BLUE = (0, 0, 155)
LIGHTBLUE = (20, 20, 175)
YELLOW = (255, 255, 0)
LIGHTYELLOW = (175, 175, 20)
CYAN = (0, 185, 185)
LIGHTCYAN = (0, 255, 255)
MAGENTA = (185, 0, 185)
LIGHTMAGENTA = (255, 0, 255)
ORANGE = (255, 128, 0)
PURPLE = (128, 0, 255)

# Define costants for teh gui
BORDERCOLOR = WHITE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
# COLORS = (GRAY, BLUE, GREEN, RED, YELLOW, CYAN, MAGENTA, ORANGE, PURPLE)
COLORS = {
    1: GRAY,
    2: BLUE,
    3: GREEN,
    4: RED,
    5: YELLOW,
    6: CYAN,
    7: MAGENTA,
    8: ORANGE,
    9: PURPLE}
LIGHTCOLORS = (WHITE, LIGHTBLUE, WHITE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW,
               LIGHTCYAN, LIGHTMAGENTA)

# set dimensioni del Template
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5
BOARDWIDTH = 10

S_SHAPE_TEMPLATE = [['00000', '00000', '00110', '01100', '00000'],
                    ['00000', '00100', '00110', '00010', '00000']]

Z_SHAPE_TEMPLATE = [['00000', '00000', '01100', '00110', '00000'],
                    ['00000', '00100', '01100', '01000', '00000']]

I_SHAPE_TEMPLATE = [['00100', '00100', '00100', '00100', '00000'],
                    ['00000', '00000', '11110', '00000', '00000']]

O_SHAPE_TEMPLATE = [['00000', '00000', '01100', '01100', '00000']]

J_SHAPE_TEMPLATE = [['00000', '01000', '01110', '00000', '00000'],
                    ['00000', '00110', '00100', '00100', '00000'],
                    ['00000', '00000', '01110', '00010', '00000'],
                    ['00000', '00100', '00100', '01100', '00000']]

L_SHAPE_TEMPLATE = [['00000', '00010', '01110', '00000', '00000'],
                    ['00000', '00100', '00100', '00110', '00000'],
                    ['00000', '00000', '01110', '01000', '00000'],
                    ['00000', '01100', '00100', '00100', '00000']]

T_SHAPE_TEMPLATE = [['00000', '00100', '01110', '00000', '00000'],
                    ['00000', '00100', '00110', '00100', '00000'],
                    ['00000', '00000', '01110', '00100', '00000'],
                    ['00000', '00100', '01100', '00100', '00000']]

PIECES = {
    'S': S_SHAPE_TEMPLATE,
    'Z': Z_SHAPE_TEMPLATE,
    'J': J_SHAPE_TEMPLATE,
    'L': L_SHAPE_TEMPLATE,
    'I': I_SHAPE_TEMPLATE,
    'O': O_SHAPE_TEMPLATE,
    'T': T_SHAPE_TEMPLATE,
}

PIECES_COLORS = {
    'S': 3,  # GREEN
    'Z': 4,  # RED
    'J': 2,  # BLUE
    'L': 8,  # ORANGE
    'I': 6,  # CYAN
    'O': 5,  # YELLOW
    'T': 9   # PURPLE
}


def add_to_board(board, piece):
    ### riempie nella board il tetramino nella locazione definita
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK and x + piece['x'] < 10 and y + piece['y'] < 20:
                board[x + piece['x']][y + piece['y']] = piece['color']
                # DEBUGGING NOTE: SOMETIMES THIS IF STATEMENT ISN'T
                # SATISFIED, WHICH NORMALLY WOULD RAISE AN ERROR.
                # NOT SURE WHAT CAUSES THE INDICES TO BE THAT HIGH.
                # THIS IS A BAND-AID FIX


def is_on_board(x, y):
    ### Verifica la presenza delle coordinate nella tupla (x,y) all'interno dei limiti dell board
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def is_valid_position(board, piece, adj_x=0, adj_y=0):
    ### Verifica la validità della posizione che si vuole fornire al tetramino corrente (interno all board e senza collisioni)
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            is_above_board = y + piece['y'] + adj_y < 0
            if is_above_board or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not is_on_board(x + piece['x'] + adj_x, y + piece['y'] + adj_y):
                return False  # The piece is off the board
            if board[x + piece['x'] + adj_x][y + piece['y'] + adj_y] != BLANK:
                return False  # The piece collides
    return True


def is_complete_line(board, y):
    ### Funzione booleana che restituisce True se la linea di altezza y è compleata, altrimenti restituisce false
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def get_level_and_fall_freq(score):
    ### Calcola il livello del gioco in base a una funzione :  int(score / 10) + 1 e calcola quanti secondi passano per il drop
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 1000) + 1
    # fall_freq = 0.07 * math.exp((1 - level) / 3)  # 0.27 - (level * 0.02) default
    multiplier = level * 0.1
    fall_freq = 0.27 - (multiplier * 0.02)
    # fall_freq =  0.27 - (level * 0.02)
    return level, fall_freq


def get_new_piece():
    ### restituisce un pezzo random con colorazione random
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    new_piece = {
        'shape': shape,
        'rotation': random.randint(0, len(PIECES[shape]) - 1),
        'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
        'y': -2,  # start it above the board (i.e. less than 0)
        # 'color': random.randint(1,len(COLORS) - 1)
        'color': PIECES_COLORS[shape]
    }
    return new_piece


def get_score(lines, level):
    # setting the multiplier
    multiplier = 1
    if level >= 25 and level < 50:
        multiplier = 2
    elif level >= 50:
        multiplier = 3

    # score per lines removed
    if lines == 0:
        return 0
    elif lines == 1:
        return int(40 * multiplier)
    elif lines == 2:
        return int(100 * multiplier)
    elif lines == 3:
        return int(300 * multiplier)
    elif lines == 4:
        return int(1200 * multiplier)


def remove_complete_lines(board):
    ### Rimuove ogni linea completata, sposta tutto in basso di una riga e restituisce il numero di linee completate
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    lines_removed = 0
    y = BOARDHEIGHT - 1  # start y at the bottom of the board
    while y >= 0:
        if is_complete_line(board, y):
            # Remove the line and pull boxes down by one line.
            for pull_down_y in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pull_down_y] = board[x][pull_down_y - 1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            lines_removed += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1  # move on to check next row up
    return lines_removed, board