from src.helpers import *


class Color:
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    RED = [253, 0, 0]
    GREEN = [0, 255, 0]
    CYAN = [0, 183, 235]
    BLUE = [33, 33, 222]
    DBLUE = [25, 25, 166]
    YELLOW = [255, 255, 0]
    DOTS_COLOR = [222, 161, 133]
    GRAY = [40, 40, 40]


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
SCORE_FOR_GHOST = 200
SCORE_FOR_FRUIT = [-999, 100, 300, 500, 700, 1000, 2000, 3000, 5000]  # 0 fruit is not existing!
PACMAN_MAX_LIVES = 3
SCREEN_RESPONSE = 3  # ms
PACMAN_SPEED = 2
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
MIXER_VOLUME = 0.4
SOUNDLIB = {
    'MENU': SOUNDS_DIR + 'menu.wav',
    'START': SOUNDS_DIR + 'intro.wav',
    'SIREN': SOUNDS_DIR + 'siren.wav',
    'CHOMP': SOUNDS_DIR + 'chomp.wav',
    'ENERGIZER': SOUNDS_DIR + 'ate_ghost.wav',  # It's right
    'DEATH': SOUNDS_DIR + 'death.wav',
    'FRUIT': SOUNDS_DIR + 'ate_fruit.wav',
    'GHOST': SOUNDS_DIR + 'ate_ghost.wav',
    'CUTSCENE': SOUNDS_DIR + 'cutscene.wav',
    'FRIGHTENING': SOUNDS_DIR + 'frightening.wav',
    'SPRUT1': SOUNDS_DIR + 'spurt1.wav',
    'SPRUT2': SOUNDS_DIR + 'spurt2.wav',
    'SPRUT3': SOUNDS_DIR + 'spurt3.wav',
    'SPRUT4': SOUNDS_DIR + 'spurt4.wav',
    'GHOST_TO_HOME': SOUNDS_DIR + 'ghost_to_home.wav',
    'EXTRA': SOUNDS_DIR + 'extra.wav'
}
# endregion Sound mixer constants

# HUD
SCORES_HUD_FONT_SIZE = 24
PATH_LIFE = IMAGES_DIR + 'life.png'

# region FIELD
CELL_SIZE = 20
WALL_CODES = 'ABCDEFGHIJKLMNOPQRST'
FRUIT_CODES = '12345678'
ENERGIZER_CODE = '0'
DOT_CODE = '.'
GHOSTS_ENTER_CODE = '-'
PACMAN_CODE = '@'
CENTER_TEXT_POS = Vec(15, 17)
GHOSTS_POS = {'BLINKY': (14, 11), 'PINKY': (12, 14), 'INKY': (14, 14), 'CLYDE': (16, 14)}
FIELD_MAP = [  # 28X31
    "KBBBBBBBBBBBBLKBBBBBBBBBBBBL",
    "C3 ..........DC.......... 4D",
    "C GAAH.GAAAH.DC.GAAAH.GAAH D",
    "C.DXXC.DXXXC.DC.DXXXC.DXXC.D",
    "C.EBBF.EBBBF.EF.EBBBF.EBBF.D",
    "C..........................D",
    "C.GAAH.GH.GAAAAAAH.GH.GAAH.D",
    "C0EBBF.DC.EBBLKBBF.DC.EBBF0D",
    "C......DC....DC....DC......D",
    "IAAAAH.DIAAH DC GAAJC.GAAAAJ",
    "     C.DKBBF EF EBBLC.D     ",
    "     C.DC5        6DC.D     ",
    "     C.DC QMM--MMR DC.D     ",
    "BBBBBF.EF P      O EF.EBBBBB",
    "      .   P      O   .      ",
    "AAAAAH.GH P      O GH.GAAAAA",
    "     C.DC SNNNNNNT DC.D     ",
    "     C.DC          DC.D     ",
    "     C.DC7GAAAAAAH8DC.D     ",
    "KBBBBF.EF EBBLKBBF EF.EBBBBL",
    "C............DC............D",
    "C.GAAH.GAAAH.DC.GAAAH.GAAH.D",
    "C.EBLC.EBBBF.EF.EBBBF.DKBF.D",
    "C0..DC....... @.......DC..0D",
    "IAH.DC.GH.GAAAAAAH.GH.DC.GAJ",
    "KBF.EF.DC.EBBLKBBF.DC.EF.EBL",
    "C......DC....DC....DC......D",
    "C.GAAAAJIAAH.DC.GAAJIAAAAH.D",
    "C EBBBBBBBBF.EF.EBBBBBBBBF D",
    "C1 ...................... 2D",
    "IAAAAAAAAAAAAAAAAAAAAAAAAAAF",
]
# endregion FIELD

# region CHARACTERS
FRIGHTENED_TICKS_LIMIT = 230 * SCREEN_RESPONSE  # 8 seconds
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
