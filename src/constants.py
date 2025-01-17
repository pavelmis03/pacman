from random import choice

from src.helpers import *
from src.enums import *


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (253, 0, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 183, 235)
    BLUE = (33, 33, 222)
    DBLUE = (33, 33, 222)
    YELLOW = (255, 255, 0)
    DOTS_COLOR = (222, 161, 133)
    GRAY = (40, 40, 40)
    PINKY = (255, 203, 219)
    ORANGE = (255, 184, 82)


class Input:
    LEFT = ord('a')
    RIGHT = ord('d')
    UP = ord('w')
    DOWN = ord('s')
    A_LEFT = ord('Ĕ')
    A_RIGHT = ord('ē')
    A_UP = ord('đ')
    A_DOWN = ord('Ē')


# region Global Directories

IMAGES_DIR = 'images/'
SOUNDS_DIR = 'sounds/ogg/'
MENU_DIR = 'menu/'
WINDOW_ICON_PATH = IMAGES_DIR + 'icon.png'
SPRITES_DIR = IMAGES_DIR + 'sprites/'
MAP_DIR = SPRITES_DIR + 'map/'
FRUITS_DIR = SPRITES_DIR + 'fruits/'
GHOSTS_DIR = SPRITES_DIR + 'ghosts/'
PACMAN_DIR = SPRITES_DIR + 'pacman/'
PATH_LOGO = IMAGES_DIR + 'logo.png'

# endregion Global Directories

# region Customization

SHOW_GHOSTS_TARGETS = False
MUTE_AUDIO = False
SKIP_CUTSCENES = False

# endregion Customization

# region General

class SZ:
    DEF_SCREEN_SIZE = Vec(560, 720)
    SCREEN_SIZE = DEF_SCREEN_SIZE
    SCREEN_WIDTH = SCREEN_SIZE.x
    SCREEN_HEIGHT = SCREEN_SIZE.y
    SCREEN_CENTER = Vec(SCREEN_SIZE.x // 2, SCREEN_SIZE.y // 2)

    def resize(self, size: Vec):
        self.SCREEN_SIZE = size
        self.SCREEN_WIDTH = size.x
        self.SCREEN_HEIGHT = size.y
        self.SCREEN_CENTER = Vec(size.x // 2, size.y // 2)


size = SZ()
SCORE_FOR_DOT = 10
SCORE_FOR_ENERGIZER = 50
SCORE_FOR_GHOST = [200, 400, 800, 1600]
SCORE_FOR_FRUIT = [-999, 100, 300, 500, 700, 1000, 2000, 3000, 5000]  # 0 fruit is not existing!
PACMAN_MAX_LIVES = 3
SCREEN_RESPONSE = 2  # ms
PACMAN_SPEED = 4
GHOST_SPEED = 2
QUALITY = 16

# endregion General

# region User Interface(UI)

BG_COLOR = [20, 20, 20]
TEXT_COLOR = [30, 250, 250]
TITLE_SIZE = 30
LABEL_SIZE = 20
TOOLTIP_SIZE = 15
MENU_ITEM_SPACE = 10

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

UI_BTN_NORM_CLR = [250, 250, 250]
UI_BTN_ACT_CLR = [250, 70, 150]
UI_BTN_SIZE = (200, 30)

FONT_PATH = MENU_DIR + 'menu_font.ttf'
PATH_HIGHSCORES = MENU_DIR + 'highscores.ini'
PATH_CREDITS = MENU_DIR + 'credits.ini'
PATH_CONTROLS = MENU_DIR + 'controls.ini'
CONFIG_PATH = 'config.ini'
MAPS_DIR = 'maps/'

# endregion User Interface(UI)

# region Sound mixer constants

DEBUG_MIXER = False
MIXER_VOLUME = 0.5
MAX_MENU_MUSIC = 6
AUD_FORMAT = '.ogg'
SOUNDLIB = {
    'MENU1': SOUNDS_DIR + 'menu1' + AUD_FORMAT,
    'MENU2': SOUNDS_DIR + 'menu2' + AUD_FORMAT,
    'MENU3': SOUNDS_DIR + 'menu3' + AUD_FORMAT,
    'MENU4': SOUNDS_DIR + 'menu4' + AUD_FORMAT,
    'MENU5': SOUNDS_DIR + 'menu5' + AUD_FORMAT,
    'MENU6': SOUNDS_DIR + 'menu6' + AUD_FORMAT,
    'START': SOUNDS_DIR + 'intro' + AUD_FORMAT,
    'SIREN': SOUNDS_DIR + 'siren' + AUD_FORMAT,
    'CHOMP': SOUNDS_DIR + 'chomp' + AUD_FORMAT,
    'ENERGIZER': SOUNDS_DIR + 'ate_ghost' + AUD_FORMAT,  # It's right
    'DEATH': SOUNDS_DIR + 'death' + AUD_FORMAT,
    'FRUIT': SOUNDS_DIR + 'ate_fruit' + AUD_FORMAT,
    'GHOST': SOUNDS_DIR + 'ate_ghost' + AUD_FORMAT,
    'CUTSCENE': SOUNDS_DIR + 'cutscene' + AUD_FORMAT,
    'FRIGHTENING': SOUNDS_DIR + 'frightening' + AUD_FORMAT,
    'SPRUT1': SOUNDS_DIR + 'spurt1' + AUD_FORMAT,
    'SPRUT2': SOUNDS_DIR + 'spurt2' + AUD_FORMAT,
    'SPRUT3': SOUNDS_DIR + 'spurt3' + AUD_FORMAT,
    'SPRUT4': SOUNDS_DIR + 'spurt4' + AUD_FORMAT,
    'GHOST_TO_HOME': SOUNDS_DIR + 'ghost_to_home' + AUD_FORMAT,
    'EXTRA': SOUNDS_DIR + 'extra' + AUD_FORMAT
}

# endregion Sound mixer constants

# region FIELD

CELL_SIZE = 20
WALL_CODES = 'ABCDEFGHIJKLMNOPQRSTX'
FRUIT_CODES = '12345678'
ENERGIZER_CODE = '0'
DOT_CODE = '.'
GHOSTS_ENTER_CODE = '-'
PACMAN_CODE = '@'
GHOSTS_CODES = {'BLINKY': 'b', 'PINKY': 'p', 'INKY': 'i', 'CLYDE': 'c'}
DEFAULT_MAP_FILE = 'def_map.ini'

# endregion FIELD

# region HUD

SCORES_HUD_FONT_SIZE = CELL_SIZE
PATH_LIFE = IMAGES_DIR + 'life.png'

# endregion HUD

# region User Events

USEREVENT = 24  # Constant from pygame
PM_TIMER = USEREVENT + 1
GH_TIMER = USEREVENT + 2
GB_TIMER = USEREVENT + 3

# endregion User Events

# region CHARACTERS

FRIGHTENED_TICKS_LIMIT = 8000  # 8 seconds
SLOW_MO_TICKS_LIMIT = 600  # 0.5 seconds
DEATH_TICKS_LIMIT = 1900  # 1.9 seconds
PACMAN_SPAWN_POS = Vec(14, 23)
PAC_SPRITE_LIB = {
    'OPEN': PACMAN_DIR + 'pacman1.png',
    'NORMAL': PACMAN_DIR + 'pacman2.png',
    'CLOSE': PACMAN_DIR + 'pacman3.png',
    'D0': PACMAN_DIR + 'pacman4.png',
    'D1': PACMAN_DIR + 'pacman5.png',
    'D2': PACMAN_DIR + 'pacman6.png',
    'D3': PACMAN_DIR + 'pacman7.png',
    'D4': PACMAN_DIR + 'pacman8.png',
    'D5': PACMAN_DIR + 'pacman9.png',
    'D6': PACMAN_DIR + 'pacman10.png',
    'D7': PACMAN_DIR + 'pacman11.png',
    'D8': PACMAN_DIR + 'pacman12.png',
    'D9': PACMAN_DIR + 'pacman13.png',
    'D10': PACMAN_DIR + 'pacman14.png'
}
GHOSTS_SPRITE_LIB = {
    'BLINKY': GHOSTS_DIR + 'ghost1.png',
    'BLINKY1': GHOSTS_DIR + 'ghost01.png',
    'PINKY': GHOSTS_DIR + 'ghost2.png',
    'PINKY1': GHOSTS_DIR + 'ghost02.png',
    'INKY': GHOSTS_DIR + 'ghost3.png',
    'INKY1': GHOSTS_DIR + 'ghost03.png',
    'CLYDE': GHOSTS_DIR + 'ghost4.png',
    'CLYDE1': GHOSTS_DIR + 'ghost04.png',

    'FRIGHTENED': GHOSTS_DIR + 'ghost5.png',
    'FRIGHTENED1': GHOSTS_DIR + 'ghost05.png',
    'ATTENT': GHOSTS_DIR + 'ghost6.png',
    'ATTENT1': GHOSTS_DIR + 'ghost06.png',

    'EYES_RIGHT': GHOSTS_DIR + 'eyes1.png',
    'EYES_LEFT': GHOSTS_DIR + 'eyes2.png',
    'EYES_UP': GHOSTS_DIR + 'eyes3.png',
    'EYES_DOWN': GHOSTS_DIR + 'eyes4.png',
    'EYES_FR_1': GHOSTS_DIR + 'eyes5.png',
    'EYES_FR_2': GHOSTS_DIR + 'eyes6.png',
}
# endregion CHARACTERS

# region Characteristics tables

WAITING_TIME = {GhostType.BLINKY: 0,
                GhostType.PINKY: 100,
                GhostType.INKY: 99999999,
                GhostType.CLYDE: 99999999}
SC_CH_TURNS = {'LVL1': [7000, 20000, 7000, 20000, 5000, 20000, 5000, 999999999],
               'LVL2-4': [7000, 20000, 7000, 20000, 5000, 1033, 16, 999999999],
               'LVL5+': [5000, 20000, 5000, 20000, 5000, 1037, 16, 999999999]}
# (100% speed = 189.393940 pixels/sec)
FULL_SPEED = 189
REF_TABLE = [
    {},  # ZERO LEVEL DOESN'T EXISTS
    {'FRUIT': 1, 'GM_SPEED': 21, 'FR_TIME': 6000, 'FR_G_SPEED': 50, 'GH_SPEED': 19},
    {'FRUIT': 2, 'GM_SPEED': 19, 'FR_TIME': 5000, 'FR_G_SPEED': 55, 'GH_SPEED': 17},
    {'FRUIT': 3, 'GM_SPEED': 19, 'FR_TIME': 4000, 'FR_G_SPEED': 55, 'GH_SPEED': 17},
    {'FRUIT': 3, 'GM_SPEED': 19, 'FR_TIME': 3000, 'FR_G_SPEED': 55, 'GH_SPEED': 17},
    {'FRUIT': 4, 'GM_SPEED': 17, 'FR_TIME': 2000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 4, 'GM_SPEED': 17, 'FR_TIME': 5000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 5, 'GM_SPEED': 17, 'FR_TIME': 2000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 5, 'GM_SPEED': 17, 'FR_TIME': 2000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 6, 'GM_SPEED': 17, 'FR_TIME': 1000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 6, 'GM_SPEED': 17, 'FR_TIME': 5000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 7, 'GM_SPEED': 17, 'FR_TIME': 2000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 7, 'GM_SPEED': 17, 'FR_TIME': 1000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 8, 'GM_SPEED': 17, 'FR_TIME': 1000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 8, 'GM_SPEED': 17, 'FR_TIME': 3000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 8, 'GM_SPEED': 17, 'FR_TIME': 1000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 8, 'GM_SPEED': 17, 'FR_TIME': 1000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 8, 'GM_SPEED': 17, 'FR_TIME': 0000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 8, 'GM_SPEED': 17, 'FR_TIME': 1000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 8, 'GM_SPEED': 17, 'FR_TIME': 0000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 8, 'GM_SPEED': 17, 'FR_TIME': 0000, 'FR_G_SPEED': 60, 'GH_SPEED': 16},
    {'FRUIT': 8, 'GM_SPEED': 19, 'FR_TIME': 0000, 'FR_G_SPEED': 60, 'GH_SPEED': 17}
]
FRUIT_LIFETIME = choice([9333, 10000, 9750])

# endregion Characteristics tables
