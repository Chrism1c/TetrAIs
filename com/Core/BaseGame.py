from abc import ABCMeta, abstractmethod
from mpmath import mp
from com.Core.Model import *
from com.Utils.sidePanel import *

import random
import time
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.locals as keys
import pyautogui


class BaseGame(metaclass=ABCMeta):
    """
        Main class for BaseGame, all AIs are based on this class
        ---Methods----
        run():

    """

    def __init__(self, r_p, gdSidePanel, title, description, titleRun: str = None):
        """
        :param r_p: str type of piece used ('r' = random, 'p' = pi)
        gdSidePanel: bool value useful to understand if the side panel has to be shown or not
        title: contains the name of the AI
        description: contains the description of the AI
        """
        self.r_p = r_p
        self.player = False
        self.timeKiller = False
        self.minutes = 5
        self.PIece = ""
        self.pause = False
        pygame.init()
        # pygame.display.set_icon(pygame.image.load(MEDIAPATH + 'DVD.png'))
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        self.BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        if titleRun == None:
            pygame.display.set_caption(APPNAME)
        else:
            pygame.display.set_caption(titleRun)
        self.show_text_screen(APPNAME)
        self.gdSidePanel = gdSidePanel
        if self.gdSidePanel == 'yes':
            self.title = title
            self.description = description
            self.panel = SidePanel(self.title, self.description)

    def run(self):
        """
        TetrAIs Soul function, execute all main operations of the game and use the 'overrided' move function by the AI
        :return:    score : int
                    weighted array : float[]
                    tot run time : float
                    #tetramino : int
                    avg time per move : float
                    #tetramino per second (moves/s) : float
        """

        if self.gdSidePanel == 'yes':
            self.panel.showSidePanel()

        start_tot_time = time.time()
        avg_tetr_time = 0
        if self.timeKiller == True:
            start = time.time()
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
        games_completed = 0
        level, fall_freq = get_level_and_fall_freq(score)
        current_move = [0, 0]  # Relative Rotation, lateral movement
        self.set_PIece(100)

        get_new_piece = self.get_new_piece_method()
        self.falling_piece = get_new_piece()
        self.next_piece = get_new_piece()
        num_tetr = 1
        while True:  # game loop

            if self.timeKiller == True:  # se ha superato il tempo limite killiamo il gioco
                current_time = time.time()
                if round(current_time - start) > 60 * self.minutes:
                    tot_time = time.time() - start_tot_time
                    return score, weights, round(tot_time, 2), num_tetr, round(avg_tetr_time/num_tetr, 2), round(num_tetr/(tot_time*10), 2)

            if self.falling_piece is None:
                num_tetr += 1
                # No falling piece in play, so start a new piece at the top
                self.falling_piece = self.next_piece
                self.next_piece = get_new_piece()
                last_fall_time = time.time()  # reset last_fall_time
                # ENDGAME
                if not is_valid_position(self.board, self.falling_piece):
                    # can't fit a new piece on the board, so game over
                    tot_time = time.time() - start_tot_time
                    if self.gdSidePanel=='yes':
                        self.panel.destroyPanel()
                    return score, weights, round(tot_time, 2), num_tetr, round(avg_tetr_time/num_tetr, 2), round(num_tetr/(tot_time*10), 2)
                # MOVE
                start_tetr = time.time()
                current_move = self.get_move()
                end_tetr = time.time()
                avg_tetr_time += (end_tetr - start_tetr)


            self.check_for_quit()  ### Verifica se è stato premuto ESC per chiudere il gioco
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
        """
        Abstracth move function, implemented by AIs when they are instanced
        # funzione che determina la mossa da effettuare
        :return: None
        """
        # funzione che determina la mossa da effettuare
        pass

    def get_new_piece_method(self):
        """
        function useful to return the function to use by the AI
        :return: function __random() or __pi()
        """

        def __random():
            """
            # restituisce un pezzo random con colorazione random
            # return a random new piece in a random rotation
            :return: new_piece object
            """
            shape = random.choice(list(PIECES.keys()))
            new_piece = {
                'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2,  # start it above the board (i.e. less than 0)
                'color': PIECES_COLORS[shape]
            }
            return new_piece

        def __pi():
            """
            # return the next piece in the PI greek sequence
            :return: new_piece
            """
            if len(self.PIeces) < 50:  # if PIECES in PI sequence are ending, the String is updated
                self.set_PIece(100)

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
        """
        function that generates a sequence of PI greek as Deterministic sequence of Pieces to use in the game
        :param num: int value of PI greek length
        :return: "num" numbers of the PI greek sequence whitout .789 numbers
        """
        mp.dps = num
        self.PIeces = str(mp.pi).translate({ord(i): None for i in '.897'})

    def show_text_screen(self, text):
        """
        # This function displays large text screen
        :param text:
        :return: None
        """

        title_surf, title_rect = self.make_text_objs(text, self.BIGFONT, TEXTSHADOWCOLOR)
        title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        self.DISPLAYSURF.blit(title_surf, title_rect)

        # Draw the text
        title_surf, title_rect = self.make_text_objs(text, self.BIGFONT, TEXTCOLOR)
        title_rect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
        self.DISPLAYSURF.blit(title_surf, title_rect)

        # Draw the additional "Press a key to play." text.
        press_key_surf, press_key_rect = self.make_text_objs('Press "P" 4 a Break', self.BASICFONT, TEXTCOLOR)
        press_key_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
        self.DISPLAYSURF.blit(press_key_surf, press_key_rect)

        pygame.display.update()
        self.FPSCLOCK.tick()
        time.sleep(0.5)

    def paused(self):
        """
        function to put the game in pause mode
        :return: None
        """
        pygame.mixer.music.pause()
        print("************************* Start PAUSE ************************")
        # self.DISPLAYSURF.fill(BGCOLOR)
        self.show_text_screen('Paused')  # pause until a key press
        self.pause = True
        while self.pause:
            for event in pygame.event.get():
                if event.type == keys.KEYUP:
                    if event.key == keys.K_p:
                        pygame.mixer.music.unpause()
                        self.pause = False
                    elif event.key == keys.K_ESCAPE:
                        self.terminate()
                        from com.Menu.menu import main
                        main()
                        print("ESC from PAUSED")
        print("************************* End PAUSE **************************")

    def terminate(self):
        """
        function to Terminate the game closing the application
        # Termina il gioco chiudendo pygame e l'applicazione
        :return: None
        """
        try:
            if self.gdSidePanel == 'yes':
                self.panel.destroyPanel()
            pygame.quit()
        except:
            print("Ended")

    def check_for_key_press(self):
        """
        Go through event queue looking for a KEYUP event. Grab KEYDOWN events to remove them from the event queue.
        # Verifica la pressione di un tasto
        :return: event.key
        """
        self.check_for_quit()
        for event in pygame.event.get([keys.KEYDOWN, keys.KEYUP]):
            if event.type == keys.KEYDOWN:
                continue
            return event.key
        return None

    def check_for_quit(self):
        """
        Close the game when ESC button is pressed (You may need to click more times ESC to fill the queque Events)
        # Interrompe il gioco quando viene premuto il tasto 'ESC'
        :return:
        """
        try:
            for event in pygame.event.get(keys.QUIT):  # get all the QUIT events
                self.terminate()  # terminate if any QUIT events are present
            for event in pygame.event.get(keys.KEYUP):  # get all the KEYUP events
                if event.key == keys.K_ESCAPE:
                    self.terminate()  # terminate if the KEYUP event was for the Esc key
                    from com.Menu.menu import  main
                    main()
                pygame.event.post(event)  # put the other KEYUP event objects back
        except SystemExit:
            print("Closing Soppressed")

    def get_blank_board(self):
        """
        # create and return a new blank board data structure
        generate a blank matrix as lists of lists
        # Restituisco una matrice (Array of Array) di celle vuote '0'
        :return: new black board
        """
        self.board = []
        for _ in range(BOARDWIDTH):
            self.board.append(['0'] * BOARDHEIGHT)
        return self.board

    def make_move(self, move):
        """
        This function will make the indicated move, with the first digit representing the number of rotations
        to be made and the seconds representing the column to place the piece in.
        :param move: get the move tuple (rot, sideway)
        :return: [rot, sideways]
        """

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
        """
        Convert the given xy coordinates of the board to xy coordinates of the location on the screen.
        # Converte le coordinate xy della board nelle corrispettive coordinate xy della loro locazione sullo schermo
        :param boxx: int coordinate value
        :param boxy: int coordinate value
        :return: alterated coordinates
        """
        return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

    def draw_box(self, boxx, boxy, color, pixelx=None, pixely=None):
        """
        Draw a single box (each tetromino piece has four boxes) at xy coordinates on the board. Or, if pixelx & pixely
        are specified, draw to the pixel coordinates stored in pixelx & pixely (this is used for the "Next" piece).
        # Disegna ogni singolo blocco (ogni tetramino ha 4 blocchi) alle coordinate xy della board.
        # Se pixelx & pixely sono avvalorati disegna quel pixel (next tetramino)
        :param boxx: int coordinate value
        :param boxy: int coordinate value
        :param color: color value identifier
        :param pixelx: int coordinate value
        :param pixely: int coordinate value
        :return:
        """
        if color == BLANK:
            return
        if pixelx is None and pixely is None:
            pixelx, pixely = self.convert_to_pixel_coords(boxx, boxy)
        pygame.draw.rect(self.DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
        # pygame.draw.rect(self.DISPLAYSURF,  LIGHTCOLORS[color],(pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

    def draw_board(self, board):
        """
        # draw the border around the board
        # Disegna la board costrunendone il bordo, sfondo e le singole box (pixel) dei tetramini
        :param board:
        :return:
        """
        pygame.draw.rect(self.DISPLAYSURF, BORDERCOLOR,
                         (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

        # fill the background of the board
        pygame.draw.rect(self.DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
        # draw the individual boxes on the board
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                self.draw_box(x, y, board[x][y])

    def draw_status(self, score, lines, level, best_move):
        """
        Draw the score and other info text on screen
        # Scrive le informazioni di gioco sullo schermo
        :param score: score value
        :param lines: num of lines removed
        :param level: current level
        :param best_move: the best move to execute [rot,sideways]
        :return: None
        """
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
        """
        Draw the piece (4 blocks) on game board
        # disegna un pezzo. Se pixelx e pixely non sono avvalorate usa le coordinate contenute in piece
        :param piece:
        :param pixelx: int coordinate value
        :param pixely: int coordinate value
        :return:
        """
        shape_to_draw = PIECES[piece['shape']][piece['rotation']]
        if pixelx is None and pixely is None:
            # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
            pixelx, pixely = self.convert_to_pixel_coords(piece['x'], piece['y'])

        # Draw each of the boxes that make up the piece
        # Disegna ogni box che compone il pezzo che vuole disegnare
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if shape_to_draw[y][x] != BLANK:
                    self.draw_box(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

    def draw_next_piece(self, piece):
        """
         draw the "next" text
         draw the "next" piece
         draw the "next" piece square box
         # Disegan il prossimo tetramino sulla sideBar
        :param piece: piece object to draw
        :return: None
        """
        # draw the "next" text
        next_surf = self.BASICFONT.render('Next Tetromino:', True, TEXTCOLOR)
        next_rect = next_surf.get_rect()
        next_rect.topleft = (WINDOWWIDTH - 180, 160)
        self.DISPLAYSURF.blit(next_surf, next_rect)

        pygame.draw.rect(self.DISPLAYSURF, TEXTCOLOR, (485, 195, (4.2 * BOXSIZE) + 8, (4.2 * BOXSIZE) + 8), 5)

        # draw the "next" piece
        self.draw_piece(piece, pixelx=WINDOWWIDTH - 150, pixely=200)

    def make_text_objs(self, text, font, color):
        """
        Create an object text by color and font
        # Crea un oggetto testo definendone il colore e il font
        :param text:
        :param font:
        :param color:
        :return: surf, surf.get_rect()
        """
        surf = font.render(text, True, color)
        return surf, surf.get_rect()
