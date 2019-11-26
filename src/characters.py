import pygame
from random import randrange
from src.base_classes import DrawableObject
from src.constants import *
import sys


class Ghost(DrawableObject):
    def __init__(self, game_object, x, y, color):
        super().__init__(game_object)

        self.ghost = pygame.image.load(HEROES_IMG_LIB['COOL'])
        self.state = False  # состояние призрака
                            # False -> блуждание
                            # True -> преследование

        # выбор цвета призрака       ---------------------------
        self.ghost = pygame.image.load(HEROES_IMG_LIB[color])
        # ------------------------------------------------------
        # координаты призрака ----------------------------------
        self.ghost_rect = self.ghost.get_rect()
        self.ghost_rect.x = x
        self.ghost_rect.y = y
        # ------------------------------------------------------

    def process_events(self, event):
        self.pacman_x = 20
        self.pacman_y = 20
        self.ranged = ((self.ghost_rect.x - self.pacman_x) ** 2 + (self.ghost_rect.y <= self.pacman_y) ** 2) ** 0.5

        self.g_go_left_up = 0
        self.g_go_left_down = 0
        self.g_go_right_up = 0
        self.g_go_right_down = 0

        self.g_go_left = 0
        self.g_go_right = 0
        self.g_go_up = 0
        self.g_go_down = 0

        if self.ranged < 200:
            self.state = True
        else:
            self.state = False

        if self.state:
            if self.ghost_rect.x > self.pacman_x and self.ghost_rect.x > self.pacman_x:
                self.g_go_left_up = 1
            elif self.ghost_rect.x < self.pacman_x and self.ghost_rect.x > self.pacman_x:
                self.g_go_right_up = 1
            elif self.ghost_rect.x > self.pacman_x and self.ghost_rect.x < self.pacman_x:
                self.g_go_left_down = 1
            elif self.ghost_rect.x < self.pacman_x and self.ghost_rect.x < self.pacman_x:
                self.g_go_right_down = 1

    def smooth_move(self):
        self.count_of_steps = randrange(1, 4)
        self.random_direction = randrange(1, 5)  # рандомное направление
                                                 # 1 -> влево
                                                 # 2 -> вправо
                                                 # 3 -> вверх
                                                 # 4 -> вниз
        i = 0

        if self.random_direction == 1:  # влево
            for i in range(self.count_of_steps):
                if self.ghost_rect.x > 20:  # проверка на выход за пределы экрана
                    self.ghost_rect.x -= 5  # шаг
            i = 0

        if self.random_direction == 2:  # вправо
            for i in range(self.count_of_steps):
                if self.ghost_rect.x < 780:  # проверка на выход за пределы экрана
                    self.ghost_rect.x += 5  # шаг
            i = 0

        if self.random_direction == 3:  # вверх
            for i in range(self.count_of_steps):
                if self.ghost_rect.y > 20:  # проверка на выход за пределы экрана
                    self.ghost_rect.y -= 5  # шаг
            i = 0

        if self.random_direction == 4:  # вниз
            for i in range(self.count_of_steps):
                if self.ghost_rect.y < 580:  # проверка на выход за пределы экрана
                    self.ghost_rect.y += 5  # шаг
            i = 0

    def process_draw(self):
        self.game_object.screen.blit(self.ghost, self.ghost_rect)  # отобразить объект


class Pacman(DrawableObject):
    def __init__(self, game_object, x, y):
        super().__init__(game_object)
        # Initialize dict of used images
        self.images = dict()
        for i in range(len(HEROES_IMG_LIB.items())):
            self.images[list(HEROES_IMG_LIB.items())[i][0]] = (pygame.image.load(list(HEROES_IMG_LIB.items())[i][1]))
        # Init pacman image and rect
        self.pacman_img = self.images['OPEN']
        self.pacman_rect = self.pacman_img.get_rect().move(x, y)

        self.key_down = 0

        self.move_left = False  # флаг анимации движеия влево
        self.move_right = False  # флаг анимации движеия вправо
        self.move_up = False  # флаг анимации движеия вверх
        self.move_down = False  # флаг анимации движеия вниз
        # есть по две разные картинки на каждое направление (всего 8)
        # в цикле значение меняется
        # если флаг False, то рисуется 1 изображение
        # если флаг True, то рисуется 2 изображени

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:  # проверка нажатия на клавиатуру
            self.game_object.mixer.stop_all_sounds()
            self.game_object.mixer.play_sound('SOUND_CHOMP', -1)
            if event.key == pygame.K_a:
                self.key_down = 1  # положене "1
            elif event.key == pygame.K_d:
                self.key_down = 2  # положене "2"
            elif event.key == pygame.K_w:
                self.key_down = 3  # положене "3"
            elif event.key == pygame.K_s:
                self.key_down = 4  # положене "4"
        if event.type == pygame.KEYUP and False:
            self.key_down = 0
            self.game_object.mixer.stop_all_sounds()

    def process_logic(self):  # логика объектов
        # действие движение --------------
        self.move_left = not self.move_left  # изменение значения флага
        self.move_right = not self.move_right  # изменение значения флага
        self.move_up = not self.move_up  # изменение значения флага
        self.move_down = not self.move_down  # изменение значения флага
        self.smooth_move()
        # -------------------------------

    def smooth_move(self):

        if self.key_down == 1:
            self.pacman_rect.x -= 3  # шаг влево
            # Смена спрайта : анимация------------------------------
            if self.move_left:
                self.pacman_img = pygame.transform.rotate(self.images['OPEN'], -180)
            else:
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], -180)
            # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.key_down == 2:
            self.pacman_rect.x += 3  # шаг вправо
            # Смена спрайта : анимация------------------------------
            if self.move_right:
                self.pacman_img = pygame.transform.rotate(self.images['OPEN'], 0)
            else:
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], 0)
            # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.key_down == 3:
            self.pacman_rect.y -= 3  # шаг вверх
            # Смена спрайта : анимация------------------------------
            if self.move_up:
                self.pacman_img = pygame.transform.rotate(self.images['OPEN'], 90)
            else:
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], 90)
            # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.key_down == 4:
            self.pacman_rect.y += 3  # шаг вниз
            # Смена спрайта : анимация------------------------------
            if self.move_down:
                self.pacman_img = pygame.transform.rotate(self.images['OPEN'], -90)
            else:
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], -90)
            # ------------------------------------------------------

    def process_draw(self):
        self.game_object.screen.blit(self.pacman_img, self.pacman_rect)  # отобразить объект

"""
class Game:
    def __init__(self, width = 800, height = 600):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]
        self.library_init()
        self.game_over = False
        self.create_game_objects()

        # разные параметры -------------
        self.move_left = False   # флаг анимации движеия влево
        self.move_right = False  # флаг анимации движеия вправо
        self.move_up = False     # флаг анимации движеия вверх
        self.move_down = False   # флаг анимации движеия вниз
                                 # есть по две разные картинки на каждое направление (всего 8)
                                 # в цикле значение меняется
                                 # если флаг False, то рисуется 1 изображение
                                 # если флаг True, то рисуется 2 изображени

        self.smooth_ghost_move = 0
        self.pacman_coordinate = []
        # ------------------------------

    def main_loop(self):
        while not self.game_over:  # Основной цикл работы программы
            self.process_events()
            self.process_logic()
            self.process_draw()
        sys.exit(0)  # Выход из программы

    def process_events(self):
        # Обработка всех событий -------------------------------
        for event in pygame.event.get():
            # Обработка события выхода--------------------------
            if event.type == pygame.QUIT:
                 self.game_over = True
            # --------------------------------------------------

            # логика движения ----------------------------------
            self.A.process_event(event)
            self.pacman_coordinate = self.A.get_coordinate()
            self.G.process_event(event, self.pacman_coordinate[0], self.pacman_coordinate[1])
            # --------------------------------------------------

    def process_logic(self):  # логика объектов
        # действие движение --------------
        self.move_left = not self.move_left     # изменение значения флага
        self.move_right = not self.move_right   # изменение значения флага
        self.move_up = not self.move_up         # изменение значения флага
        self.move_down = not self.move_down     # изменение значения флага
        self.A.smooth_move(self.move_left, self.move_right, self.move_up, self.move_down)
        self.G.smooth_move()
        # -------------------------------

    def process_draw(self):
        self.A.draw_object(self.screen)
        self.G.draw_object(self.screen)
"""