import pygame
from random import randrange

from src.animations import Anim
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
class GhostState(Enum):
    chase = 0
    scatter = 1
    eaten = 2
    frightened = 3


# Base class of Ghost
class Ghost(DrawableObject):
    state: GhostState

    def __init__(self, game_object, color):
        super().__init__(game_object)

        # Get spawn pose
        spawn = self.game_object.field.get_cell_position(Vec(GHOSTS_POS[color]))

        # Load all ghosts sprites
        self.images = self.game_object.pacman_sprites
        # Choose ghost type
        self.g_image = self.game_object.ghosts_sprites[color]
        self.e_image = self.game_object.ghosts_sprites['EYES_LEFT']
        self.g_rect = pygame.Rect(spawn.x - CELL_SIZE // 2, spawn.y, CELL_SIZE, CELL_SIZE)

        self.reset()

    def reset(self):
        self.state = GhostState.chase

    # Base class methods
    def process_event(self, event):
        pass

    def process_logic(self):
        if self.game_object.pacman.hit_ghost(self):
            self.game_object.pacman.kill()

    def process_draw(self):
        # Draw ghost
        ghost_size = CELL_SIZE * 2
        ghost_rect = pygame.Rect(self.g_rect.x - CELL_SIZE // 2, self.g_rect.y - CELL_SIZE // 2,
                                 self.g_rect.width + ghost_size, self.g_rect.height + ghost_size)
        self.game_object.screen.blit(self.g_image, ghost_rect)

        # Draw his eyes
        self.game_object.screen.blit(self.e_image, ghost_rect)


# Base class of Pacman
class Pacman(DrawableObject):
    speed: float
    vel: Vec
    turn_to: Vec
    eating: bool

    def __init__(self, game_object, x, y):
        super().__init__(game_object)
        # Initialize dict of used images
        self.images = self.game_object.pacman_sprites
        # Init pacman image and rect (DIRECTION = LEFT)
        self.pacman_img = pygame.transform.rotate(self.images['CLOSE'], -180)
        self.p_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        # Animations
        self.a_eat = Anim(['NORMAL', 'OPEN', 'NORMAL', 'CLOSE'], 5)
        self.a_death = Anim(['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D10', 'D10'], 20)
        # Setup default variables in reset
        self.reset()

    # Setup default variables values
    def reset(self):
        pac_pos = self.game_object.field.get_cell_position(self.game_object.field.pacman_pos)
        self.p_rect.x = pac_pos.x - CELL_SIZE // 2
        self.p_rect.y = pac_pos.y

        self.speed = nearest_divisor_of_num(PACMAN_SPEED, CELL_SIZE)
        self.vel = Vec(-1, 0)
        self.turn_to = Vec(-1, 0)

        self.eating = False

    def check_teleportations(self):
        field_width = len(self.game_object.field.field[0]) * CELL_SIZE
        offset_x = self.game_object.field.offset.x
        # Check Left teleportation
        if self.p_rect.x < offset_x:
            self.p_rect.x = offset_x + field_width - CELL_SIZE - self.speed
        # Check Right teleportation=
        elif self.p_rect.right > offset_x + field_width - self.speed - 1:
            self.p_rect.x = self.game_object.field.offset.x

    # Check collision rect of pacman with other rext
    def check_collision_with(self, other: pygame.Rect):
        return pygame.Rect(self.p_rect.x, self.p_rect.y, self.p_rect.width, self.p_rect.height) \
            .colliderect(pygame.Rect(other.x, other.y, other.width, other.height))

    def change_sprites(self):
        if self.vel == Dir.left:
            self.pacman_img = pygame.transform.rotate(self.images[self.a_eat.curr_sprite], 180)
        elif self.vel == Dir.right:
            self.pacman_img = pygame.transform.rotate(self.images[self.a_eat.curr_sprite], 0)
        elif self.vel == Dir.up:
            self.pacman_img = pygame.transform.rotate(self.images[self.a_eat.curr_sprite], 90)
        elif self.vel == Dir.down:
            self.pacman_img = pygame.transform.rotate(self.images[self.a_eat.curr_sprite], -90)

    # return if pacman can move (there is no wall in the direction of movement)
    def check_position(self):
        crit_pos = Vec((self.p_rect.x - self.game_object.field.offset.x) % CELL_SIZE,
                       (self.p_rect.y - self.game_object.field.offset.y) % CELL_SIZE)
        if 0 == crit_pos.x and 0 == crit_pos.y:  # If pacman and cell pos equals
            cell = self.game_object.field.get_cell_from_position(Vec(self.p_rect.centerx, self.p_rect.centery))
            # ==================================================================================================
            # Eating food
            if cell and cell.food:
                # DOTS
                if not self.eating:
                    if cell.food.type == FoodType.DOT:  # Don't chomping on fruits and enj-ers
                        self.game_object.mixer.play_sound('CHOMP', 0)
                        self.eating = True
                    else:
                        self.game_object.mixer.stop_sound('CHOMP')
                        self.eating = False
                # ENERGIZER
                if cell.food.type == FoodType.ENERGIZER:
                    # Set all ghosts to frightened
                    for ghost in self.game_object.ghosts:
                        ghost.state = GhostState.frightened
                cell.food.eat_up()
            else:
                # DOTS
                self.game_object.mixer.stop_sound('CHOMP')
                self.eating = False
            # ==================================================================================================
            # Movement
            f_pos = Vec(cell.f_pos.x, cell.f_pos.y)  # Pacman position in field
            pos_to_check = f_pos + self.turn_to  # Pos in field that the pacman is turning towards
            # Check if there is a free space in the direction that it is going to turn
            if self.game_object.field.field[pos_to_check.y][pos_to_check.x].is_wall:
                if self.game_object.field.field[f_pos.y + self.vel.y][f_pos.x + self.vel.x].is_wall:
                    return False  # if neither are free then dont move
                else:
                    # If you want some hard, uncommit the line below
                    # self.turn_to = self.vel
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
        ghost_pos = Vec(ghost.g_rect.x, ghost.g_rect.y)
        return self_pos.dist(ghost_pos) < CELL_SIZE

    # called when a ghost hits pacman
    def kill(self):
        self.game_object.lives -= 1
        self.game_object.hud.update_lives()

        if self.game_object.lives == 0:
            self.play_death_anim('GAME OVER!')
            self.game_object.game_over = True
        else:
            self.play_death_anim()
            self.reset()

    def play_death_anim(self, text=''):
        self.game_object.mixer.play_sound('DEATH')
        self.a_death.curr_sprite_num = 0
        while self.game_object.mixer.is_busy():  # PLAY DEATH ANIMATION
            self.game_object.screen.fill(BG_COLOR)  # Заливка цветом
            self.a_death.add_tick()  # Переключаем спрайт
            self.pacman_img = self.images[self.a_death.curr_sprite]  # Переключаем спрайт
            self.game_object.field.process_draw()  # Рисуем поле
            self.game_object.display_center_text(text, Color.RED, False)  # Рисуем текст
            for food in self.game_object.food: food.process_draw()  # Рисуем еду
            self.process_draw()  # Рисуем спрайт пакмана
            pygame.display.flip()  # Флипаем экран

    # Base class methods)=============================================================================
    def process_event(self, event):
        if event.type == pygame.KEYDOWN:  # Check key down
            if event.key in [Input.A_LEFT, Input.LEFT]:  # Change directory to left
                self.turn_to = Dir.left  # LEFT
            elif event.key in [Input.A_RIGHT, Input.RIGHT]:
                self.turn_to = Dir.right  # RIGHT
            elif event.key in [Input.A_UP, Input.UP]:
                self.turn_to = Dir.up  # UP
            elif event.key in [Input.A_DOWN, Input.DOWN]:
                self.turn_to = Dir.down  # DOWN

    def process_logic(self):  # логика объектов
        self.change_sprites()
        if self.check_position():
            self.a_eat.add_tick()
            self.p_rect.x += self.vel.x * self.speed
            self.p_rect.y += self.vel.y * self.speed
            self.check_teleportations()
        else:
            # If pacman hit the wall
            self.a_eat.curr_sprite = 'NORMAL'

    def process_draw(self):
        pac_size = CELL_SIZE * 2
        pac_rect = pygame.Rect(self.p_rect.x - CELL_SIZE // 2, self.p_rect.y - CELL_SIZE // 2,
                               self.p_rect.width + pac_size, self.p_rect.height + pac_size)
        self.game_object.screen.blit(self.pacman_img, pac_rect)  # отобразить объект
