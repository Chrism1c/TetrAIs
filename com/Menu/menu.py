# Import libraries
import os
import pygame
import pygameMenu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------

ABOUT = ['TetrAIs: v0.5', 'Authors: ']

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
ARANCIONE = (228, 100, 36)
ARANCIONE_SCURO = (218, 1, 1)
BLU_SCURO = (0, 11, 173)
BLU_CHIARO = (84, 95, 255)

FPS = 60.0

MENU_BACKGROUND_COLOR = ARANCIONE_SCURO
COLOR_BACKGROUND = COLOR_BLACK
MENU_TITLE_COLOR = COLOR_WHITE
WINDOW_SIZE = (500, 380)

sound = None
surface = None
main_menu = None


AI_Setting_menu = None

pieceType = "r"
numOfRuns = 1

# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def main_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    :return: None
    """
    global surface
    surface.fill(COLOR_BACKGROUND)


def check_name_test(value):
    """
    This function tests the text input widget.
    :param value: The widget value
    :type value: basestring
    :return: None
    """
    print('User name: {0}'.format(value))


def changePieceType(x,y):
    global pieceType
    pieceType = y
    print("pieceType = ",pieceType)

def update_num_runs(num):
    global numOfRuns
    if len(num)>0 and int(num)>0 and int(num)<999:
        numOfRuns = int(num)
        print("numOfRuns = ", numOfRuns)



def DFS(x, mode):
    global pieceType,numOfRuns
    print("GO --> DFS ",mode," ",pieceType," ",numOfRuns)
    os.system('python com/Agents/DeepFirstSearch.py ' + pieceType + ' ' + mode +' '+ str(numOfRuns))

def Local_Search():
    global pieceType,numOfRuns
    print("GO --> LS ",pieceType," ",numOfRuns)
    os.system('python com/Agents/LocalSearch.py ' + pieceType +' '+ str(numOfRuns))

def SDG_QL():
    global pieceType,numOfRuns
    # os.system("")
    print("GO --> SDG_QL ",pieceType," ",numOfRuns)
    os.system('python com/Agents/SdgQL.py ' + pieceType + ' ' + str(numOfRuns))

def Genetic(x, mode):
    global pieceType,numOfRuns
    # os.system("")
    print("GO --> Genetic ",mode," ",pieceType)
    os.system('python com/Agents/Genetic/__main__.py ' + pieceType + ' ' + mode + ' ' + str(numOfRuns))


def Rule_Based():
    global pieceType,numOfRuns
    # os.system("")
    print("GO --> Rule_Based ",pieceType)

def Monte_Carlo():
    global pieceType,numOfRuns
    # os.system("")
    print("GO --> Monte_Carlo ",pieceType)

def Player():
    global pieceType,numOfRuns
    print("GO --> Player ", pieceType, " ",numOfRuns)
    os.system('python com/Agents/Player.py ' + pieceType + " " + str(numOfRuns))





def cat():
    #url = "https://www.youtube.com/watch?v=J---aiyznGQ"
    url = "https://www.youtube.com/watch?v=3AGqTbqhAU4"
    os.startfile(url)


def CM():
    url = "https://github.com/Chrism1c"
    os.startfile(url)


def DP():
    url = "https://github.com/W1l50n2208"
    os.startfile(url)


def MP():
    url = "https://github.com/m3ttiw"
    os.startfile(url)


# noinspection PyUnusedLocal
def update_menu_sound(value, enabled):
    """
    Update menu sound.
    :param value: Value of the selector (Label and index)
    :type value: tuple
    :param enabled: Parameter of the selector, (True/False)
    :type enabled: bool
    :return: None
    """
    global main_menu
    global sound
    if enabled:
        main_menu.set_sound(sound, recursive=True)
        print('Menu sound were enabled')
    else:
        main_menu.set_sound(None, recursive=True)
        print('Menu sound were disabled')


def main(test=False):
    """
    Main program.
    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('TetrAIs')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Set sounds
    # -------------------------------------------------------------------------
    sound = pygameMenu.sound.Sound()

    # Load example sounds
    sound.load_example_sounds()

    # Disable a sound
    sound.set_sound(pygameMenu.sound.SOUND_TYPE_ERROR, None)

    # -------------------------------------------------------------------------
    # Create menus
    # -------------------------------------------------------------------------

    AI_menu = pygameMenu.Menu(surface,
                              bgfun=main_background,
                              color_selected=COLOR_WHITE,
                              font=pygameMenu.font.FONT_NEVIS,
                              font_title=pygameMenu.font.FONT_8BIT,
                              font_color=COLOR_BLACK,
                              font_size=20,
                              font_size_title=50,
                              menu_alpha=100,
                              option_shadow=False,
                              menu_color=MENU_BACKGROUND_COLOR,
                              menu_color_title=MENU_TITLE_COLOR,
                              menu_height=int(WINDOW_SIZE[1] * 0.9),
                              menu_width=int(WINDOW_SIZE[0] * 0.9),
                              onclose=pygameMenu.events.DISABLE_CLOSE,
                              title='AI Agents',
                              widget_alignment=pygameMenu.locals.ALIGN_CENTER,  # .ALIGN_LEFT,
                              window_height=WINDOW_SIZE[1],
                              window_width=WINDOW_SIZE[0],
                              )

    AI_menu.add_option('Player', Player)
    AI_menu.add_selector('Deep First Search ',
                         [('LV1 Deep', 'LV1'), ('LV2 Deep', 'LV2')], onreturn=DFS)
    AI_menu.add_option('Local Search ', Local_Search)
    AI_menu.add_option('SGD Q-Learning ', SDG_QL)
    AI_menu.add_selector('Genetic ',
                         [('Perfect Chromosome', 'Perfect'), ('Training Run', 'Training')], onreturn=Genetic)
    AI_menu.add_option('Rule Based ', Rule_Based)
    AI_menu.add_option('Monte Carlo', Monte_Carlo)

    # AI_menu.add_option('|| BACK ||', pygameMenu.events.BACK)


    AI_Setting_menu = pygameMenu.Menu(surface,
                              bgfun=main_background,
                              color_selected=COLOR_WHITE,
                              font=pygameMenu.font.FONT_NEVIS,
                              font_title=pygameMenu.font.FONT_8BIT,
                              font_color=COLOR_BLACK,
                              font_size=25,
                              font_size_title=40,
                              menu_alpha=100,
                              option_shadow=False,
                              menu_color=MENU_BACKGROUND_COLOR,
                              menu_color_title=MENU_TITLE_COLOR,
                              menu_height=int(WINDOW_SIZE[1] * 0.85),
                              menu_width=int(WINDOW_SIZE[0] * 0.85),
                              onclose=pygameMenu.events.DISABLE_CLOSE,
                              title='AI Settings',
                              widget_alignment=pygameMenu.locals.ALIGN_CENTER,  # .ALIGN_LEFT,
                              window_height=WINDOW_SIZE[1],
                              window_width=WINDOW_SIZE[0],
                              )

    #AI_Setting_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    AI_Setting_menu.add_selector('Type of Circuit: ',
                                 [('Random', 'r'), ('PI', 'p')], onchange=changePieceType)
    AI_Setting_menu.add_text_input('How many runs?: ',
                                        default='1',
                                        onchange=update_num_runs,
                                        textinput_id='Runs')
    AI_Setting_menu.add_option("|| AI Agents ||",AI_menu)



    # About menu
    about_menu = pygameMenu.TextMenu(surface,
                                     bgfun=main_background,
                                     color_selected=COLOR_WHITE,
                                     font=pygameMenu.font.FONT_BEBAS,
                                     font_color=COLOR_BLACK,
                                     font_size_title=50,
                                     font_title=pygameMenu.font.FONT_8BIT,
                                     menu_color=MENU_BACKGROUND_COLOR,
                                     menu_color_title=COLOR_WHITE,
                                     menu_height=int(WINDOW_SIZE[1] * 1),
                                     menu_width=int(WINDOW_SIZE[0] * 1),
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=False,
                                     text_color=COLOR_BLACK,
                                     text_fontsize=25,
                                     font_size=30,
                                     title='About',
                                     window_height=WINDOW_SIZE[1],
                                     window_width=WINDOW_SIZE[0]
                                     )
    #about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    for m in ABOUT:
        about_menu.add_line(m)

    about_menu.add_option('@Chrism1c', CM)
    about_menu.add_option('@W1l50n2208', DP)
    about_menu.add_option('@m3ttiw', MP)
    about_menu.add_option('??? ', cat)

    # about_menu.add_option('> BACK <', pygameMenu.events.BACK)


    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_title=pygameMenu.font.FONT_8BIT,
                                font_color=COLOR_BLACK,
                                font_size=40,
                                font_size_title=50,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_color_title=MENU_TITLE_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 1),
                                menu_width=int(WINDOW_SIZE[0] * 1),
                                # User press ESC button
                                onclose=pygameMenu.events.EXIT,
                                option_shadow=False,
                                title='TetrAIs',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    main_menu.set_fps(FPS)

    main_menu.add_option('New Game', AI_Setting_menu)

    main_menu.add_selector('Sound ',
                           [('Off', False), ('On', True)],
                           onchange=update_menu_sound)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Close', pygameMenu.events.EXIT)

    # assert main_menu.get_widget('first_name', recursive=True) is wid1
    # assert main_menu.get_widget('last_name', recursive=True) is wid2
    # assert main_menu.get_widget('last_name') is None

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Main menu
        main_menu.mainloop(disable_loop=test)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
