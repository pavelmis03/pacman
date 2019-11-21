import pygame
import sys

width = 800
height = 600
size = [width, height]

class Object:

    def __init__(self, x, y):
        pass

    def process_event(self, event):
        pass

    def smooth_move(self):
        pass

    def draw_object(self, screen):
        pass


class Pacman(Object):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.pacman = pygame.image.load("pm-right-small.png")
        self.pacman_in_rect = self.pacman.get_rect()
        self.pacman_in_rect.x = x
        self.pacman_in_rect.y = y

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
        elif event.type == pygame.KEYUP:  # проверка отжатия клавиатуры
            if event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
                self.key_down = 0  # положене "0"

    def smooth_move(self, move_left, move_right, move_up, move_down):
        self.move_left = move_left     # флаг анимации движеия влево
        self.move_right = move_right    # флаг анимации движеия вправо
        self.move_up = move_up       # флаг анимации движеия вверх
        self.move_down = move_down     # флаг анимации движеия вниз

        if self.key_down == 1:
            self.pacman_in_rect.x -= 2      # шаг влево
            if self.move_left:
                self.pacman = pygame.image.load("pm-left-big.png")
            else:
                self.pacman = pygame.image.load("pm-left-small.png")
            # -------------------------
        elif self.key_down == 2:
            self.pacman_in_rect.x += 2      # шаг вправо
            if self.move_right:
                self.pacman = pygame.image.load("pm-right-big.png")
            else:
                self.pacman = pygame.image.load("pm-right-small.png")
            # -------------------------
        elif self.key_down == 3:
            self.pacman_in_rect.y -= 2      # шаг вверх
            if self.move_up:
                self.pacman = pygame.image.load("pm-up-big.png")
            else:
                self.pacman = pygame.image.load("pm-up-small.png")
            # -------------------------
        elif self.key_down == 4:
            self.pacman_in_rect.y += 2      # шаг вниз
            if self.move_down:
                self.pacman = pygame.image.load("pm-down-big.png")
            else:
                self.pacman = pygame.image.load("pm-down-small.png")

    def draw_object(self, screen):
        screen.blit(self.pacman, self.pacman_in_rect)  # отобразить объект


def main():
    # начало -----------------------
    pygame.init()  # иницилизация библиотеки
    screen = pygame.display.set_mode(size)  # создание окна и установка размера
    game_over = False #флаг - проверка на выход
    # ------------------------------

    # создать объект ---------------
    A = Pacman(50, 50)
    # ------------------------------

    # разные параметры -------------
    move_left = False       # флаг анимации движеия влево
    move_right = False      # флаг анимации движеия вправо
    move_up = False         # флаг анимации движеия вверх
    move_down = False       # флаг анимации движеия вниз
                            # есть по две разные картинки на каждое направление (всего 8)
                            # в цикле значение меняется
                            # если флаг False, то рисуется 1 изображение
                            # если флаг True, то рисуется 2 изображени
    # ------------------------------
    
    # главный цикл ------------------------------------------------------
    while not game_over:                        # основной цикл программы

        # цикл событий --------------------------------------------------
        for event in pygame.event.get():        # получение всех событий
            # проверка события выхода ---------
            if event.type == pygame.QUIT:
                game_over = True
            # ---------------------------------

            # реализация плавного движения ---
            A.process_event(event)
            # --------------------------------
        # ---------------------------------------------------------------
        
        # действие движение --------------
        move_left = not move_left       # изменение значения флага
        move_right = not move_right     # изменение значения флага
        move_up = not move_up           # изменение значения флага
        move_down = not move_down       # изменение значения флага
        A.smooth_move(move_left, move_right, move_up, move_down)
        # --------------------------------

        # отображение ------------------------
        screen.fill((0, 0, 0))
        A.draw_object(screen)
        pygame.display.flip()  # double buffering
        pygame.time.wait(100)  # ждать 100 миллисекунд
        # ------------------------------------

    sys.exit()


if __name__ == '__main__':
    main()
