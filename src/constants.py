class Color:
    BLACK = [0, 0, 0]
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]


IMAGES_DIR = 'images'
SOUNDS_DIR = 'sounds'

SCREEN_RESPONCE = 3

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