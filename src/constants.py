class Color:
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]
    WHITE = [255, 255, 255]

SCREEN_SIZE = [560, 720]
SCREEN_WIDTH = SCREEN_SIZE[0]
SCREEN_HEIGHT = SCREEN_SIZE[1]
SCREEN_CENTER = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

IMAGES_DIR = 'images'
SOUNDS_DIR = 'sounds'

# User Interface(UI)
BG_COLOR = [15, 15, 15]
TEXT_COLOR = [30, 250, 250]
TITLE_SIZE = 35
LABEL_SIZE = 20
TOOLTIP_SIZE = 15

UI_BTN_NORM_CLR = [250, 250, 250]
UI_BTN_ACT_CLR = [250, 180, 0]
UI_BTN_SIZE = (200, 30)

FONT_PATH = 'menu/menu_font.ttf'
PATH_HIGHSCORES = 'menu/highscores.ini'
PATH_CREDITS = 'menu/credits.ini'
PATH_CONTROLS = 'menu/controls.ini'

PATH_LOGO = IMAGES_DIR + '/logo.png'

RESPONSE = 5 # ms

# Sound mixer constants
DEBUG_MIXER = True
SOUNDLIB = {
'SOUND_START' : SOUNDS_DIR + '/pacman_beginning.wav',
'SOUND_CHOMP' : SOUNDS_DIR + '/pacman_chomp.wav',
'SOUND_DEATH' : SOUNDS_DIR + '/pacman_death.wav',
'SOUND_EAT_FRUIT' : SOUNDS_DIR + '/pacman_eatfruit.wav',
'SOUND_EAT_GHOST' : SOUNDS_DIR + '/pacman_eatghost.wav',
'SOUND_EAT_FINAL' : SOUNDS_DIR + '/pacman_intermission.wav',
}
# HUD TEST
SCORES_HUD_FONT_SIZE = 30
PATH_HEART_IMG = IMAGES_DIR + '/life.png'
PACMAN_MAX_LIFES = 5
