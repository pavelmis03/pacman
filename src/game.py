import sys
import pygame
from os import environ

from src.constants import *
from src.sound_engine import *
from src.food import *
from src.menu import *
from src.hud import *
from src.field import Field
from src.characters import *


class Game:
    screen = field = food = menu = hud = None

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.size = [width, height]
        self.library_init()
        self.game_over = False
        self.start_game = False
        self.lives = PACMAN_MAX_LIVES
        self.scores = 0

        self.objects = []
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
        self.hud = HUD(self)
        self.field = Field(self)
        self.food = self.field.get_food()
        pac_pos = self.field.get_cell_position(PACMAN_SPAWN_POS[0], PACMAN_SPAWN_POS[1])
        self.pacman = Pacman(self, pac_pos[0] + 2, pac_pos[1] + 4)
        self.blinky = Ghost(self, 100, 100, 'BLINKY')
        self.pinky = Ghost(self, 100, 100, 'PINKY')
        self.inky = Ghost(self, 100, 100, 'INKY')
        self.clyde = Ghost(self, 100, 100, 'CLYDE')

        # Add all food to object list
        for food in self.food:
            self.objects.append(food)

        self.objects += [self.hud, self.field, self.pacman, self.blinky, self.pinky, self.inky, self.clyde]


    def library_init(self):
        # Initialize all libs
        pygame.init()
        pygame.font.init()
        # Create and move a window
        self.screen = pygame.display.set_mode(self.size, flags=pygame.DOUBLEBUF)  # Create window
        environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (1, 30)  # Move window to start coordinates
        # Set window caption
        pygame.display.set_caption('Pacman')
        # Setup the icon
        icon = pygame.image.load(IMAGES_DIR + '/icon.png')
        pygame.display.set_icon(icon)

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
        for item in self.objects:
            item.process_draw()
        pygame.display.flip()  # Double buffering
        pygame.time.wait(RESPONSE)  # Ждать SCREEN_RESPONCE миллисекунд

    def process_logic(self):
        self.screen.fill(BG_COLOR)  # Заливка цветом
        for item in self.objects:
            item.process_logic()
        self.field.process_logic()

    def process_events(self):
        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:  # Обработка события выхода
                self.game_over = True
            for item in self.objects:
                item.process_event(event)