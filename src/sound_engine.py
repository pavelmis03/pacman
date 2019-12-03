import pygame
from src.constants import *


class SoundMixer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
        pygame.init()
        # Make list of sounds from SOUNDLIB
        self.sounds = dict()
        for i in range(len(SOUNDLIB.items())):
            self.sounds[list(SOUNDLIB.items())[i][0]] = (pygame.mixer.Sound(list(SOUNDLIB.items())[i][1]))

        # Initialize query of sounds
        self.query_of_sounds = []
        # Global volume
        self.volume = MIXER_VOLUME

    # Can play sound at any time
    def play_sound(self, sound, loops_count=1, ad_volume = 1):
        self.sounds[sound].set_volume(0 if MUTE_AUDIO else self.volume * ad_volume)
        if not MIXER_OFF:
            self.sounds[sound].play(loops=loops_count - 1)  # For some reason plays 1 repeat more
        if DEBUG_MIXER:
            print("Plays sound: " + sound)

    # Can play sound at any time
    def stop_sound(self, sound):
        self.sounds[sound].stop()  # For some reason plays 1 repeat more
        if DEBUG_MIXER:
            print("Stop sound: " + sound)

    # Add sound to query with loops count
    def add_sound_to_query(self, sound, loops_count=1):
        request = dict(sound=sound, loops=loops_count)
        self.query_of_sounds.append(request)

    # Query of sounds - consecutive playing list of sounds
    def process_query_of_sounds(self):
        if pygame.mixer.get_busy() == 0 and len(self.query_of_sounds) > 0:
            self.play_sound(self.query_of_sounds[0]['sound'], self.query_of_sounds[0]['loops'])
            self.query_of_sounds.remove(self.query_of_sounds[0])

    def clear_query_of_sounds(self):
        self.stop_all_sounds()
        self.query_of_sounds = []

    @staticmethod
    def stop_all_sounds():
        pygame.mixer.stop()
        if DEBUG_MIXER:
            print("All sounds stopped.")

    @staticmethod
    def pause_all_sounds(unpause=False):
        if DEBUG_MIXER:
            print("All sounds are paused/unpaused.")
        if unpause:
            pygame.mixer.unpause()
        else:
            pygame.mixer.pause()