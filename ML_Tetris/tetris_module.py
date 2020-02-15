import random

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
YELLOW = (155, 155, 0)
LIGHTYELLOW = (175, 175, 20)
CYAN = (0, 185, 185)
LIGHTCYAN = (0, 255, 255)
MAGENTA = (185, 0, 185)
LIGHTMAGENTA = (255, 0, 255)
ORANGE = (255, 128, 0)
PURPLE = (128 ,0 ,255)

# Define costants for teh gui
BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (GRAY, BLUE, GREEN, RED, YELLOW, CYAN, MAGENTA, ORANGE, PURPLE)
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
    'T': T_SHAPE_TEMPLATE
}

PIECES_COLORS = {
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE,
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE
}

def get_new_piece():
    ### restituisce un pezzo random con colorazione random
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    new_piece = {
        'shape': shape,
        'rotation': random.randint(0,len(PIECES[shape]) - 1),
        'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
        'y': -2,  # start it above the board (i.e. less than 0)
        #'color': random.randint(1,len(COLORS) - 1)
        'color': PIECES_COLORS[shape].value()
    }
    return new_piece

