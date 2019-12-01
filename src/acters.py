import pygame
from random import randrange
import sys

class Bots:

    def __init__(self, x, y, color):
        self.ghost = pygame.image.load("dead-g-1.png")

        self.right_free = False  # идти в право пока свободно 
        self.left_free = False
        self.up_free = False
        self.down_free = False
        self.state = 0  # каким способом будет двигаться призрак (1, 2)

        # выбор цвета призрака       ---------------------------
        if color[0] == 'b':
            self.ghost = pygame.image.load("blue-g-left-1.png")
            self.right_free = True
            self.state = 1
        if color[0] == 'g':
            self.ghost = pygame.image.load("green-g-left-1.png")
            self.left_free = True
            self.state = 2
        if color[0] == 'r':
            self.ghost = pygame.image.load("red-g-left-1.png")
            self.up_free = True
            self.state = 1
        if color[0] == 'o':
            self.ghost = pygame.image.load("orange-g-left-1.png")
            self.down_free = True
            self.state = 2
        # ------------------------------------------------------
        # координаты призрака ----------------------------------
        self.ghost_in_rect = self.ghost.get_rect()
        self.ghost_in_rect.x = x
        self.ghost_in_rect.y = y
        # ------------------------------------------------------

    def process_event(self, event):
        pass

    def smooth_move(self):
        if self.state == 1:
            if self.right_free:
                if self.ghost_in_rect.x < 780:
                    self.ghost_in_rect.x += 5
                else:
                    self.right_free = False
                    self.left_free = True
            elif self.down_free:
                if self.ghost_in_rect.y < 580:
                    self.ghost_in_rect.y += 5
                else:
                    self.down_free = False
                    self.up_free = True
            elif self.left_free:
                if self.ghost_in_rect.x > 0:
                    self.ghost_in_rect.x -= 5
                else:
                    self.left_free = False
                    self.down_free = True
            elif self.up_free:
                if self.ghost_in_rect.y > 0:
                    self.ghost_in_rect.y -= 5
                else:
                    self.up_free = False
                    self.right_free = True
        elif self.state == 2:
            if self.right_free:
                if self.ghost_in_rect.x < 780:
                    self.ghost_in_rect.x += 5
                else:
                    self.right_free = False
                    self.down_free = True
            elif self.down_free:
                if self.ghost_in_rect.y < 580:
                    self.ghost_in_rect.y += 5
                else:
                    self.down_free = False
                    self.left_free = True
            elif self.left_free:
                if self.ghost_in_rect.x > 0:
                    self.ghost_in_rect.x -= 5
                else:
                    self.left_free = False
                    self.up_free = True
            elif self.up_free:
                if self.ghost_in_rect.y > 0:
                    self.ghost_in_rect.y -= 5
                else:
                    self.up_free = False
                    self.right_free = True

    def draw_object(self, screen):
        screen.blit(self.ghost, self.ghost_in_rect)  # отобразить объект


class Pacman:

    def __init__(self, x, y):
        self.pacman = pygame.image.load("pm.png")
        self.pacman_in_rect = self.pacman.get_rect()
        self.pacman_in_rect.x = x
        self.pacman_in_rect.y = y

        self.move_animation = 0  # Это флаг анимации. В цикле он постоянно меняется, растет на 1.
                                 # Теперь можно проверять его кратность тому или иному числу, в зависимости от того,
                                 # сколько картинок в анимации.

    def process_event(self, event):
        self.key_down = 0   # флаг на нажатие одной из 4-х кнопок
                            # 0 -> кнопка отжата - стоп
                            # 1 -> нажата кнопка влево
                            # 2 -> нажата кнопка вправо
                            # 3 -> нажата кнопка ввер
                            # 4 -> нажата кнопка вниз

        if event.type == pygame.KEYDOWN:  # проверка нажатия на клавиатуру
            if event.key == pygame.K_a:
                self.key_down = 1  # положене "1"
            elif event.key == pygame.K_d:
                self.key_down = 2  # положене "2"
            elif event.key == pygame.K_w:
                self.key_down = 3  # положене "3"
            elif event.key == pygame.K_s:
                self.key_down = 4  # положене "4"


    def smooth_move(self):
        self.move_animation += 1

        if self.key_down == 1:
            if self.pacman_in_rect.x > 3:  # проверка на выход за пределы экрана
                self.pacman_in_rect.x -= 3  # шаг влево
                # Смена спрайта : анимация------------------------------
                if self.move_animation % 2 == 0:
                    self.pacman = pygame.image.load("pm-left-big.png")
                else:
                    self.pacman = pygame.image.load("pm-left-small.png")
                # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.key_down == 2:
            if self.pacman_in_rect.x < 797:  # проверка на выход за пределы экрана
                self.pacman_in_rect.x += 3  # шаг вправо
                # Смена спрайта : анимация------------------------------
                if self.move_animation % 2 == 0:
                    self.pacman = pygame.image.load("pm-right-big.png")
                else:
                    self.pacman = pygame.image.load("pm-right-small.png")
                # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.key_down == 3:
            if self.pacman_in_rect.y > 3:  # проверка на выход за пределы экрана
                self.pacman_in_rect.y -= 3  # шаг вверх
                # Смена спрайта : анимация------------------------------
                if self.move_animation % 2 == 0:
                    self.pacman = pygame.image.load("pm-up-big.png")
                else:
                    self.pacman = pygame.image.load("pm-up-small.png")
                # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.key_down == 4:
            if self.pacman_in_rect.y < 597:  # проверка на выход за пределы экрана
                self.pacman_in_rect.y += 3  # шаг вниз
                # Смена спрайта : анимация------------------------------
                if self.move_animation % 2 == 0:
                    self.pacman = pygame.image.load("pm-down-big.png")
                else:
                    self.pacman = pygame.image.load("pm-down-small.png")
                # ------------------------------------------------------

    def draw_object(self, screen):
        screen.blit(self.pacman, self.pacman_in_rect)  # отобразить объект


class Game:
    def __init__(self, width = 800, height = 600):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]

        self.library_init()
        self.game_over = False
        self.create_game_objects()

        # разные параметры -------------
        self.smooth_ghost_move = 0
        self.pacman_coordinate = []
        # ------------------------------


    def create_game_objects(self):
        self.A = Pacman(300, 50)
        self.G1 = Bots(50, 50, 'blue')
        self.G2 = Bots(50, 70, 'red')
        self.G3 = Bots(50, 90, 'orange')
        self.G4 = Bots(50, 110, 'green')


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
        self.A.smooth_move()
        self.G1.smooth_move()
        self.G2.smooth_move()
        self.G3.smooth_move()
        self.G4.smooth_move()
        # -------------------------------

    def process_draw(self):
        self.screen.fill((0, 0, 0))
        self.A.draw_object(self.screen)
        self.G1.draw_object(self.screen)
        self.G2.draw_object(self.screen)
        self.G3.draw_object(self.screen)
        self.G4.draw_object(self.screen)
        pygame.display.flip()  # Double buffering
        pygame.time.wait(100)  # Ждать 100 миллисекунд


def main():
    pygame.font.init()  # ???
    g = Game()  # создания понятия как игра
    g.main_loop()  # запуск игры


if __name__ == '__main__':
    main()
