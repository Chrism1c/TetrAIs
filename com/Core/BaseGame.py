from abc import ABCMeta, abstractmethod
import time
from mpmath import mp
from com.Core.Model import *
from com.Core.Plot import *

import pygame
import random


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


class BaseGame(metaclass=ABCMeta):

    def __init__(self, r_p):
        self.r_p = r_p
        self.player = False
        self.PIece = ""
        self.pause = False
        pygame.init()
        #pygame.display.set_icon(pygame.image.load(MEDIAPATH + 'DVD.png'))
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        self.BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption(APPNAME)
        self.show_text_screen(APPNAME)

    def init_run(self):
        # setting iniziale uguale per tutti
        pass

    def run(self):

        # setup variables for the start of the game
        self.board = self.get_blank_board()
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
        self.set_PIece(100)

        # sezione riguardante l'IA genetica
        # if AI == 2:
        #     #chromosome = gen.getNewChromosome()
        #     chromosome = gen.get_chromosome()
        get_new_piece = self.get_new_piece_method()
        self.falling_piece = get_new_piece()
        self.next_piece = get_new_piece()

        while True:  # game loop

            if self.falling_piece is None:
                # No falling piece in play, so start a new piece at the top
                self.falling_piece = self.next_piece
                self.next_piece = get_new_piece()
                last_fall_time = time.time()  # reset last_fall_time
                # ENDGAME
                if not is_valid_position(self.board, self.falling_piece):
                    # can't fit a new piece on the board, so game over
                    return score, weights
                # MOVE
                current_move = self.get_move()

            # check_for_quit() ### Verifica se è stato premuto ESC per chiudere il gioco
            if self.player == False:
                current_move = self.make_move(current_move)  ### Effettua la mossa con pyautoGui

            for event in pygame.event.get():  # event handling loop
                # event_handler(event)
                if not pygame.key.get_focused():
                    self.paused()
                elif event.type == keys.KEYUP:
                    if (event.key == keys.K_p):
                        # Pausing the game
                        self.paused()
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
                            self.board, self.falling_piece, adj_x=-1):
                        self.falling_piece['x'] -= 1
                        moving_left = True
                        moving_right = False
                        last_lateral_time = time.time()

                    elif (event.key == keys.K_RIGHT or event.key == keys.K_d) and is_valid_position(
                            self.board, self.falling_piece, adj_x=1):
                        self.falling_piece['x'] += 1
                        moving_right = True
                        moving_left = False
                        last_lateral_time = time.time()

                    # rotating the piece (if there is room to rotate)
                    elif (event.key == keys.K_UP or event.key == keys.K_w):
                        self.falling_piece['rotation'] = (self.falling_piece['rotation'] + 1) % len(
                            PIECES[self.falling_piece['shape']])
                        if not is_valid_position(self.board, self.falling_piece):
                            self.falling_piece['rotation'] = (self.falling_piece['rotation'] - 1) % len(
                                PIECES[self.falling_piece['shape']])
                    elif (event.key == keys.K_q):  # rotate the other direction
                        self.falling_piece['rotation'] = (self.falling_piece['rotation'] - 1) % len(
                            PIECES[self.falling_piece['shape']])
                        if not is_valid_position(self.board, self.falling_piece):
                            self.falling_piece['rotation'] = (self.falling_piece['rotation'] + 1) % len(
                                PIECES[self.falling_piece['shape']])

                    # making the piece fall faster with the down key
                    elif (event.key == keys.K_DOWN or event.key == keys.K_s):
                        moving_down = True
                        if is_valid_position(self.board, self.falling_piece, adj_y=1):
                            self.falling_piece['y'] += 1
                        last_move_down_time = time.time()

                    # move the current piece all the way down
                    elif event.key == keys.K_SPACE:
                        moving_down = False
                        moving_left = False
                        moving_right = False
                        for i in range(1, BOARDHEIGHT):
                            if not is_valid_position(self.board, self.falling_piece, adj_y=i):
                                break
                        self.falling_piece['y'] += i - 1

            # handle moving the piece because of user input
            if (moving_left or moving_right) and time.time() - last_lateral_time > MOVESIDEWAYSFREQ:
                if moving_left and is_valid_position(self.board, self.falling_piece, adj_x=-1):
                    self.falling_piece['x'] -= 1
                elif moving_right and is_valid_position(self.board, self.falling_piece, adj_x=1):
                    self.falling_piece['x'] += 1
                last_lateral_time = time.time()

            if moving_down and time.time() - last_move_down_time > MOVEDOWNFREQ and is_valid_position(
                    self.board, self.falling_piece, adj_y=1):
                self.falling_piece['y'] += 1
                last_move_down_time = time.time()
                games_completed += 1

            # let the piece fall if it is time to fall
            if time.time() - last_fall_time > fall_freq:
                # see if the piece has landed
                if not is_valid_position(self.board, self.falling_piece, adj_y=1):
                    # falling piece has landed, set it on the board
                    add_to_board(self.board, self.falling_piece)

                    lines_removed, self.board = remove_complete_lines(self.board)
                    score += get_score(lines_removed, level)
                    # score += lines #* lines
                    lines += lines_removed  # * lines
                    level, fall_freq = get_level_and_fall_freq(score)
                    # print("level: ", level)
                    # print("fall_freq: ", fall_freq)
                    self.falling_piece = None
                else:
                    # piece did not land, just move the piece down
                    self.falling_piece['y'] += 1
                    last_fall_time = time.time()
                    games_completed += 1
            # drawing everything on the screen
            self.DISPLAYSURF.fill(BGCOLOR)
            self.draw_board(self.board)
            self.draw_status(score, lines, level, current_move)
            self.draw_next_piece(self.next_piece)
            if self.falling_piece is not None:
                self.draw_piece(self.falling_piece)
            # time.sleep(1000)
            pygame.display.update()
            self.FPSCLOCK.tick(FPS)

    @abstractmethod
    def get_move(self):
        # funzione che determina la mossa da effettuare
        pass

    def get_new_piece_method(self):
        def __random():
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

        def __pi():
            if len(self.PIeces) < 50:
                self.set_PIece(100)  # 200

            listx = list(PIECES.keys())
            shape = listx[int(self.PIeces[0])]
            new_piece = {
                'shape': shape, 'rotation': 0,  # random.randint(0,len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2,  # start it above the board (i.e. less than 0)
                'color': PIECES_COLORS[shape]
                }
            self.PIeces = self.PIeces[1:]

            return new_piece

        if self.r_p == 'r':
            return __random
        else:
            return __pi

    def set_PIece(self, num):
        mp.dps = num
        self.PIeces = str(mp.pi).translate({ord(i): None for i in '.897'})

    def show_text_screen(self, text):
        ### Splash Screen introduttiva e della pausa
        # This function displays large text in the
        # center of the screen until a key is pressed.
        # Draw the text drop shadow
        title_surf, title_rect = self.make_text_objs(text, self.BIGFONT, TEXTSHADOWCOLOR)
        title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        self.DISPLAYSURF.blit(title_surf, title_rect)

        # Draw the text
        title_surf, title_rect = self.make_text_objs(text, self.BIGFONT, TEXTCOLOR)
        title_rect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
        self.DISPLAYSURF.blit(title_surf, title_rect)

        # Draw the additional "Press a key to play." text.
        press_key_surf, press_key_rect = self.make_text_objs('Loading a new Dance !', self.BASICFONT, TEXTCOLOR)
        press_key_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
        self.DISPLAYSURF.blit(press_key_surf, press_key_rect)

        pygame.display.update()
        self.FPSCLOCK.tick()  ### Avanza al frame successivo
        time.sleep(0.5)

    def paused(self):
        pygame.mixer.music.pause()
        print("************************* Start PAUSE ************************")
        # self.DISPLAYSURF.fill(BGCOLOR)
        self.show_text_screen('Paused')  # pause until a key press
        self.pause = True
        while self.pause:
            for event in pygame.event.get():
                if event.type == keys.KEYUP:
                    if (event.key == keys.K_p):
                        pygame.mixer.music.unpause()
                        pause = False
        print("************************* End PAUSE **************************")

    def terminate(self):
        ### Termina il gioco chiudendo pygame e l'applicazione
        try:
            pygame.quit()
            sys.exit()
            # da aggiungere alla classe e distruggere l'oggetto
        except:
            print("Ended")

    def check_for_key_press(self):
        ### Verifica la pressione di un tasto
        # Go through event queue looking for a KEYUP event.
        # Grab KEYDOWN events to remove them from the event queue.
        self.check_for_quit()

        for event in pygame.event.get([keys.KEYDOWN, keys.KEYUP]):
            if event.type == keys.KEYDOWN:
                continue
            return event.key
        return None

    def check_for_quit(self):
        ### Interrompe il gioco quando viene premuto il tasto 'ESC' e
        for event in pygame.event.get(keys.QUIT):  # get all the QUIT events
            self.terminate()  # terminate if any QUIT events are present
        for event in pygame.event.get(keys.KEYUP):  # get all the KEYUP events
            if event.key == keys.K_ESCAPE:
                self.terminate()  # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event)  # put the other KEYUP event objects back

    def get_blank_board(self):
        ### Restituisco una matrice (Array of Array) di celle vuote '0'
        # create and return a new blank board data structure
        self.board = []
        for _ in range(BOARDWIDTH):
            self.board.append(['0'] * BOARDHEIGHT)
        return self.board

    def make_move(self, move):
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

    def convert_to_pixel_coords(self, boxx, boxy):
        ### Converte le coordinate xy della board nelle corrispettive coordinate xy della loro locazione sullo schermo
        # Convert the given xy coordinates of the board to xy
        # coordinates of the location on the screen.
        return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

    def draw_box(self, boxx, boxy, color, pixelx=None, pixely=None):
        ### Disegna ogni singolo blocco (ogni tetramino ha 4 blocchi) alle coordinate xy della board.
        ### Se pixelx & pixely sono avvalorati disegna quel pixel (next tetramino)
        # draw a single box (each tetromino piece has four boxes)
        # at xy coordinates on the board. Or, if pixelx & pixely
        # are specified, draw to the pixel coordinates stored in
        # pixelx & pixely (this is used for the "Next" piece).
        if color == BLANK:
            return
        if pixelx is None and pixely is None:
            pixelx, pixely = self.convert_to_pixel_coords(boxx, boxy)
        pygame.draw.rect(self.DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
        # pygame.draw.rect(self.DISPLAYSURF,  LIGHTCOLORS[color],(pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

    def draw_board(self, board):
        ### Disegna la board costrunendone il bordo, sfondo e le singole box (pixel) dei tetramini
        # draw the border around the board
        pygame.draw.rect(self.DISPLAYSURF, BORDERCOLOR,
                         (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

        # fill the background of the board
        pygame.draw.rect(self.DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
        # draw the individual boxes on the board
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                self.draw_box(x, y, board[x][y])

    def draw_status_OLD(self, score, level, best_move):
        ### Scrive le informazioni di gioco sullo schermo
        # draw the score text
        # randCol = random_color()
        score_surf = self.BASICFONT.render('# Lines: %s' % score, True, TEXTCOLOR)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (WINDOWWIDTH - 150, 20)
        self.DISPLAYSURF.blit(score_surf, score_rect)

        # draw the level text
        level_surf = self.BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
        level_rect = level_surf.get_rect()
        level_rect.topleft = (WINDOWWIDTH - 150, 50)
        self.DISPLAYSURF.blit(level_surf, level_rect)

        # draw the best_move text
        move_surf = self.BASICFONT.render('Current Move: %s' % best_move, True, TEXTCOLOR)
        move_rect = move_surf.get_rect()
        move_rect.topleft = (WINDOWWIDTH - 200, 80)
        self.DISPLAYSURF.blit(move_surf, move_rect)

    def draw_status(self, score, lines, level, best_move):
        ### Scrive le informazioni di gioco sullo schermo
        # draw the score text
        # randCol = random_color()
        score_surf = self.BASICFONT.render('# Score: %s' % score, True, TEXTCOLOR)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (WINDOWWIDTH - 150, 20)
        self.DISPLAYSURF.blit(score_surf, score_rect)

        # draw the lines text
        lines_surf = self.BASICFONT.render('# Lines: %s' % lines, True, TEXTCOLOR)
        lines_rect = lines_surf.get_rect()
        lines_rect.topleft = (WINDOWWIDTH - 150, 40)
        self.DISPLAYSURF.blit(lines_surf, lines_rect)

        # draw the level text
        level_surf = self.BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
        level_rect = level_surf.get_rect()
        level_rect.topleft = (WINDOWWIDTH - 150, 70)
        self.DISPLAYSURF.blit(level_surf, level_rect)

        # draw the best_move text
        move_surf = self.BASICFONT.render('Current Move: %s' % best_move, True, TEXTCOLOR)
        move_rect = move_surf.get_rect()
        move_rect.topleft = (WINDOWWIDTH - 200, 100)
        self.DISPLAYSURF.blit(move_surf, move_rect)

    def draw_piece(self, piece, pixelx=None, pixely=None):
        ### disegna un pezzo. Se pixelx e pixely non sono avvalorate usa le coordinate contenute in piece
        shape_to_draw = PIECES[piece['shape']][piece['rotation']]
        if pixelx is None and pixely is None:
            # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
            pixelx, pixely = self.convert_to_pixel_coords(piece['x'], piece['y'])

        ### Disegna ogni box che compone il pezzo che vuole disegnare
        # draw each of the boxes that make up the piece
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if shape_to_draw[y][x] != BLANK:
                    self.draw_box(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

    def draw_next_piece(self, piece):
        # global GlobalNextPiece
        ### Disegan il prossimo tetramino sulla sideBar
        # draw the "next" text
        # GlobalNextPiece = piece
        # print("GlobalNextPiece = ",GlobalNextPiece)
        # time.sleep(2)

        # randCol = random_color()
        next_surf = self.BASICFONT.render('Next Tetromino:', True, TEXTCOLOR)
        next_rect = next_surf.get_rect()
        next_rect.topleft = (WINDOWWIDTH - 180, 160)
        self.DISPLAYSURF.blit(next_surf, next_rect)

        pygame.draw.rect(self.DISPLAYSURF, TEXTCOLOR, (485, 195, (4.2 * BOXSIZE) + 8, (4.2 * BOXSIZE) + 8), 5)

        # draw the "next" piece
        self.draw_piece(piece, pixelx=WINDOWWIDTH - 150, pixely=200)

    def make_text_objs(self, text, font, color):
        ### Crea un oggetto testo definendone il colore e il font
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

