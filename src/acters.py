import pygame
import sys

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
        self.move_left = move_left      # флаг анимации движеия влево
        self.move_right = move_right    # флаг анимации движеия вправо
        self.move_up = move_up          # флаг анимации движеия вверх
        self.move_down = move_down      # флаг анимации движеия вниз
        
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
        # ------------------------------

    def create_game_objects(self):
        self.A = Pacman(50, 50)

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
        self.move_left = not self.move_left     # изменение значения флага
        self.move_right = not self.move_right   # изменение значения флага
        self.move_up = not self.move_up         # изменение значения флага
        self.move_down = not self.move_down     # изменение значения флага
        self.A.smooth_move(self.move_left, self.move_right, self.move_up, self.move_down)
        # --------------------------------

    def process_draw(self):
        self.screen.fill((0, 0, 0))
        self.A.draw_object(self.screen)
        pygame.display.flip()  # Double buffering
        pygame.time.wait(100)  # Ждать 100 миллисекунд
        
        
def main():
    pygame.font.init()  # ???
    g = Game()  # создания понятия как игра
    g.main_loop()  # запуск игры


if __name__ == '__main__':
    main()
