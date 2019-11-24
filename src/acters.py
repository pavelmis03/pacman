import pygame
from random import randrange
import sys


class Bots:

    def __init__(self, x, y, color):
        self.ghost = pygame.image.load("dead-g-1.png")
        self.state = False  # состояние призрака
                            # False -> блуждание
                            # True -> преследование

        # выбор цвета призрака       ---------------------------
        if color[0] == 'b':
            self.ghost = pygame.image.load("blue-g-left-1.png")
        if color[0] == 'g':
            self.ghost = pygame.image.load("green-g-left-1.png")
        if color[0] == 'r':
            self.ghost = pygame.image.load("red-g-left-1.png")
        if color[0] == 'o':
            self.ghost = pygame.image.load("orange-g-left-1.png")
        # ------------------------------------------------------
        # координаты призрака ----------------------------------
        self.ghost_in_rect = self.ghost.get_rect()
        self.ghost_in_rect.x = x
        self.ghost_in_rect.y = y
        # ------------------------------------------------------

    def process_event(self, event, p_x, p_y):
        pass

    def smooth_move(self):
        self.count_of_steps = randrange(1, 4) #
        self.random_direction = randrange(1, 5)  # рандомное направление
                                                 # 1 -> влево
                                                 # 2 -> вправо
                                                 # 3 -> вверх
                                                 # 4 -> вниз
        i = 0

        if self.random_direction == 1:  # влево
            for i in range(self.count_of_steps):
                if self.ghost_in_rect.x > 20:  # проверка на выход за пределы экрана
                    self.ghost_in_rect.x -= 5  # шаг
            i = 0

        if self.random_direction == 2:  # вправо
            for i in range(self.count_of_steps):
                if self.ghost_in_rect.x < 780:  # проверка на выход за пределы экрана
                    self.ghost_in_rect.x += 5  # шаг
            i = 0

        if self.random_direction == 3:  #  вверх
            for i in range(self.count_of_steps):
                if self.ghost_in_rect.y > 20:  # проверка на выход за пределы экрана
                    self.ghost_in_rect.y -= 5  # шаг
            i = 0

        if self.random_direction == 4:  #  вниз
            for i in range(self.count_of_steps):
                if self.ghost_in_rect.y < 580:  # проверка на выход за пределы экрана
                    self.ghost_in_rect.y += 5  # шаг
            i = 0

    def draw_object(self, screen):
        screen.blit(self.ghost, self.ghost_in_rect)  # отобразить объект


class Pacman:

    def __init__(self, x, y):
        self.pacman = pygame.image.load("pm-right-small.png")
        self.pacman_in_rect = self.pacman.get_rect()
        self.pacman_in_rect.x = x
        self.pacman_in_rect.y = y

    def get_coordinate(self):
        return self.pacman_in_rect

    def process_event(self, event):
        self.key_down = 0   # флаг на нажатие одной из 4-х кнопок
                            # 0 -> кнопка отжата - стоп
                            # 1 -> нажата кнопка влево
                            # 2 -> нажата кнопка вправо
                            # 3 -> нажата кнопка ввер
                            # 4 -> нажата кнопка вниз

        if event.type == pygame.KEYDOWN:  # проверка нажатия на клавиатуру
            if event.key == pygame.K_a:
                self.key_down = 1  # положене "1
            elif event.key == pygame.K_d:
                self.key_down = 2  # положене "2"
            elif event.key == pygame.K_w:
                self.key_down = 3  # положене "3"
            elif event.key == pygame.K_s:
                self.key_down = 4  # положене "4"

    def smooth_move(self, move_left, move_right, move_up, move_down):
        self.move_left = move_left  # флаг анимации движеия влево
        self.move_right = move_right  # флаг анимации движеия вправо
        self.move_up = move_up  # флаг анимации движеия вверх
        self.move_down = move_down  # флаг анимации движеия вниз

        if self.key_down == 1:
            if self.pacman_in_rect.x > 3:  # проверка на выход за пределы экрана
                self.pacman_in_rect.x -= 3  # шаг влево
                # Смена спрайта : анимация------------------------------
                if self.move_left:
                    self.pacman = pygame.image.load("pm-left-big.png")
                else:
                    self.pacman = pygame.image.load("pm-left-small.png")
                # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.key_down == 2:
            if self.pacman_in_rect.x < 797:  # проверка на выход за пределы экрана
                self.pacman_in_rect.x += 3  # шаг вправо
                # Смена спрайта : анимация------------------------------
                if self.move_right:
                    self.pacman = pygame.image.load("pm-right-big.png")
                else:
                    self.pacman = pygame.image.load("pm-right-small.png")
                # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.key_down == 3:
            if self.pacman_in_rect.y > 3:  # проверка на выход за пределы экрана
                self.pacman_in_rect.y -= 3  # шаг вверх
                # Смена спрайта : анимация------------------------------
                if self.move_up:
                    self.pacman = pygame.image.load("pm-up-big.png")
                else:
                    self.pacman = pygame.image.load("pm-up-small.png")
                # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.key_down == 4:
            if self.pacman_in_rect.y < 597:  # проверка на выход за пределы экрана
                self.pacman_in_rect.y += 3  # шаг вниз
                # Смена спрайта : анимация------------------------------
                if self.move_down:
                    self.pacman = pygame.image.load("pm-down-big.png")
                else:
                    self.pacman = pygame.image.load("pm-down-small.png")
                # ------------------------------------------------------


    def draw_object(self, screen):
        screen.blit(self.pacman, self.pacman_in_rect)  # отобразить объект


class Game:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]
        self.library_init()
        self.game_over = False
        self.create_game_objects()

        # разные параметры -------------
        self.move_left = False  # флаг анимации движеия влево
        self.move_right = False  # флаг анимации движеия вправо
        self.move_up = False  # флаг анимации движеия вверх
        self.move_down = False  # флаг анимации движеия вниз
                                # есть по две разные картинки на каждое направление (всего 8)
                                # в цикле значение меняется
                                # если флаг False, то рисуется 1 изображение
                                # если флаг True, то рисуется 2 изображени

        self.smooth_ghost_move = 0
        self.pacman_coordinate = []
        # ------------------------------

    def create_game_objects(self):
        self.A = Pacman(300, 50)
        self.G = Bots(50, 50, 'blue')

    def library_init(self):
        pygame.init()  # Инициализация библиотеки
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size)  # Создание окна (установка размера)

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
            # --------------------------------------------------

    def process_logic(self):  # логика объектов
        # действие движение --------------
        self.move_left = not self.move_left  # изменение значения флага
        self.move_right = not self.move_right  # изменение значения флага
        self.move_up = not self.move_up  # изменение значения флага
        self.move_down = not self.move_down  # изменение значения флага
        self.A.smooth_move(self.move_left, self.move_right, self.move_up, self.move_down)

        self.G.smooth_move()
        # -------------------------------

    def process_draw(self):
        self.screen.fill((0, 0, 0))
        self.A.draw_object(self.screen)
        self.G.draw_object(self.screen)
        pygame.display.flip()  # Double buffering
        pygame.time.wait(100)  # Ждать 100 миллисекунд


def main():
    pygame.font.init()  # ???
    g = Game()  # создания понятия как игра
    g.main_loop()  # запуск игры


if __name__ == '__main__':
    main()
