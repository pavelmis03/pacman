import pygame
import sys

width = 800
height = 600
size = [width, height]


def main():
    # начало -----------------------
    pygame.init()  # иницилизация библиотеки
    screen = pygame.display.set_mode(size)  # создание окна и установка размера
    game_over = False #флаг - проверка на выход
    # ------------------------------

    # создать объект ---------------
    pacman = pygame.image.load("pm.png")
    pacman_in_rect = pacman.get_rect()
    # ------------------------------

    # разные параметры -------------
    pacman_in_rect.x = 50
    pacman_in_rect.y = 50
    
    key_down = 0  # флаг на нажатие одной из 4-х кнопок
                  # 0 -> кнопка отжата - стоп
                  # 1 -> нажата кнопка влево
                  # 2 -> нажата кнопка вправо
                  # 3 -> нажата кнопка ввер
                  # 4 -> нажата кнопка вниз
                  
    move_left = 0   # флаг анимации движеия влево
    move_right = 0  # флаг анимации движеия вправо
    move_up = 0     # флаг анимации движеия вверх
    move_down = 0   # флаг анимации движеия вниз
                    # есть по две разные картинки на каждое направление (всего 8)
                    # в цикле значение меняется
                    # если флаг четный, то рисуется 1 изображение
                    # если флаг нечетный, то рисуется 2 изображени

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
            if event.type == pygame.KEYDOWN:  # проверка нажатия на клавиатуру
                if event.key == pygame.K_a:
                    key_down = 1              # положене "1"
                elif event.key == pygame.K_d:
                    key_down = 2              # положене "2"
                elif event.key == pygame.K_w:
                    key_down = 3              # положене "3"
                elif event.key == pygame.K_s:
                    key_down = 4              # положене "4"
            elif event.type == pygame.KEYUP:  # проверка отжатия клавиатуры
                if event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
                    key_down = 0              # положене "0"
            # --------------------------------

        # ---------------------------------------------------------------

        # действие движение --------------
        if key_down == 1:
            pacman_in_rect.x -= 2      # шаг влево
            move_left += 1             # увеличение флага
            if move_left % 2 == 0:
                pacman = pygame.image.load("pm-left-big.png")
            else:
                pacman = pygame.image.load("pm-left-small.png")
            # -------------------------
        elif key_down == 2:
            pacman_in_rect.x += 2      # шаг вправо
            move_right += 1            # увеличение флага
            if move_right % 2 == 0:
                pacman = pygame.image.load("pm-right-big.png")
            else:
                pacman = pygame.image.load("pm-right-small.png")
            # -------------------------
        elif key_down == 3:
            pacman_in_rect.y -= 2      # шаг вверх
            move_up += 1               # увеличение флага
            if move_up % 2 == 0:
                pacman = pygame.image.load("pm-up-big.png")
            else:
                pacman = pygame.image.load("pm-up-small.png")
            # -------------------------
        elif key_down == 4:
            pacman_in_rect.y += 2      # шаг вниз
            move_down += 1             # увеличение флага
            if move_down % 2 == 0:
                pacman = pygame.image.load("pm-down-big.png")
            else:
                pacman = pygame.image.load("pm-down-small.png")
        # --------------------------------

        # отображение ------------------------
        screen.fill((0, 0, 0))
        screen.blit(pacman, pacman_in_rect)  # отобразить объект
        pygame.display.flip()  # double buffering
        pygame.time.wait(50)  # ждать 50 миллисекунд
        # ------------------------------------

    sys.exit()


if __name__ == '__main__':
    main()

