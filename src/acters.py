import pygame
import sys

width = 800
height = 600
size = [width, height]


def main():
    # начало -----------------------
    pygame.init()  # иницилизация библиотеки
    screen = pygame.display.set_mode(size)  # создание окна и установка размера
    game_over = False  # флаг - проверка на выход
    # ------------------------------

    # создать объект ---------------
    square = pygame.Surface((20, 20))
    square.fill((255, 211, 0))
    # ------------------------------

    # разные параметры -------------
    square_x = 50
    square_y = 50

    key_down = 0  # флаг на нажатие одной из 4-х кнопок
                  # 0 -> кнопка отжата - стоп
                  # 1 -> нажата кнопка влево
                  # 2 -> нажата кнопка вправо
                  # 3 -> нажата кнопка ввер
                  # 4 -> нажата кнопка вниз
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
            square_x -= 2  # шаг влево
        elif key_down == 2:
            square_x += 2  # шаг вправо
        elif key_down == 3:
            square_y -= 2  # шаг вверх
        elif key_down == 4:
            square_y += 2  # шаг вниз
        # --------------------------------

        # отображение ------------------------
        screen.fill((0, 0, 0))
        screen.blit(square, (square_x, square_y))  # отобразить объект
        pygame.display.flip()  # double buffering
        pygame.time.wait(50)  # ждать 50 миллисекунд
        # ------------------------------------

    sys.exit()


if __name__ == '__main__':
    main()


