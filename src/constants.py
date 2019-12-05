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

SCREEN_RESPONSE = 3  # ms

# region User Interface(UI)
BG_COLOR = [20, 20, 20]
FONT_PATH = MENU_DIR + 'menu_font.ttf'
# endregion User Interface(UI)

SCORES_HUD_FONT_SIZE = 24

# region FIELD
CELL_SIZE = 20
WALL_CODES = 'ABCDEFGHIJKLMNOPQRST'
FRUIT_CODES = '12345678'
ENERGIZER_CODE = '0'
DOT_CODE = '.'
GHOSTS_ENTER_CODE = '-'
PACMAN_CODE = '@'
