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
    square = pygame.Surface((20, 20))
    square.fill((255, 211, 0))
    # ------------------------------

    # разные параметры -------------
    square_x = 50
    square_y = 50
    # ------------------------------

    # главный цикл ------------------------------------------------------
    while not game_over:                        # основной цикл программы
        for event in pygame.event.get():        # получение всех событий

            if event.type == pygame.QUIT:       # проверка события выхода
                game_over = True

            # реализация движения -------------
            if event.type == pygame.KEYDOWN:  # проверка нажатия на клавиатуру
                if event.key == pygame.K_a:
                    square_x -= 2             # шаг на 2 пикселя влево
                elif event.key == pygame.K_d:
                    square_x += 2             # шаг на 2 пикселя вправо
                elif event.key == pygame.K_w:
                    square_y -= 2             # шаг на 2 пикселя вверх
                elif event.key == pygame.K_s:
                    square_y += 2             # шаг на 2 пикселя вниз
            # --------------------------------

        # отображение ------------------------
        screen.fill((0, 0, 0))
        screen.blit(square, (square_x, square_y))  #отобразить объект
        pygame.display.flip()  # double buffering
        pygame.time.wait(50)  # ждать 50 миллисекунд
        # ------------------------------------

    sys.exit()


if __name__ == '__main__':
    main()

