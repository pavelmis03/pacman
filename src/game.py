import sys
import pygame

from src.constants import *
from src.sound_engine import *


class Game:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]
        self.library_init()
        self.game_over = False
        self.create_game_objects()

        self.mixer = SoundMixer()  # Initialization of sound mixer

        # region Sound Mixer Text()
        self.mixer.add_sound_to_query('SOUND_EAT_FRUIT')
        self.mixer.add_sound_to_query('SOUND_EAT_GHOST')
        self.mixer.play_sound('SOUND_DEATH')
        self.mixer.add_sound_to_query('SOUND_START')
        self.mixer.stop_all_sounds()
        self.mixer.add_sound_to_query('SOUND_EAT_FINAL')
        # endregion Sound Mixer Text()

    def create_game_objects(self):
        self.objects = []

    def library_init(self):
        pygame.init()  # Инициализация библиотеки
        pygame.font.init()
        pygame.display.set_caption('Pacman')
        icon = pygame.image.load(IMAGES_DIR + '/icon.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode(self.size)  # Создание окна (установка размера)

    def main_loop(self):
        while not self.game_over:  # Основной цикл работы программы
            self.mixer.process_query_of_sounds()  # need to process the query of sounds if it used
            self.process_events()
            self.process_logic()
            self.process_draw()
        sys.exit(0)  # Выход из программы

    def process_draw(self):
        self.screen.fill(Color.BLACK)  # Заливка цветом
        for item in self.objects:
            item.process_draw()
        pygame.display.flip()  # Double buffering
        pygame.time.wait(SCREEN_RESPONCE)  # Ждать SCREEN_RESPONCE миллисекунд

    def process_logic(self):
        for item in self.objects:
            item.process_logic()

    def process_events(self):
        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:  # Обработка события выхода
                self.game_over = True
            for item in self.objects:
                item.process_event(event)