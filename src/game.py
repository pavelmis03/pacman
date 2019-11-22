import sys
import pygame

from src.constants import *
from src.hud import *


class Game:
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]
        self.library_init()
        self.game_over = False
        self.hud = HUD(self)
        self.lifes = 3

        self.create_game_objects()

    def create_game_objects(self):
        self.objects = [self.hud]

    def library_init(self):
        pygame.init()  # Инициализация библиотеки
        pygame.font.init()
        pygame.display.set_caption('Pacman')
        icon = pygame.image.load(IMAGES_DIR + '/icon.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode(self.size)  # Создание окна (установка размера)

    def main_loop(self):
        while not self.game_over:  # Основной цикл работы программы
            self.process_events()
            self.process_logic()
            self.process_draw()
        sys.exit(0)  # Выход из программы

    def process_draw(self):
        self.screen.fill(Color.BLACK)  # Заливка цветом
        for item in self.objects:
            item.process_draw()
        pygame.display.flip()  # Double buffering
        pygame.time.wait(5)  # Ждать 10 миллисекунд

    def process_logic(self):
        for item in self.objects:
            item.process_logic()

    def process_events(self):
        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:  # Обработка события выхода
                self.game_over = True
            for item in self.objects:
                item.process_event(event)