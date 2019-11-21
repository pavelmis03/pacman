import pygame
import sys

width = 800
height = 600
size = [width, height]


def main():
    # начало -----------------------
    pygame.init()  # иницилизация библиотеки
    screen = pygame.display.set_mode(size)  # создание окна и установка размера
    screen.fill((0, 0, 0))
    game_over = False #флаг - проверка на выход
    # ------------------------------

    # создать объект ---------------
    square = pygame.Surface((20, 20))
    square.fill((255, 211, 0))
    # ------------------------------

    # главный цикл
    while not game_over:                        # основной цикл программы
        for event in pygame.event.get():        # получение всех событий
            if event.type == pygame.QUIT:       # проверка события выхода
                game_over = True

        screen.blit(square, (50, 70))  #отобразить объект
        pygame.display.flip()  # double buffering
        pygame.time.wait(50)  # ждать 50 миллисекунд
    sys.exit()

    
if __name__ == '__main__':
    main()

