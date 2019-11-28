import pygame
from random import randrange
from src.base_classes import DrawableObject
from src.constants import *
from enum import Enum
import sys


# Types of basic direction
class Direction(Enum):
    right = 1
    left = 2
    up = 3
    down = 4


# Types of behavior of ghosts
class GostState(Enum):
    walk = 0
    persecution = 1
    go_home = 2
    waiting = 3


# Base class of Ghost
class Ghost(DrawableObject):
    def __init__(self, game_object, x, y, color):
        super().__init__(game_object)
        self.state = GostState.walk

        # выбор призрака       ---------------------------
        self.ghost = pygame.image.load(GHOSTS_SPRITE_LIB[color])
        # ------------------------------------------------------
        # координаты призрака ----------------------------------
        self.ghost_rect = self.ghost.get_rect()
        self.ghost_rect.x = x
        self.ghost_rect.y = y
        # ------------------------------------------------------

    def process_event(self, event):
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

    def process_logic(self):
        self.smooth_move()

    def smooth_move(self):
        self.count_of_steps = randrange(1, 4)
        self.random_direction = randrange(1, 5)  # рандомное направление
                                                 # 1 -> влево
                                                 # 2 -> вправо
                                                 # 3 -> вверх
                                                 # 4 -> вниз

        if self.random_direction == 1:  # влево
            for i in range(self.count_of_steps):
                if self.ghost_rect.x > 20:  # проверка на выход за пределы экрана
                    self.ghost_rect.x -= 5  # шаг

        if self.random_direction == 2:  # вправо
            for i in range(self.count_of_steps):
                if self.ghost_rect.x < 780:  # проверка на выход за пределы экрана
                    self.ghost_rect.x += 5  # шаг

        if self.random_direction == 3:  # вверх
            for i in range(self.count_of_steps):
                if self.ghost_rect.y > 20:  # проверка на выход за пределы экрана
                    self.ghost_rect.y -= 5  # шаг

        if self.random_direction == 4:  # вниз
            for i in range(self.count_of_steps):
                if self.ghost_rect.y < 580:  # проверка на выход за пределы экрана
                    self.ghost_rect.y += 5  # шаг

    def process_draw(self):
        self.game_object.screen.blit(self.ghost, self.ghost_rect)  # отобразить объект


# Base class of Pacman
class Pacman(DrawableObject):
    def __init__(self, game_object, x, y):
        super().__init__(game_object)
        # Initialize dict of used images
        self.images = self.game_object.pacman_sprites
        # Init pacman image and rect (DIRECTION = LEFT)
        self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], -180)
        self.p_rect = pygame.Rect(self.pacman_img.get_rect().move(x, y))
        # Setup default variables
        self.move_dir = Direction.left
        self.speed = PACMAN_SPEED

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:  # Check key down
            if event.key in [Input.A_LEFT, Input.LEFT]:  # Change directory to left
                self.move_dir = Direction.left
            elif event.key in [Input.A_RIGHT, Input.RIGHT]:
                self.move_dir = Direction.right
            elif event.key in [Input.A_UP, Input.UP]:
                self.move_dir = Direction.up
            elif event.key in [Input.A_DOWN, Input.DOWN]:
                self.move_dir = Direction.down

    def process_logic(self):  # логика объектов
        self.move()
        self.check_position()

    def process_draw(self):
        pac_size = CELL_SIZE * 2
        pac_img = pygame.transform.scale(self.pacman_img, (pac_size, pac_size))
        pac_rect = pygame.Rect(self.p_rect.x - CELL_SIZE // 2, self.p_rect.y - CELL_SIZE // 2,
                           self.p_rect.width + pac_size, self.p_rect.height + pac_size)
        self.game_object.screen.blit(pac_img, pac_rect)  # отобразить объект

    # Check collision rect of pacman with other rext
    def check_collision_with(self, other: pygame.Rect):
        return pygame.Rect(self.p_rect.x, self.p_rect.y, self.p_rect.width, self.p_rect.height)\
            .colliderect(pygame.Rect(other.x, other.y, other.width, other.height))

    def move(self):
        if self.move_dir == Direction.left:
            if True:
                self.p_rect.x -= self.speed  # шаг влево
                # Смена спрайта : анимация------------------------------
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], -180)
                # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.move_dir == Direction.right:
            if True:
                self.p_rect.x += self.speed * 1.2  # шаг вправо
                # Смена спрайта : анимация------------------------------
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], 0)
                # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.move_dir == Direction.up:
            if True:
                self.p_rect.y -= self.speed  # шаг вверх
                # Смена спрайта : анимация------------------------------
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], 90)
                # ------------------------------------------------------
        # --------------------------------------------------------------
        elif self.move_dir == Direction.down:
            if True:
                self.p_rect.y += self.speed * 1.2  # шаг вниз
                # Смена спрайта : анимация------------------------------
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], -90)
                # ------------------------------------------------------

    # return if pacman can move (there is no wall in the direction of movement)
    def check_position(self):
        crit_pos = Point((self.p_rect.x - self.game_object.field.offset.x) % CELL_SIZE,
                         (self.p_rect.y - self.game_object.field.offset.y) % CELL_SIZE)
        if 0 == crit_pos.x and 0 == crit_pos.y:  # If pacman and cell pos equals
            cell = self.game_object.field.get_cell_from_position(Point(self.p_rect.centerx, self.p_rect.centery))
            if cell and cell.food:
                cell.food.eat_up()
            return True
        return False

    """def check_field_collisions(self, pacman_speed):
        field = self.game_object.field
        p_x = self.p_rect.left + (pacman_speed if self.move_dir in [Direction.left, Direction.right] else 0)
        p_y = self.p_rect.top + (pacman_speed if self.move_dir in [Direction.up, Direction.down] else 0)
        p_size = self.p_rect.width

        for y in range(len(field.cells)):
            for x in range(len(field.cells[y])):
                if field.cells[y][x] == field.WALL_CODE:
                    cell_x, cell_y = field.offset[0] + x * field.cell_size, field.offset[1] + y * field.cell_size
                    # Строка внизу отвечает за дебаг
                    #pygame.draw.line(self.game_object.screen, Color.RED, (field.offset[0] + x * field.cell_size, field.offset[1] + y * field.cell_size), (p_x, p_y), 1)
                    if pygame.Rect(p_x, p_y, p_size, p_size).colliderect(pygame.Rect(cell_x, cell_y,
                                                                                     field.cell_size, field.cell_size)):
                        return False
        return True"""