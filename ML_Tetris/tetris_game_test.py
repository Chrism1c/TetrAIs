# contiene il core del game Tetris

# import dei moduli
from tetris_model import *
from tetris_plot import *

# IMPORT DELLE AI
import tetris_ls as ls
import tetris_ql as ql
import tetris_genetic as gen


##########################################################  GAME FUNCTIONS  #############################################################

def run_game(AI):
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
    lines = 0
    one_step_reward = 0
    games_completed = 0
    level, fall_freq = get_level_and_fall_freq(score)
    current_move = [0, 0]  # Relative Rotation, lateral movement

    # sezione riguardante l'IA genetica
    if AI == 2:
        chromosome = gen.getNewChromosome()

    if AI == 3:
        ql.set_PIece(100)
        falling_piece = ql.get_next_PIece()
        next_piece = ql.get_next_PIece()
    else:
        falling_piece = get_new_piece()
        next_piece = get_new_piece()

    while True:  # game loop

        if falling_piece is None:
            # No falling piece in play, so start a new piece at the top
            falling_piece = next_piece

            if AI == 3:
                next_piece = ql.get_next_PIece()
            else:
                next_piece = get_new_piece()

            last_fall_time = time.time()  # reset last_fall_time

            if not is_valid_position(board, falling_piece):
                # can't fit a new piece on the board, so game over
                return score, weights

            ### AI "THINK" HERE ###
            if AI == 0:
                continue  # l'utente fa la sua mossa
            elif AI == 1:
                current_move = ls.LS(board, falling_piece, next_piece)  ### Ottiene la mossa dall'IA
            elif AI == 2:
                current_move = gen.getGeneticMove(board, falling_piece, next_piece,
                                                  chromosome)  # ottiene la mossa dall'IA
            elif AI == 3:
                print("3 - Q-LEARNING DETERMINISTICO")
                current_move = ql.QL_P(board, falling_piece)  ### Ottiene la mossa dall'IA
            elif AI == 4:
                print("4 - Q-LEARNING NONDETERMINISTICO")
                current_move = ql.QL_P(board, falling_piece)  ### Ottiene la mossa dall'IA
            elif AI == 5:
                print("AI NON ANCORA IMPLEMENTATA")
                quit()  # IA DA IMPLEMENTARE
            elif AI == 6:
                print("AI NON ANCORA IMPLEMENTATA")
                quit()  # IA DA IMPLEMENTARE
            elif AI == 7:
                print("AI NON ANCORA IMPLEMENTATA")
                quit()  # IA DA IMPLEMENTARE
            elif AI == 8:
                print("AI NON ANCORA IMPLEMENTATA")
                quit()  # IA DA IMPLEMENTARE

        # check_for_quit()
        if AI:  ### Verifica se è stato premuto ESC per chiudere il gioco
            current_move = make_move(current_move)  ### Effettua la mossa con pyautoGui

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
                    falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(PIECES[falling_piece['shape']])
                    if not is_valid_position(board, falling_piece):
                        falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(
                            PIECES[falling_piece['shape']])
                elif (event.key == keys.K_q):  # rotate the other direction
                    falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(PIECES[falling_piece['shape']])
                    if not is_valid_position(board, falling_piece):
                        falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(
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

        if moving_down and time.time() - last_move_down_time > MOVEDOWNFREQ and is_valid_position(
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

                lines_removed, board = remove_complete_lines(board)
                score += get_score(lines_removed, level)
                # score += lines #* lines
                lines += lines_removed  # * lines
                level, fall_freq = get_level_and_fall_freq(score)
                print("level: ", level)
                print("fall_freq: ", fall_freq)
                falling_piece = None
            else:
                # piece did not land, just move the piece down
                falling_piece['y'] += 1
                last_fall_time = time.time()
                games_completed += 1
        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        draw_board(board)
        draw_status(score, lines, level, current_move)
        draw_next_piece(next_piece)
        if falling_piece is not None:
            draw_piece(falling_piece)
        # time.sleep(1000)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


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
    FPSCLOCK.tick()  ### Avanza al frame successivo
    time.sleep(0.5)


def check_for_quit():
    ### Interrompe il gioco quando viene premuto il tasto 'ESC' e
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
    # DISPLAYSURF.fill(BGCOLOR)
    show_text_screen('Paused')  # pause until a key press
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == keys.KEYUP:
                if (event.key == keys.K_p):
                    pygame.mixer.music.unpause()
                    pause = False
    print("************************* End PAUSE **************************")


def get_blank_board():
    ### Restituisco una matrice (Array of Array) di celle vuote '0'
    # create and return a new blank board data structure
    board = []
    for _ in range(BOARDWIDTH):
        board.append(['0'] * BOARDHEIGHT)
    return board


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


######################################################  GUI DRAW FUNCTIONS  ###########################################################


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
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    # pygame.draw.rect(DISPLAYSURF,  LIGHTCOLORS[color],(pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def draw_board(board):
    ### Disegna la board costrunendone il bordo, sfondo e le singole box (pixel) dei tetramini
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR,
                     (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            draw_box(x, y, board[x][y])


def draw_status_OLD(score, level, best_move):
    ### Scrive le informazioni di gioco sullo schermo
    # draw the score text
    # randCol = random_color()
    score_surf = BASICFONT.render('# Lines: %s' % score, True, TEXTCOLOR)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(score_surf, score_rect)

    # draw the level text
    level_surf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(level_surf, level_rect)

    # draw the best_move text
    move_surf = BASICFONT.render('Current Move: %s' % best_move, True, TEXTCOLOR)
    move_rect = move_surf.get_rect()
    move_rect.topleft = (WINDOWWIDTH - 200, 80)
    DISPLAYSURF.blit(move_surf, move_rect)


def draw_status(score, lines, level, best_move):
    ### Scrive le informazioni di gioco sullo schermo
    # draw the score text
    # randCol = random_color()
    score_surf = BASICFONT.render('# Score: %s' % score, True, TEXTCOLOR)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(score_surf, score_rect)

    # draw the lines text
    lines_surf = BASICFONT.render('# Lines: %s' % lines, True, TEXTCOLOR)
    lines_rect = lines_surf.get_rect()
    lines_rect.topleft = (WINDOWWIDTH - 150, 40)
    DISPLAYSURF.blit(lines_surf, lines_rect)

    # draw the level text
    level_surf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOWWIDTH - 150, 70)
    DISPLAYSURF.blit(level_surf, level_rect)

    # draw the best_move text
    move_surf = BASICFONT.render('Current Move: %s' % best_move, True, TEXTCOLOR)
    move_rect = move_surf.get_rect()
    move_rect.topleft = (WINDOWWIDTH - 200, 100)
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
    # global GlobalNextPiece
    ### Disegan il prossimo tetramino sulla sideBar
    # draw the "next" text
    # GlobalNextPiece = piece
    # print("GlobalNextPiece = ",GlobalNextPiece)
    # time.sleep(2)

    # randCol = random_color()
    next_surf = BASICFONT.render('Next Tetromino:', True, TEXTCOLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOWWIDTH - 180, 160)
    DISPLAYSURF.blit(next_surf, next_rect)

    pygame.draw.rect(DISPLAYSURF, TEXTCOLOR, (485, 195, (4.2 * BOXSIZE) + 8, (4.2 * BOXSIZE) + 8), 5)

    # draw the "next" piece
    draw_piece(piece, pixelx=WINDOWWIDTH - 150, pixely=200)


def make_text_objs(text, font, color):
    ### Crea un oggetto testo definendone il colore e il font    
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


##########################################################  MAIN ZONE  ################################################################

if __name__ == '__main__':
    ##game mode choice
    AI = int(input("chose game mode: \n"
                   "0 - Player\n"
                   "1 - LS\n"
                   "2 - GENETICO\n"
                   "3 - Q-LEARNING DETERMINISTICO\n"
                   "4 - Q-LEARNING NON DETERMINISTICO\n"
                   "5 - RETI NEURALI\n"
                   "6 - INCERTEZZA\n"
                   "7 - ALTRA AI\n"
                   "8 - RULE BASED\n\n"))
    if AI < 0 or AI > 8:
        print("game mode error")
        quit()

    Ngames = int(input("How many runs? "))
    if Ngames < 1:
        print("to low number of games error")
        quit()
    # AI = True if choice == 1 else False

    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    pygame.display.set_icon(pygame.image.load(MEDIAPATH + 'DVD.png'))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption(APPNAME)
    show_text_screen(APPNAME)

    games_completed = 0
    scoreArray = []
    # weight0Array = []
    # weight1Array = []
    # weight2Array = []
    # weight3Array = []
    # weight4Array = []
    # weight5Array = []
    # weight6Array = []
    game_index_array = []
    time.sleep(0.5)

    # try:
    #     #pygame.mixer.music.load(MEDIAPATH+'DiscoTetris.mp3')
    #     #pygame.mixer.music.play(-1)
    #     print("Music loaded")
    # except:
    #     print("Music not loaded")

    while True:  # games loop
        caption = "Game {game}".format(game=games_completed + 1)
        pygame.display.set_caption(caption)
        newScore, weights = run_game(AI)
        games_completed += 1
        print("Game Number ", games_completed, " achieved a score of: ", newScore)
        print("weights ", weights)

        scoreArray.append(newScore)
        game_index_array.append(games_completed)

        # weight0Array.append(-weights[0])
        # weight1Array.append(-weights[1])
        # weight2Array.append(-weights[2])
        # weight3Array.append(-weights[3])
        # weight4Array.append(-weights[4])
        # weight5Array.append(-weights[5])
        # weight6Array.append(-weights[6])
        show_text_screen('Game Over')

        # time.sleep(2)

        if games_completed >= Ngames:
            # Plot the game score over time
            pygame.mixer.music.stop()
            # plot_results(scoreArray, game_index_array)
            plot = plot_results(scoreArray, game_index_array, list())
            plot()

            break

#################################################################### TESTER BOARD ################################################################
