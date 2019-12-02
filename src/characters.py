import sys
import random

import pygame

from src.animations import Anim
from src.base_classes import DrawableObject
from src.constants import *
from src.enums import *
from src.food import Food


# Types of basic direction
class Dir:
    left = Vec(-1, 0)
    right = Vec(1, 0)
    up = Vec(0, -1)
    down = Vec(0, 1)


# Base class of Ghost
class Ghost(DrawableObject):
    old_f_pos: Vec
    f_pos: Vec
    g_rect: pygame.Rect
    target: Vec
    speed: float
    state: GhostState
    frightened_ticks: int
    vel: Vec

    def __init__(self, game_object, ghost_type: GhostType):
        super().__init__(game_object)

        # Load all ghosts sprites
        self.g_lib = self.game_object.ghosts_sprites
        # Choose ghost type
        self.ghost_type = ghost_type
        self.g_image = self.g_lib[ghost_type]
        self.e_image = self.g_lib['EYES_LEFT']
        # Animation
        self.a_move = Anim(['', '1'], 15)

        self.reset()

    def reset(self):

        # Get spawn pose
        spawn = self.game_object.field.get_cell_position(Vec(GHOSTS_POS[self.ghost_type]))
        self.g_rect = pygame.Rect(spawn.x - CELL_SIZE // 2, spawn.y, CELL_SIZE, CELL_SIZE)
        self.target = self.game_object.pacman.f_pos
        self.state = GhostState.chase
        self.frightened_ticks = 0
        self.vel = Vec(-1, 0) if self.ghost_type == GhostType.BLINKY else Vec(0, -1)
        self.speed = nearest_divisor_of_num(GHOST_SPEED, CELL_SIZE)
        self.f_pos = self.game_object.field.get_cell_from_position(Vec(self.g_rect.centerx, self.g_rect.centery)).f_pos

    def choose_way_by_dist(self, ways: []):
        dists = []
        for way in ways:
            r = self.f_pos + way
            dist = ((self.target.x - r.x) ** 2 + (self.target.y - r.y) ** 2) ** 0.5
            dists += [dist]
        way = ways[dists.index(min(dists))]
        return way

    def get_vec_of_move(self, g_type: GhostType, ways: []):
        if g_type == GhostType.BLINKY:  # Calculate behavior of BLINKY
            if self.state in [GhostState.chase, GhostState.frightened]:  # Go fast to point
                if self.f_pos == GHOSTS_POS[GhostType.PINKY]:
                    ways += [Dir.up]  # If blinky in house, now he can exit
                self.target = self.game_object.pacman.f_pos if self.state == GhostState.chase else Vec(31, 0)
                return self.choose_way_by_dist(ways)
            if self.state == GhostState.scatter:
                way = random.choice([ways.index(item) for item in ways if item])
                return way
        # Eaten state is the same for all types of ghosts
        if self.state == GhostState.eaten:
            self.target = Vec(GHOSTS_POS[GhostType.BLINKY])  # Need pinky position, but it'll do for now
            #if self.f_pos == GHOSTS_POS[GhostType.BLINKY]:
            #    ways += [Dir.down]  # Now ghost can enter the house
            return self.choose_way_by_dist(ways)

    def check_crit_pos(self):
        crit_pos = Vec((self.g_rect.x - self.game_object.field.offset.x) % CELL_SIZE,
                       (self.g_rect.y - self.game_object.field.offset.y) % CELL_SIZE)
        return 0 == crit_pos.x and 0 == crit_pos.y

    def move_to_target(self):
        self.g_rect.x += self.vel.x * self.speed
        self.g_rect.y += self.vel.y * self.speed
        self.check_teleportations()

    def check_teleportations(self):
        field_width = len(self.game_object.field.field[0]) * CELL_SIZE
        offset_x = self.game_object.field.offset.x
        # Check Left teleportation
        if self.g_rect.x < offset_x:
            self.g_rect.x = offset_x + field_width - CELL_SIZE - self.speed
        # Check Right teleportation=
        elif self.g_rect.right > offset_x + field_width - self.speed - 1:
            self.g_rect.x = self.game_object.field.offset.x

    # Animations)====================================================================================
    def set_eyes(self):
        curr_eyes = 'EYES_FR_2' if self.state == GhostState.frightened and \
                    pygame.time.get_ticks() - self.frightened_ticks > 6000 and \
                    ((pygame. time.get_ticks() - self.frightened_ticks) // 200) % 2 else \
            'EYES_FR_1' if self.state == GhostState.frightened else \
                'EYES_LEFT' if self.vel == Dir.left else \
                    'EYES_RIGHT' if self.vel == Dir.right else \
                        'EYES_DOWN' if self.vel == Dir.down else \
                            'EYES_UP'
        self.e_image = self.g_lib[curr_eyes]

    def set_body(self):
        anim = self.a_move.curr_sprite
        curr_body = 'ATTENT' + anim if self.state == GhostState.frightened and \
                    pygame.time.get_ticks() - self.frightened_ticks > 6000 and \
                    ((pygame. time.get_ticks() - self.frightened_ticks) // 200) % 2 else \
            'FRIGHTENED' + anim if self.state == GhostState.frightened else \
                self.ghost_type + anim
        self.g_image = self.g_lib[curr_body]

    # Base class methods)=============================================================================
    def process_event(self, event):
        pass

    def process_logic(self):
        # Hit pacman
        if self.game_object.pacman.hit_ghost(self):
            if self.state == GhostState.frightened:  # If hit pacman under energizer, pacman eat ghost
                self.game_object.pacman.eat_ghost_fruit(self)
                self.state = GhostState.eaten
            if self.state in [GhostState.chase, GhostState.scatter]:
                self.game_object.pacman.kill()

        # Animation
        self.a_move.add_tick()
        # Set eyes and body sprites
        self.set_eyes()
        self.set_body()

        # Frightened state
        if self.state == GhostState.frightened:
            self.speed = GHOST_SPEED // 2  # Set ghoast speed
            # Stop Frightening
            if pygame.time.get_ticks() - self.frightened_ticks > FRIGHTENED_TICKS_LIMIT:
                self.state = GhostState.chase
                self.frightened_ticks = 0

        # Eaten state
        elif self.state == GhostState.eaten:
            pass
            if self.f_pos == Vec(GHOSTS_POS[GhostType.BLINKY]):  # Need pinky position, but it'll do for now
                self.state = GhostState.chase
        else:
            self.speed = GHOST_SPEED  # Set ghoast speed

        # Movement
        if self.check_crit_pos():
            cell = self.game_object.field.get_cell_from_position(Vec(self.g_rect.centerx, self.g_rect.centery))
            self.old_f_pos = self.f_pos
            self.f_pos = cell.f_pos

            # Check around
            f = self.game_object.field.field
            pos = self.f_pos
            ways = [Vec(0, -1) if not f[pos.y - 1][pos.x].is_wall and pos + Vec(0, -1) != self.old_f_pos else None,
                    Vec(0, +1) if not f[pos.y + 1][pos.x].is_wall and pos + Vec(0, +1) != self.old_f_pos else None,
                    Vec(-1, 0) if not f[pos.y][pos.x - 1].is_wall and pos + Vec(-1, 0) != self.old_f_pos else None,
                    Vec(+1, 0) if not f[pos.y][pos.x + 1].is_wall and pos + Vec(1, 0) != self.old_f_pos else None]
            ways = [item for item in ways if item is not None]
            way = self.get_vec_of_move(GhostType.BLINKY, ways)
            self.vel = way

            if self.ghost_type == GhostType.BLINKY:
                self.move_to_target()

            pass  # Choose path
        else:
            if self.ghost_type == GhostType.BLINKY:
                self.move_to_target()

    def process_draw(self):
        ghost_size = CELL_SIZE * 2
        ghost_rect = pygame.Rect(self.g_rect.x - CELL_SIZE // 2, self.g_rect.y - CELL_SIZE // 2,
                                 self.g_rect.width + ghost_size, self.g_rect.height + ghost_size)
        # Draw ghost
        if self.state != GhostState.eaten:
            self.game_object.screen.blit(self.g_image, ghost_rect)

        # Draw his eyes
        self.game_object.screen.blit(self.e_image, ghost_rect)


# Base class of Pacman
class Pacman(DrawableObject):
    f_pos: Vec
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
        self.a_death = Anim(['D' + str(i) for i in range(11)] + ['D10'] * 20, 16)
        # Setup default variables in reset
        self.reset()

    # Setup default variables values
    def reset(self):
        self.f_pos = self.game_object.field.pacman_pos
        pac_pos = self.game_object.field.get_cell_position(self.f_pos)
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

    # Eating ghost
    def eat_ghost_fruit(self, obj):
        self.game_object.mixer.play_sound('GHOST' if isinstance(obj, Ghost) else 'FRUIT')
        self.game_object.scores += SCORE_FOR_GHOST
        while self.game_object.mixer.is_busy():
            self.game_object.screen.fill(BG_COLOR)  # Заливка цветом
            self.game_object.field.process_draw()  # Рисуем поле
            for food in self.game_object.food:
                if food != obj:  # Не рисуем съеденную еду
                    food.process_draw()  # Рисуем еду
            for ghost in self.game_object.ghosts:
                if ghost != obj:  # Не рисуем съеденного призрака
                    ghost.process_draw()  # Рисуем призраков
            self.game_object.hud.process_draw()  # Рисуем HUD
            text_pos = Vec(self.p_rect.center[0], self.p_rect.center[1])
            # Рисуем очки
            if isinstance(obj, Ghost):
                self.game_object.display_score_text(str(SCORE_FOR_GHOST), Color.CYAN, text_pos, 15)
            if isinstance(obj, Food):
                self.game_object.display_score_text(str(SCORE_FOR_FRUIT[obj.fruit_type]), Color.CYAN, text_pos, 15)
            # Флипаем экран
            pygame.display.flip()

    # return if pacman can move (there is no wall in the direction of movement)
    def check_position(self):
        crit_pos = Vec((self.p_rect.x - self.game_object.field.offset.x) % CELL_SIZE,
                       (self.p_rect.y - self.game_object.field.offset.y) % CELL_SIZE)
        if 0 == crit_pos.x and 0 == crit_pos.y:  # If pacman and cell pos equals
            cell = self.game_object.field.get_cell_from_position(Vec(self.p_rect.centerx, self.p_rect.centery))
            self.f_pos = cell.f_pos
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

    # Death of pacman
    def kill(self):
        self.game_object.lives -= 1
        self.game_object.hud.update_lives()

        if self.game_object.lives == 0:
            self.play_death_anim('GAME OVER!')
            self.game_object.game_over = True
        else:
            self.play_death_anim()
            for ghost in self.game_object.ghosts:
                ghost.reset()
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
            self.game_object.hud.process_draw()  # Рисуем HUD
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
