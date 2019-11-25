import sys
import pygame

from src.constants import *
from src.sound_engine import *
from src.menu import *


class Game:
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]
        self.library_init()
        self.game_over = False
        self.start_game = False
        self.create_game_objects()

        self.mixer = SoundMixer()  # Initialization of sound mixer

    def init_menu(self):
        # Start sound
        self.mixer.play_sound('SOUND_START', -1)

        # Start Main menu First
        self.menu = MainMenu(self)
        self.menu.menu_loop()

        # Stop sound if we start game or close it
        self.mixer.stop_all_sounds()

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
        # Start Main menu First
        self.init_menu()

        while not self.start_game:
            self.menu.menu_loop()

        # If user click START - start game
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
        pygame.time.wait(RESPONSE)  # Ждать SCREEN_RESPONCE миллисекунд

    def process_logic(self):
        for item in self.objects:
            item.process_logic()

    def get_highscores(self):
        f = open(PATH_HIGHSCORES, 'r', encoding="utf-8")
        text = f.readlines()
        text = [line.rstrip() for line in text]
        f.close()
        minscore = 100 # if future set in self.scores
        name_of_min_scores = 'Player' #set name
        glist = []
        glist.append([minscore, name_of_min_scores])
        for line in text:
            st, a = map(str, line.split(':'))
            glist.append([int(a), st])
        glist.sort()
        f = open(PATH_HIGHSCORES, 'w', encoding="utf-8")
        for i in range(min(len(glist), 5)):
            l = glist[len(glist) - i - 1]
            f.write(str(l[1]) + ':' + str(l[0]) + '\n')
        f.close()




    def process_events(self):
        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:  # Обработка события выхода
                self.get_highscores()
                self.game_over = True
            for item in self.objects:
                item.process_event(event)