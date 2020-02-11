
# Import dell librerie
import random
import time
import pygame
import sys
import math
import copy
import numpy
import matplotlib.pyplot as plt
import pygame.locals as keys
import pyautogui

# Define settings and constants
pyautogui.PAUSE = 0.03
pyautogui.FAILSAFE = True

pause = False
APPNAME = "DiscoTetris"
MEDIAPATH = "Media/"
FPS = 50                    ### framerate del gioco (PAL 50FPS)
WINDOWWIDTH = 640
WINDOWHEIGHT = 480          
BOXSIZE = 20                ### Dimensione singolo blocco                       
BOARDWIDTH = 10
BOARDHEIGHT = 20                                                                        
BLANK = '0'
MOVESIDEWAYSFREQ = 0.075    ### frequenza di movimento laterale
MOVEDOWNFREQ = 0.05         ### frequenza di discesa

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

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

# impostazione delle variabili costatnti per le componenti del gioco
BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (GRAY, BLUE, GRAY, GREEN, RED, YELLOW, CYAN, MAGENTA)
LIGHTCOLORS = (WHITE, LIGHTBLUE, WHITE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW,
               LIGHTCYAN, LIGHTMAGENTA)

# set dimensioni del Template
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['00000', '00000', '00110', '01100', '00000'],
                    ['00000', '00100', '00110', '00010', '00000']]

Z_SHAPE_TEMPLATE = [['00000', '00000', '01100', '00110', '00000'],
                    ['00000', '00100', '01100', '01000', '00000']]

I_SHAPE_TEMPLATE = [['00100', '00100', '00100', '00100', '00000'],
                    ['00000', '00000', '11110', '00000', '00000']]

O_SHAPE_TEMPLATE = [['00000', '00000', '01100', '01100', '00000']]

J_SHAPE_TEMPLATE = [['00000', '01000', '01110', '00000',
                     '00000'], ['00000', '00110', '00100', '00100', '00000'],
                    ['00000', '00000', '01110', '00010',
                     '00000'], ['00000', '00100', '00100', '01100', '00000']]
L_SHAPE_TEMPLATE = [['00000', '00010', '01110', '00000',
                     '00000'], ['00000', '00100', '00100', '00110', '00000'],
                    ['00000', '00000', '01110', '01000',
                     '00000'], ['00000', '01100', '00100', '00100', '00000']]

T_SHAPE_TEMPLATE = [['00000', '00100', '01110', '00000',
                     '00000'], ['00000', '00100', '00110', '00100', '00000'],
                    ['00000', '00000', '01110', '00100',
                     '00000'], ['00000', '00100', '01100', '00100', '00000']]

PIECES = {
    'S': S_SHAPE_TEMPLATE,
    'Z': Z_SHAPE_TEMPLATE,
    'J': J_SHAPE_TEMPLATE,
    'L': L_SHAPE_TEMPLATE,
    'I': I_SHAPE_TEMPLATE,
    'O': O_SHAPE_TEMPLATE,
    'T': T_SHAPE_TEMPLATE
}

# Define learning parameters
alpha = 0.01
gamma = 0.9
MAX_GAMES = 100
explore_change = 0.5
weights = [-1, -1, -1, -30]  # Initial weight vector
# weights = [-0.0015, -0.00046, -0.0101, -99.9841] #400 Score
# weights = [-0.0009, -0.0292, -0.7492, -99.2209] #489 Score

 ##########################################################  CODE ZONE  #############################################################

def run_game(weights, explore_change):
    global pause
    """Runs a full game of tetris, learning and updating the policy as the game progresses.

    Arguments:
        weights {list} -- list of four floats, defining the piece placement policy and denoting the respective weighting
                          of the four features:
                            * Sum of all column heights
                            * Sum of absolute column differences
                            * Maximum height on the board
                            * Number of holes on the board
        explore_change {float} -- A float between 0 and 1 which determines the probability that a random move will be
                                   selected instead of the best move per the current policy.

    Returns:
        score {int} -- The integer score of the finished game.
        weights {list} -- The same list as the argument, piped to allow for persistent learning across games.
        explore_change {float} -- The same parameter as the input argument, piped to allow for persistent learning
                                    across games.
    """

    # setup variables for the start of the game
    board = get_blank_board()
    last_move_down_time = time.time()
    last_lateral_time = time.time()
    last_fall_time = time.time()
    moving_down = False  # note: there is no movingUp variable
    moving_left = False
    moving_right = False
    score = 0
    one_step_reward = 0
    games_completed = 0
    level, fall_freq = get_level_and_fall_freq(score)
    current_move = [0, 0]  # Relative Rotation, lateral movement
    falling_piece = get_new_piece()
    next_piece = get_new_piece()

    while True:  # game loop

        if falling_piece is None:
            # No falling piece in play, so start a new piece at the top
            falling_piece = next_piece
            next_piece = get_new_piece()
            last_fall_time = time.time()  # reset last_fall_time

            if not is_valid_position(board, falling_piece):
                # can't fit a new piece on the board, so game over
                return score, weights, explore_change
            current_move, weights = gradient_descent(board, falling_piece, weights, explore_change) ### Ottiene la mossa dall'IA
            if explore_change > 0.001:
                explore_change = explore_change * 0.99
            else:
                explore_change = 0
        check_for_quit()
        current_move = make_move(current_move)
        for event in pygame.event.get():  # event handling loop
            if not pygame.key.get_focused():
                paused()
            elif event.type == keys.KEYUP:
                if (event.key == keys.K_p):
                    # Pausing the game
                    paused()
                    last_fall_time = time.time()
                    last_move_down_time = time.time()
                    last_lateral_time = time.time()
                elif (event.key == keys.K_LEFT or event.key == keys.K_a):
                    moving_left = False
                elif (event.key == keys.K_RIGHT or event.key == keys.K_d):
                    moving_right = False
                elif (event.key == keys.K_DOWN or event.key == keys.K_s):
                    moving_down = False

            elif event.type == keys.KEYDOWN:
                # moving the piece sideways
                if (event.key == keys.K_LEFT or event.key == keys.K_a) and is_valid_position(
                            board, falling_piece, adj_x=-1):
                    falling_piece['x'] -= 1
                    moving_left = True
                    moving_right = False
                    last_lateral_time = time.time()

                elif (event.key == keys.K_RIGHT or event.key == keys.K_d) and is_valid_position(
                          board, falling_piece, adj_x=1):
                    falling_piece['x'] += 1
                    moving_right = True
                    moving_left = False
                    last_lateral_time = time.time()

                # rotating the piece (if there is room to rotate)
                elif (event.key == keys.K_UP or event.key == keys.K_w):
                    falling_piece[
                        'rotation'] = (falling_piece['rotation'] + 1) % len(
                            PIECES[falling_piece['shape']])
                    if not is_valid_position(board, falling_piece):
                        falling_piece[
                            'rotation'] = (falling_piece['rotation'] - 1) % len(
                                PIECES[falling_piece['shape']])
                elif (event.key == keys.K_q):  # rotate the other direction
                    falling_piece[
                        'rotation'] = (falling_piece['rotation'] - 1) % len(
                            PIECES[falling_piece['shape']])
                    if not is_valid_position(board, falling_piece):
                        falling_piece[
                            'rotation'] = (falling_piece['rotation'] + 1) % len(
                                PIECES[falling_piece['shape']])

                # making the piece fall faster with the down key
                elif (event.key == keys.K_DOWN or event.key == keys.K_s):
                    moving_down = True
                    if is_valid_position(board, falling_piece, adj_y=1):
                        falling_piece['y'] += 1
                    last_move_down_time = time.time()

                # move the current piece all the way down
                elif event.key == keys.K_SPACE:
                    moving_down = False
                    moving_left = False
                    moving_right = False
                    for i in range(1, BOARDHEIGHT):
                        if not is_valid_position(board, falling_piece, adj_y=i):
                            break
                    falling_piece['y'] += i - 1

        # handle moving the piece because of user input
        if (moving_left or moving_right) and time.time() - last_lateral_time > MOVESIDEWAYSFREQ:
            if moving_left and is_valid_position(board, falling_piece, adj_x=-1):
                falling_piece['x'] -= 1
            elif moving_right and is_valid_position(board, falling_piece, adj_x=1):
                falling_piece['x'] += 1
            last_lateral_time = time.time()

        if moving_down and time.time(
        ) - last_move_down_time > MOVEDOWNFREQ and is_valid_position(
                board, falling_piece, adj_y=1):
            falling_piece['y'] += 1
            last_move_down_time = time.time()
            games_completed += 1

        # let the piece fall if it is time to fall
        if time.time() - last_fall_time > fall_freq:
            # see if the piece has landed
            if not is_valid_position(board, falling_piece, adj_y=1):
                # falling piece has landed, set it on the board
                add_to_board(board, falling_piece)

                #count = count_full_lines(board)
                #if count>0:
                #    print("count = ",count)

                lines, board = remove_complete_lines(board)
                score += lines * lines
                level, fall_freq = get_level_and_fall_freq(score)
                falling_piece = None
            else:
                # piece did not land, just move the piece down
                falling_piece['y'] += 1
                last_fall_time = time.time()
                games_completed += 1
        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        draw_board(board)
        draw_status(score, level, current_move)
        draw_next_piece(next_piece)
        if falling_piece is not None:
            draw_piece(falling_piece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def make_text_objs(text, font, color):
    ### Crea un oggetto testo definendone il colore e il font    
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    ### Termina il gioco chiudendo pygame e l'applicazione
    try:
        pygame.quit()
        sys.exit()
    except:
        print("Ended")


def check_for_key_press():
    ### Verifica la pressione di un tasto
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    check_for_quit()

    for event in pygame.event.get([keys.KEYDOWN, keys.KEYUP]):
        if event.type == keys.KEYDOWN:
            continue
        return event.key
    return None


def show_text_screen(text):
    ### Splash Screen introduttiva e della pausa
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    title_surf, title_rect = make_text_objs(text, BIGFONT, TEXTSHADOWCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(title_surf, title_rect)

    # Draw the text
    title_surf, title_rect = make_text_objs(text, BIGFONT, TEXTCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(title_surf, title_rect)

    # Draw the additional "Press a key to play." text.
    press_key_surf, press_key_rect = make_text_objs('Loading a new Dance !',
                                                    BASICFONT, TEXTCOLOR)
    press_key_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(press_key_surf, press_key_rect)

    pygame.display.update()
    FPSCLOCK.tick() ### Avanza al frame successivo
    time.sleep(0.5)


def check_for_quit():
    ### Interrompe il gioco quando viene premuto il tasto 'ESC' e poi cose con UPKEY (?)
    for event in pygame.event.get(keys.QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(keys.KEYUP):  # get all the KEYUP events
        if event.key == keys.K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back

def paused():
    global pause
    pygame.mixer.music.pause()
    print("************************* Start PAUSE ************************")
    #DISPLAYSURF.fill(BGCOLOR)
    show_text_screen('Paused')  # pause until a key press
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == keys.KEYUP:
                if (event.key == keys.K_p):
                    pygame.mixer.music.unpause()
                    pause = False       
    print("************************* End PAUSE **************************")

def get_level_and_fall_freq(score):
    ### Calcola il livello del gioco in base a una funzione :  int(score / 10) + 1 e calcola quanti secondi passano per il drop
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 10) + 1
    fall_freq = 0.07 * math.exp(
        (1 - level) / 3)  # 0.27 - (level * 0.02) default
    return level, fall_freq


def get_new_piece():
    ### restituisce un pezzo random con colorazione random
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    new_piece = {
        'shape': shape,
        'rotation': random.randint(0,
                                   len(PIECES[shape]) - 1),
        'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
        'y': -2,  # start it above the board (i.e. less than 0)
        'color': random.randint(1,len(COLORS) - 1)
        
        #// Implementare assegnazione statica dei colori in base alla forma

    }
    return new_piece

# (DISCO MODE - ON)   SELEZIONA UN COLORE COMPLEATAMENTE A MotherFucker RANDOM
def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

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
                  
def get_blank_board():                                                                                                                  
    ### Restituisco una matrice (Array of Array) di celle vuote '0'
    # create and return a new blank board data structure
    board = []
    for _ in range(BOARDWIDTH):
        board.append(['0'] * BOARDHEIGHT)
    return board

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

def convert_to_pixel_coords(boxx, boxy):
    ### Converte le coordinate xy della board nelle corrispettive coordinate xy della loro locazione sullo schermo 
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def draw_box(boxx, boxy, color, pixelx=None, pixely=None):
    ### Disegna ogni singolo blocco (ogni tetramino ha 4 blocchi) alle coordinate xy della board. 
    ### Se pixelx & pixely sono avvalorati disegna quel pixel (next tetramino)
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx is None and pixely is None:
        pixelx, pixely = convert_to_pixel_coords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, random_color(), #COLORS[color],
                     (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, random_color(), #LIGHTCOLORS[color],
                     (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def draw_board(board):
    ### Disegna la board costrunendone il bordo, sfondo e le singole box (pixel) dei tetramini
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, random_color(),#BORDERCOLOR,
                     (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8,
                      (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(
        DISPLAYSURF, BGCOLOR, #random_color()
        (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            draw_box(x, y, board[x][y])

def draw_status(score, level, best_move):
    ### Scrive le informazioni di gioco sullo schermo
    # draw the score text
    randCol = random_color()
    score_surf = BASICFONT.render('Score: %s' % score, True, randCol)#TEXTCOLOR)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(score_surf, score_rect)

    # draw the level text
    level_surf = BASICFONT.render('Level: %s' % level, True, randCol)#TEXTCOLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(level_surf, level_rect)

    # draw the best_move text
    move_surf = BASICFONT.render('Current Move: %s' % best_move, True, randCol)#TEXTCOLOR)
    move_rect = move_surf.get_rect()
    move_rect.topleft = (WINDOWWIDTH - 200, 80)
    DISPLAYSURF.blit(move_surf, move_rect)

def draw_piece(piece, pixelx=None, pixely=None):
    ### disegna un pezzo. Se pixelx e pixely non sono avvalorate usa le coordinate contenute in piece
    shape_to_draw = PIECES[piece['shape']][piece['rotation']]
    if pixelx is None and pixely is None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convert_to_pixel_coords(piece['x'], piece['y'])

    ### Disegna ogni box che compone il pezzo che vuole disegnare
    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shape_to_draw[y][x] != BLANK:
                draw_box(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def draw_next_piece(piece):
    ### Disegan il prossimo tetramino sulla sideBar
    # draw the "next" text
    randCol = random_color()
    next_surf = BASICFONT.render('Next Tetromino:', True, randCol)#TEXTCOLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOWWIDTH - 180, 160)
    DISPLAYSURF.blit(next_surf, next_rect)

    pygame.draw.rect(DISPLAYSURF, randCol,
                    (485, 195, 
                    (4.2 * BOXSIZE) + 8,(4.2 * BOXSIZE) + 8), 5)

    # draw the "next" piece
    draw_piece(piece, pixelx=WINDOWWIDTH - 150, pixely=200)

def get_parametersOLd(board):
    ### Calcola le metriche "MaxAltezza", "Buchi", "Somma altezze Colonne", diff_sum,
    # This function will calculate different parameters of the current board

    # Initialize some stuff
    heights = [0]*BOARDWIDTH
    diffs = [0]*(BOARDWIDTH-1)
    holes = 0
    diff_sum = 0

    # Calculate the maximum height of each column
    for i in range(0, BOARDWIDTH):  # Select a column
        for j in range(0, BOARDHEIGHT):  # Search down starting from the top of the board
            if int(board[i][j]) > 0:  # Is the cell occupied?
                heights[i] = BOARDHEIGHT - j  # Store the height value
                break

    # Calculate the difference in heights
    for i in range(0, len(diffs)):
        diffs[i] = heights[i + 1] - heights[i]
    #print("diffs ",diffs)

    # Calculate the maximum height
    max_height = max(heights)

    # Count the number of holes
    for i in range(0, BOARDWIDTH):
        occupied = 0  # Set the 'Occupied' flag to 0 for each new column
        for j in range(0, BOARDHEIGHT):  # Scan from top to bottom
            if int(board[i][j]) > 0:
                occupied = 1  # If a block is found, set the 'Occupied' flag to 1
            if int(board[i][j]) == 0 and occupied == 1:
                holes += 1  # If a hole is found, add one to the count

    height_sum = sum(heights)
    for i in diffs:
        diff_sum += abs(i)

    #print("================== Metrics ==================")
    #print("height_sum ",height_sum)
    #print("diff_sum ",diff_sum)
    #print("max_height ",max_height)
    #print("holes ",holes)

    return height_sum, diff_sum, max_height, holes

def get_parameters(board):
    ### Calcola le metriche "MaxAltezza", "Buchi", "Somma altezze Colonne", diff_sum,
    # This function will calculate different parameters of the current board

    # Initialize some stuff
    heights = [0]*BOARDWIDTH
    diffs = [0]*(BOARDWIDTH-1)
    holes = 0
    diff_sum = 0

    # Calculate the maximum height of each column
    for i in range(0, BOARDWIDTH):  # Select a column
        for j in range(0, BOARDHEIGHT):  # Search down starting from the top of the board
            if int(board[i][j]) > 0:  # Is the cell occupied?
                heights[i] = BOARDHEIGHT - j  # Store the height value
                break

    # Calculate the difference in heights
    for i in range(0, len(diffs)):
        diffs[i] = heights[i + 1] - heights[i]
    #print("diffs ",diffs)

    # Calculate the maximum height
    max_height = max(heights)

    # Count the number of holes
    for i in range(0,10):
        occupied = 0  # Set the 'Occupied' flag to 0 for each new column
        for j in range(0,20):  # Scan from top to bottom
            #print((i,j)," = ",board[i][j])
            if int(board[i][j]) > 0:
                occupied = 1  # If a block is found, set the 'Occupied' flag to 1
            if int(board[i][j]) == 0 and occupied == 1:
                holes += 1  # If a hole is found, add one to the count

    # Count the number of lines
    count = 0
    for i in range(0, BOARDHEIGHT):
        check = True
        for j in range(0, BOARDWIDTH):
            if board[j][i] == '0':
                #print("Find hole in = ",(i+1,j+1))
                check = False
                break
            #else:
            #    print("Cot Find hole in = ",(i+1,j+1))
        if check:
            count+=1
    if count>0:
        print("lines = ",count)

    height_sum = sum(heights)
    for i in diffs:
        diff_sum += abs(i)
    
    #print("================== Metrics ==================")
    #print("height_sum: ",height_sum,", diff_sum: ",diff_sum,", max_height: ",max_height,", holes: ",holes)

    return height_sum, diff_sum, max_height, holes

def count_full_lines(board):
    # Count the number of lines
    count = 0
    for i in range(0, BOARDHEIGHT):
        check = True
        for j in range(0, BOARDWIDTH):
            if board[j][i] == '0':
                #print("Find hole in = ",(i+1,j+1))
                check = False
                break
            #else:
            #    print("Cot Find hole in = ",(i+1,j+1))
        if check:
            count+=1
    return count

def get_expected_score(test_board, weights):
    ### Calcola lo score sulla board di test passando il vettore dei pesi di ogni metrica
    # This function calculates the score of a given board state, given weights and the number
    # of lines previously cleared.
    height_sum, diff_sum, max_height, holes = get_parameters(test_board)
    A = weights[0]
    B = weights[1]
    C = weights[2]
    D = weights[3]
    test_score = float(A * height_sum + B * diff_sum + C * max_height + D * holes)
    return test_score


def simulate_board(test_board, test_piece, move):
    ### Simula la board di test piazzando il tetramino di test e la mossa scelta 

    # This function simulates placing the current falling piece onto the
    # board, specified by 'move,' an array with two elements, 'rot' and 'sideways'.
    # 'rot' gives the number of times the piece is to be rotated ranging in [0:3]
    # 'sideways' gives the horizontal movement from the piece's current position, in [-9:9]
    # It removes complete lines and gives returns the next board state as well as the number
    # of lines cleared.

    rot = move[0]
    sideways = move[1]
    test_lines_removed = 0
    reference_height = get_parameters(test_board)[0]
    if test_piece is None:
        return None

    # Rotate test_piece to match the desired move
    for i in range(0, rot):
        test_piece['rotation'] = (test_piece['rotation'] + 1) % len(PIECES[test_piece['shape']])

    # Test for move validity!
    if not is_valid_position(test_board, test_piece, adj_x=sideways, adj_y=0):
        # The move itself is not valid!
        return None

    # Move the test_piece to collide on the board
    test_piece['x'] += sideways
    for i in range(0, BOARDHEIGHT):
        if is_valid_position(test_board, test_piece, adj_x=0, adj_y=1):
            test_piece['y'] = i

    # Place the piece on the virtual board
    if is_valid_position(test_board, test_piece, adj_x=0, adj_y=0):
        add_to_board(test_board, test_piece)
        test_lines_removed, test_board = remove_complete_lines(test_board)

    height_sum, diff_sum, max_height, holes = get_parameters(test_board)
    one_step_reward = 5 * (test_lines_removed * test_lines_removed) - (height_sum - reference_height)   ### Premio del primo step
    return test_board, one_step_reward


def find_best_move(board, piece, weights, explore_change):
    ### Cerca la mossa migliore da effettuare sulla board, passando il vettore dei pesi e explore_change (Vedi in top per descrizione)
    move_list = []
    score_list = []
    for rot in range(0, len(PIECES[piece['shape']])):
        for sideways in range(-5, 6):
            move = [rot, sideways]
            test_board = copy.deepcopy(board)
            test_piece = copy.deepcopy(piece)
            test_board = simulate_board(test_board, test_piece, move)
            if test_board is not None:
                move_list.append(move)
                test_score = get_expected_score(test_board[0], weights)
                score_list.append(test_score)
    best_score = max(score_list)
    best_move = move_list[score_list.index(best_score)]

    if random.random() < explore_change:
        move = move_list[random.randint(0, len(move_list) - 1)]
    else:
        move = best_move
    return move


def make_move(move):
    # This function will make the indicated move, with the first digit
    # representing the number of rotations to be made and the seconds
    # representing the column to place the piece in.
    rot = move[0]
    sideways = move[1]
    if rot != 0:
        pyautogui.press('up')
        rot -= 1
    else:
        if sideways == 0:
            pyautogui.press('space')
        if sideways < 0:
            pyautogui.press('left')
            sideways += 1
        if sideways > 0:
            pyautogui.press('right')
            sideways -= 1

    return [rot, sideways]


def gradient_descent(board, piece, weights, explore_change):
    ### Funzione algoritmo AI gradient_descent
    move = find_best_move(board, piece, weights, explore_change)    ### Trova la mossa migliore da effettuare
    old_params = get_parameters(board)                              ### Preleva le metriche dalla board corrente
    test_board = copy.deepcopy(board)                               ### DeepCopy della Board a i fini di Testing
    test_piece = copy.deepcopy(piece)                               ### DeepCopy del Tetramino a i fini di Testing
    test_board = simulate_board(test_board, test_piece, move)       ### Simulazione sulla board Copiata della mossa migliore
    if test_board is not None:                                      ### Se test_board non è vuota
        new_params = get_parameters(test_board[0])                  ### Preleva le Metriche dulla board appena testata
        one_step_reward = test_board[1]                             ### Preleva la reword dalla board appena testata
    for i in range(0, len(weights)):                                ### Per ogni peso nel vettore
        weights[i] = weights[i] + alpha * weights[i] * (            ### Aggiorno il suo valore con la funzione:      [  * weights[i] è un (BOOSTER)  ]
            one_step_reward - old_params[i] + gamma * new_params[i])### Peso[i] + alpha * Peso[i] * (RicompensaStep1board - VecchieMetriche[i] + gamma * NuoveMetriche[i])
    regularization_term = abs(sum(weights))                         ### Calcolo il valore assoluto della somma dei pesi
    for i in range(0, len(weights)):                                ### Per ogni peso nel vettore
        weights[i] = 100 * weights[i] / regularization_term         ### Aggiorno il suo valore moltiplicandolo per 100 e dividendolo per il valore assoluto della somma dei pesi
        weights[i] = math.floor(1e4 * weights[i]) / 1e4  # Rounds the weights   ### Arrotondamento dei pesi con ((10^4) * Peso) / (10^4)
                                                                    
    return move, weights                                            ### Restituisce la mossa scelta e i pesi


### FORMULA:            weights[i] = weights[i] + alpha * weights[i] * (one_step_reward - old_params[i] + gamma * new_params[i])
### FORMULA TRADOTTA:   Peso[i]    = Peso[i]    + alpha * Peso[i]    * (RicompensaStp1  - OldMetriche[i] + gamma * NewMetr[i])
### Q-Learning:         Q(s,a)     = Q(s,a)     + alpha * Q(s,a)     * [reward          + gamma*Q(s+1,a+1) - Q(s,a)]           [ * Q(s,a)  prima dell reward è un BOOSTER ]


##########################################################  MAIN ZONE  ################################################################

if __name__ == '__main__':
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    pygame.display.set_icon(pygame.image.load(MEDIAPATH+'DVD.png'))
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption(APPNAME)

    show_text_screen(APPNAME)
    games_completed = 0
    scoreArray = []
    weight0Array = []
    weight1Array = []
    weight2Array = []
    weight3Array = []
    game_index_array = []
    time.sleep(3)

    try:
        #pygame.mixer.music.load(MEDIAPATH+'DiscoTetris.mp3')
        #pygame.mixer.music.play(-1)
        print("Music loaded")
    except:
        print("Music not loaded")

    while True:  # game loop
        games_completed += 1
        newScore, weights, explore_change = run_game(weights, explore_change)
        print("Game Number ", games_completed, " achieved a score of: ", newScore)
        print("weights ", weights)

        scoreArray.append(newScore)
        game_index_array.append(games_completed)
        weight0Array.append(-weights[0])
        weight1Array.append(-weights[1])
        weight2Array.append(-weights[2])
        weight3Array.append(-weights[3])
        show_text_screen('Game Over')

        if games_completed >= MAX_GAMES:
            # Plot the game score over time
            pygame.mixer.music.stop()

            plt.figure(1)
            plt.subplot(211)
            plt.plot(game_index_array, scoreArray, 'k-')
            plt.xlabel('Game Number')
            plt.ylabel('Game Score')
            plt.title('Learning Curve')
            plt.xlim(1, max(game_index_array))
            plt.ylim(0, max(scoreArray) * 1.1)

            # Plot the weights over time
            plt.subplot(212)
            plt.xlabel('Game Number')
            plt.ylabel('Weights')
            plt.title('Learning Curve')
            ax = plt.gca()
            ax.set_yscale('log')
            plt.plot(game_index_array, weight0Array, label="Aggregate Height")
            plt.plot(game_index_array, weight1Array, label="Unevenness")
            plt.plot(game_index_array, weight2Array, label="Maximum Height")
            plt.plot(game_index_array, weight3Array, label="Number of Holes")
            plt.legend(loc='lower left')
            plt.xlim(0, max(game_index_array))
            plt.ylim(0.0001, 100)
            plt.show()
            break




#################################################################### TESTER BOARD ################################################################
#board = []
#for _ in range(10):
#    board.append(['0'] * 20)

##for i in range(20):
##    print(board[i])
##    print("\n")

#for i in range(10):
#    for j in range(20):
#        if j <10:
#            board[i][j] = '1'
#print("\n")
#for i in range(10):
#    print(board[i])
#    print("\n")

#print("----------------------------------------")
#print(get_parameters(board))
            