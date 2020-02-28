# Import libraries
import sys

import os
import pygame
import pygameMenu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------

ABOUT = ['TetrAIs: v0.5','Authors: ']

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
ARANCIONE  = (228, 100, 36)
ARANCIONE_SCURO = (218, 1, 1)
BLU_SCURO = (0, 11, 173)
BLU_CHIARO = (84, 95, 255)

FPS = 60.0

MENU_BACKGROUND_COLOR =  ARANCIONE_SCURO
COLOR_BACKGROUND = COLOR_BLACK
MENU_TITLE_COLOR = COLOR_WHITE
WINDOW_SIZE = (900, 580)

LS_mode = ""
Genetic_mode = ""
SDG_mode = ""

sound = None
surface = None
main_menu = None


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


def update_LS(value, mode):
    """
    :param value: Value of the selector (Label and index)
    :type value: tuple
    :param enabled: Parameter of the selector, (True/False)
    :type enabled: bool
    :return: None
    """
    global LS_mode
    if mode:
        LS_mode = "Ricerca profonda Livello 2"
        print(LS_mode)
    else:
        LS_mode = "Ricerca profonda Livello 1"
        print(LS_mode)


def update_Genetic(value, mode):
    """
    :param value: Value of the selector (Label and index)
    :type value: tuple
    :param enabled: Parameter of the selector, (True/False)
    :type enabled: bool
    :return: None
    """
    global Genetic_mode
    if mode:
        Genetic_mode = "Genetic Training"
        print(Genetic_mode)
    else:
        Genetic_mode = "Genetic Perfect Run"
        print(Genetic_mode)

def update_SDG(value, mode):
    """
    :param value: Value of the selector (Label and index)
    :type value: tuple
    :param enabled: Parameter of the selector, (True/False)
    :type enabled: bool
    :return: None
    """
    global SDG_mode
    if mode:
        SDG_mode = "SDG Random Circuit"
        print(SDG_mode)
    else:
        SDG_mode = "SDG PI Circuit"
        print(SDG_mode)


def starter(x,y):
    print("GO ",x)

def exSys():
    print("exSys")

def cat():
    import subprocess
    url = "https://www.youtube.com/watch?v=J---aiyznGQ"
    url2 = "https://www.youtube.com/watch?v=3AGqTbqhAU4"
    os.startfile(url)

def CM():
    import subprocess
    url = "https://github.com/Chrism1c"
    os.startfile(url)

def DP():
    import subprocess
    url = "https://github.com/W1l50n2208"
    os.startfile(url)

def MP():
    import subprocess
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
    pygame.display.set_caption('Example - Multi Input')
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
                              font_size=28,
                              font_size_title=50,
                              menu_alpha=100,
                              menu_color=MENU_BACKGROUND_COLOR,
                              menu_color_title = MENU_TITLE_COLOR,
                              menu_height=int(WINDOW_SIZE[1] * 0.85),
                              menu_width=int(WINDOW_SIZE[0] * 0.9),
                              onclose=pygameMenu.events.DISABLE_CLOSE,
                              title='AI Agents',
                              widget_alignment=pygameMenu.locals.ALIGN_CENTER,#.ALIGN_LEFT,
                              window_height=WINDOW_SIZE[1],
                              window_width=WINDOW_SIZE[0],
                              )


    AI_menu.add_selector('Local Search ',
                           [('LV1', False), ('LV2', True)], onchange=update_LS, onreturn=starter)
    AI_menu.add_selector('SGD Q-Learning ',
                         [('PI Circuit', False), ('Random Circuit', True)], onchange=update_SDG, onreturn=starter)
    AI_menu.add_selector('Genetic ',
                         [('Perfect Chromosome', False), ('Training', True)], onchange=update_Genetic, onreturn=starter)
    AI_menu.add_option('Probabilistic', exSys)
    AI_menu.add_option('Expert System', exSys)
    AI_menu.add_option('Monte Carlo', exSys)
    AI_menu.add_option('??? ', cat)
    #AI_menu.add_option('|| BACK ||', pygameMenu.events.BACK)

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
                                     menu_height=int(WINDOW_SIZE[1] * 0.7),
                                     menu_width=int(WINDOW_SIZE[0] * 0.5),
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=False,
                                     text_color=COLOR_BLACK,
                                     text_fontsize=25,
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

    #about_menu.add_option('> BACK <', pygameMenu.events.BACK)

    # Settings menu
    # settings_menu = pygameMenu.Menu(surface,
    #                                 bgfun=main_background,
    #                                 color_selected=COLOR_WHITE,
    #                                 font=pygameMenu.font.FONT_HELVETICA,
    #                                 font_color=COLOR_BLACK,
    #                                 font_size=25,
    #                                 font_size_title=50,
    #                                 menu_alpha=100,
    #                                 menu_color=MENU_BACKGROUND_COLOR,
    #                                 menu_height=int(WINDOW_SIZE[1] * 0.85),
    #                                 menu_width=int(WINDOW_SIZE[0] * 0.9),
    #                                 onclose=pygameMenu.events.DISABLE_CLOSE,
    #                                 title='Settings',
    #                                 widget_alignment=pygameMenu.locals.ALIGN_LEFT,
    #                                 window_height=WINDOW_SIZE[1],
    #                                 window_width=WINDOW_SIZE[0]
    #                                 )
    #
    # # Add text inputs with different configurations
    # wid1 = settings_menu.add_text_input('First name: ',
    #                                     default='John',
    #                                     onreturn=check_name_test,
    #                                     textinput_id='first_name')
    # wid2 = settings_menu.add_text_input('Last name: ',
    #                                     default='Rambo',
    #                                     maxchar=10,
    #                                     textinput_id='last_name',
    #                                     input_underline='.')
    # settings_menu.add_text_input('Your age: ',
    #                              default=25,
    #                              maxchar=3,
    #                              textinput_id='age',
    #                              input_type=pygameMenu.locals.INPUT_INT,
    #                              enable_selection=False)
    # settings_menu.add_text_input('Some long text: ',
    #                              maxwidth=19,
    #                              textinput_id='long_text',
    #                              input_underline='_')
    # settings_menu.add_text_input('Password: ',
    #                              maxchar=6,
    #                              password=True,
    #                              textinput_id='pass',
    #                              input_underline='_')
    #
    # # Create selector with 3 difficulty options
    # settings_menu.add_selector('Select difficulty',
    #                            [('Easy', 'EASY'),
    #                             ('Medium', 'MEDIUM'),
    #                             ('Hard', 'HARD')],
    #                            selector_id='difficulty',
    #                            default=1)

    # def data_fun():
    #     """
    #     Print data of the menu.
    #     :return: None
    #     """
    #     print('Settings data:')
    #     data = settings_menu.get_input_data()
    #     for k in data.keys():
    #         print(u'\t{0}\t=>\t{1}'.format(k, data[k]))
    #
    # settings_menu.add_option('Store data', data_fun)  # Call function
    # settings_menu.add_option('Return to main menu', pygameMenu.events.BACK,
    #                          align=pygameMenu.locals.ALIGN_CENTER)

    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_title=pygameMenu.font.FONT_8BIT,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                font_size_title=40,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_color_title=MENU_TITLE_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.5),
                                menu_width=int(WINDOW_SIZE[0] * 0.7),
                                # User press ESC button
                                onclose=pygameMenu.events.EXIT,
                                option_shadow=False,
                                title = 'TetrAIs',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    main_menu.set_fps(FPS)

    main_menu.add_option('New Game', AI_menu)

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
