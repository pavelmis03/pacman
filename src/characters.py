import pygame
from random import randrange
from src.base_classes import DrawableObject
from src.constants import *
from src.food import FoodType
from enum import Enum
import sys


# Types of basic direction
class Dir:
    left = Vec(-1, 0)
    right = Vec(1, 0)
    up = Vec(0, -1)
    down = Vec(0, 1)


# Types of behavior of ghosts
class GostState(Enum):
    frightened = 0
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
    speed: float
    vel: Vec
    turn_to: Vec

    def __init__(self, game_object, x, y):
        super().__init__(game_object)
        # Initialize dict of used images
        self.images = self.game_object.pacman_sprites
        # Init pacman image and rect (DIRECTION = LEFT)
        self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], -180)
        self.p_rect = pygame.Rect(self.pacman_img.get_rect().move(x, y))
        # Setup default variables in reset
        self.reset()

    # Setup default variables values
    def reset(self):
        pac_pos = self.game_object.field.get_cell_position(self.game_object.field.pacman_pos)
        self.p_rect.move(pac_pos.x - CELL_SIZE // 2, pac_pos.y)

        self.speed = PACMAN_SPEED
        self.vel = Vec(-self.speed, 0)
        self.turn_to = Vec(-self.speed, 0)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:  # Check key down
            if event.key in [Input.A_LEFT, Input.LEFT]:  # Change directory to left
                self.turn_to = Dir.left * self.speed  # LEFT
            elif event.key in [Input.A_RIGHT, Input.RIGHT]:
                self.turn_to = Dir.right * self.speed  # RIGHT
            elif event.key in [Input.A_UP, Input.UP]:
                self.turn_to = Dir.up * self.speed  # UP
            elif event.key in [Input.A_DOWN, Input.DOWN]:
                self.turn_to = Dir.down * self.speed  # DOWN

    def process_logic(self):  # логика объектов
        self.move()
        if self.check_position():
            self.p_rect.x += self.vel.x
            self.p_rect.y += self.vel.y
        else:
            cell = self.game_object.field.get_cell_from_position(Vec(self.p_rect.centerx, self.p_rect.centery))
            if cell and cell.food:
                # Eat dot
                cell.food.eat_up()
                if cell.food.type == FoodType.ENERGIZER:
                    # Set all ghosts to frightened
                    for ghost in self.game_object.ghosts:
                        ghost.state = GostState.frightened

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
        if self.vel == Dir.left:
            if True:
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], 0)
        elif self.vel == Dir.right:
            if True:
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], 0)
        elif self.vel == Dir.up:
            if True:
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], 0)
        elif self.vel == Dir.down:
            if True:
                self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], 0)

    # return if pacman can move (there is no wall in the direction of movement)
    def check_position(self):
        crit_pos = Vec((self.p_rect.x - self.game_object.field.offset.x) % CELL_SIZE,
                         (self.p_rect.y - self.game_object.field.offset.y) % CELL_SIZE)
        if 0 == crit_pos.x and 0 == crit_pos.y:  # If pacman and cell pos equals
            cell = self.game_object.field.get_cell_from_position(Vec(self.p_rect.centerx, self.p_rect.centery))
            #==================================================================================================
            # Eating food
            if cell and cell.food:
                # Eat dot
                if cell.food.type == FoodType.ENERGIZER:
                    # Set all ghosts to frightened
                    for ghost in self.game_object.ghosts:
                        ghost.state = GostState.frightened
                cell.food.eat_up()
            # ==================================================================================================
            # Movement
            f_pos = Vec(cell.f_pos.x, cell.f_pos.y)  # Pacman position in field
            pos_to_check = f_pos + self.turn_to  # Pos in field that the pacman is turning towards
            # Check if there is a free space in the direction that it is going to turn
            print(self.game_object.field.field[pos_to_check.y][pos_to_check.x].is_wall)
            if self.game_object.field.field[pos_to_check.y][pos_to_check.x].is_wall:
                if self.game_object.field.field[f_pos.y + self.vel.y][f_pos.x + self.vel.x].is_wall:
                    return False  # if neither are free then dont move
                else:
                    return True  # forward is free
            else:
                self.vel = self.turn_to
                return True  # Free to turn
        else:
            if self.turn_to.x + self.vel.x == 0 and self.vel.y + self.turn_to.y == 0:  # if turning chenging directions entirely i.e.180 degree turn
                self.vel = Vec(self.turn_to.x, self.turn_to.y)
            return True

    # return whether the input vector hits pacman
    def hit_ghost(self, ghost: Ghost):
        self_pos = Vec(self.p_rect.x, self.p_rect.y)
        ghost_pos = Vec(ghost.ghost_rect.x, ghost.ghost_rect.y)
        return self_pos.dist(ghost_pos)

    # called when a ghost hits pacman
    def kill(self):
        self.game_object.lives -= 1
        if self.game_object.lives == 0:
            self.game_object.game_over = True
        else:
            self.reset()
    """def check_field_collisions(self, pacman_speed):
        field = self.game_object.field
        p_x = self.p_rect.left + (pacman_speed if self.vel in [Direction.left, Direction.right] else 0)
        p_y = self.p_rect.top + (pacman_speed if self.vel in [Direction.up, Direction.down] else 0)
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