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
SPRITES_DIR = IMAGES_DIR + 'sprites/'
MAP_DIR = SPRITES_DIR + 'map/'
FRUITS_DIR = SPRITES_DIR + 'fruits/'
GHOSTS_DIR = SPRITES_DIR + 'ghosts/'
PACMAN_DIR = SPRITES_DIR + 'pacman/'

# region General
SCREEN_SIZE = [560, 720]
SCREEN_WIDTH = SCREEN_SIZE[0]
SCREEN_HEIGHT = SCREEN_SIZE[1]
SCREEN_CENTER = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

SCORE_FOR_DOT = 10
SCORE_FOR_ENERGIZER = 50
SCORE_FOR_FRUIT = [-999, 100, 300, 500, 700, 1000, 2000, 3000, 5000]  # 0 fruit is not existing!
PACMAN_MAX_LIVES = 3
SCREEN_RESPONSE = 1  # ms
PACMAN_SPEED = 1
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
DEBUG_MIXER = False
MUTE_AUDIO = False
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
PATH_LIFE = IMAGES_DIR + 'life.png'

# region FIELD
CELL_SIZE = 20
WALL_CODES = 'ABCDEFGHIJKLMNOPQRST'
FRUIT_CODES = '12345678'
ENERGIZER_CODE = '0'
DOT_CODE = '.'
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
    "     C.DKBBF EF EBBLC.D     ",
    "     C.DC          DC.D     ",
    "     C.DC QMM--MMR DC.D     ",
    "BBBBBF.EF P      O EF.EBBBBB",
    "      .   P      O   .      ",
    "AAAAAH.GH P      O GH.GAAAAA",
    "     C.DC SNNNNNNT DC.D     ",
    "     C.DC 12345678 DC.D     ",
    "     C.DC GAAAAAAH DC.D     ",
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
PAC_SPRITE_LIB = {
    'OPEN': PACMAN_DIR + 'pacman1.png',
    'NORMAL': PACMAN_DIR + 'pacman2.png',
    'CLOSE': PACMAN_DIR + 'pacman3.png'
}
GHOSTS_SPRITE_LIB = {
    'BLINKY': GHOSTS_DIR + 'ghost1.png',
    'PINKY': GHOSTS_DIR + 'ghost2.png',
    'INKY': GHOSTS_DIR + 'ghost3.png',
    'CLYDE': GHOSTS_DIR + 'ghost4.png',

    'EYES_RIGHT': GHOSTS_DIR + 'eyes1.png',
    'EYES_LEFT': GHOSTS_DIR + 'eyes2.png',
    'EYES_UP': GHOSTS_DIR + 'eyes3.png',
    'EYES_DOWN': GHOSTS_DIR + 'eyes4.png',
}
"""FRUITS_SPRITE_LIB = {
    'FRUIT_1': FRUITS_DIR + 'fruit1.png',
    'FRUIT_2': FRUITS_DIR + 'fruit2.png',
    'FRUIT_3': FRUITS_DIR + 'fruit3.png',
    'FRUIT_4': FRUITS_DIR + 'fruit4.png',
    'FRUIT_5': FRUITS_DIR + 'fruit5.png',
    'FRUIT_6': FRUITS_DIR + 'fruit6.png',
    'FRUIT_7': FRUITS_DIR + 'fruit7.png',
    'FRUIT_8': FRUITS_DIR + 'fruit8.png',
}"""
# endregion CHARACTERS
