from src.helpers import *

class Color:
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]
    DBLUE = [0, 0, 150]
    YELLOW = [250, 150, 0]
    DOTS_COLOR = [255, 181, 181]


class Input:
    LEFT = ord('a')
    RIGHT = ord('d')
    UP = ord('w')
    DOWN = ord('s')
    A_LEFT = ord('Ĕ')
    A_RIGHT = ord('ē')
    A_UP = ord('đ')
    A_DOWN = ord('Ē')


# Global Directories
IMAGES_DIR = 'images/'
SOUNDS_DIR = 'sounds/'
MENU_DIR = 'menu/'
CHARACTERS_IMG_DIR = IMAGES_DIR + 'sprites/'
MAP_SPRITES_DIR = CHARACTERS_IMG_DIR + 'map/'

# region General
SCREEN_SIZE = [560, 720]
SCREEN_WIDTH = SCREEN_SIZE[0]
SCREEN_HEIGHT = SCREEN_SIZE[1]
SCREEN_CENTER = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

SCORE_FOR_DOT = 100
SCORE_FOR_FRUIT = [100, 200, 300, 400, 500, 600, 700, 800]
PACMAN_MAX_LIVES = 3
SCREEN_RESPONSE = 5  # ms
PACMAN_SPEED = 3
PATH_LOGO = IMAGES_DIR + 'logo.png'
# endregion General

# region User Interface(UI)
BG_COLOR = [20, 20, 20]
TEXT_COLOR = [30, 250, 250]
TITLE_SIZE = 30
LABEL_SIZE = 20
TOOLTIP_SIZE = 15
MENU_ITEM_SPACE = 10

UI_BTN_NORM_CLR = [250, 250, 250]
UI_BTN_ACT_CLR = [250, 70, 150]
UI_BTN_SIZE = (200, 30)

FONT_PATH = MENU_DIR + 'menu_font.ttf'
PATH_HIGHSCORES = MENU_DIR + 'highscores.ini'
PATH_CREDITS = MENU_DIR + 'credits.ini'
PATH_CONTROLS = MENU_DIR + 'controls.ini'
# endregion User Interface(UI)

# region Sound mixer constants
DEBUG_MIXER = True
MUTE_AUDIO = True
SOUNDLIB = {
    'START': SOUNDS_DIR + 'pacman_beginning.wav',
    'CHOMP': SOUNDS_DIR + 'pacman_chomp.wav',
    'ENERGIZER': SOUNDS_DIR + 'pacman_eatghost.wav',
    'DEATH': SOUNDS_DIR + 'pacman_death.wav',
    'FRUIT': SOUNDS_DIR + 'pacman_eatfruit.wav',
    'GHOST': SOUNDS_DIR + 'pacman_eatghost.wav',
    'FINAL': SOUNDS_DIR + 'pacman_intermission.wav',
}
# endregion Sound mixer constants

# HUD
SCORES_HUD_FONT_SIZE = 30
PATH_HEART_IMG = IMAGES_DIR + 'life.png'

# region FIELD
CELL_SIZE = 20
WALL_CODES = 'ABCDEFGHIJKLMNOPQRST'
ENERGIZER_CODE = '0'
DOT_CODE = '.'
FRUIT_CODE = '$'
GHOSTS_ENTER_CODE = '-'
PACMAN_CODE = '@'
FIELD_MAP = [
    "KBBBBBBBBBBBBLKBBBBBBBBBBBBL",
    "C............DC............D",
    "C.GAAH.GAAAH.DC.GAAAH.GAAH.D",
    "C.DXXC.DXXXC.DC.DXXXC.DXXC.D",
    "C.EBBF.EBBBF.EF.EBBBF.EBBF.D",
    "C..........................D",
    "C.GAAH.GH.GAAAAAAH.GH.GAAH.D",
    "C0EBBF.DC.EBBLKBBF.DC.EBBF0D",
    "C......DC....DC....DC......D",
    "IAAAAH.DIAAH DC GAAJC.GAAAAJ",
    "XXXXXC.DKBBF EF EBBLC.DXXXXX",
    "XXXXXC.DC          DC.DXXXXX",
    "XXXXXC.DC QMM--MMR DC.DXXXXX",
    "BBBBBF.EF PZZZZZZO EF.EBBBBB",
    "      .   PZZZZZZO   .      ",
    "AAAAAH.GH PZZZZZZO GH.GAAAAA",
    "XXXXXC.DC SNNNNNNT DC.DXXXXX",
    "XXXXXC.DC          DC.DXXXXX",
    "XXXXXC.DC GAAAAAAH DC.DXXXXX",
    "KBBBBF.EF EBBLKBBF EF.EBBBBL",
    "C............DC............D",
    "C.GAAH.GAAAH.DC.GAAAH.GAAH.D",
    "C.EBLC.EBBBF.EF.EBBBF.DKBF.D",
    "C0..DC....... @.......DC..0D",
    "IAH.DC.GH.GAAAAAAH.GH.DC.GAJ",
    "KBF.EF.DC.EBBLKBBF.DC.EF.EBL",
    "C......DC....DC....DC......D",
    "C.GAAAAJIAAH.DC.GAAJIAAAAH.D",
    "C.EBBBBBBBBF.EF.EBBBBBBBBF.D",
    "C..........................D",
    "IAAAAAAAAAAAAAAAAAAAAAAAAAAF",
]
# endregion FIELD

# region CHARACTERS
PACMAN_SPAWN_POS = Point(14, 23)
HEROES_IMG_LIB = {
    'OPEN': CHARACTERS_IMG_DIR + 'pacman/pacman1.png',
    'NORMAL': CHARACTERS_IMG_DIR + 'pacman/pacman2.png',
    'CLOSE': CHARACTERS_IMG_DIR + 'pacman/pacman3.png',

    'BLINKY': CHARACTERS_IMG_DIR + 'ghosts/ghost1.png',
    'PINKY': CHARACTERS_IMG_DIR + 'ghosts/ghost2.png',
    'INKY': CHARACTERS_IMG_DIR + 'ghosts/ghost3.png',
    'CLYDE': CHARACTERS_IMG_DIR + 'ghosts/ghost4.png',

    'EYES_RIGHT': CHARACTERS_IMG_DIR + 'ghosts/eyes1.png',
    'EYES_LEFT': CHARACTERS_IMG_DIR + 'ghosts/eyes2.png',
    'EYES_UP': CHARACTERS_IMG_DIR + 'ghosts/eyes3.png',
    'EYES_DOWN': CHARACTERS_IMG_DIR + 'ghosts/eyes4.png',

    'FRUIT_1': CHARACTERS_IMG_DIR + 'fruits/fruit1.png',
    'FRUIT_2': CHARACTERS_IMG_DIR + 'fruits/fruit2.png',
    'FRUIT_3': CHARACTERS_IMG_DIR + 'fruits/fruit3.png',
    'FRUIT_4': CHARACTERS_IMG_DIR + 'fruits/fruit4.png',
    'FRUIT_5': CHARACTERS_IMG_DIR + 'fruits/fruit5.png',
    'FRUIT_6': CHARACTERS_IMG_DIR + 'fruits/fruit6.png',
    'FRUIT_7': CHARACTERS_IMG_DIR + 'fruits/fruit7.png',
    'FRUIT_8': CHARACTERS_IMG_DIR + 'fruits/fruit8.png',
}
# endregion CHARACTERS
