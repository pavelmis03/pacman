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
    next_state: GhostState
    behaviour_state: GhostState
    frightened_ticks: int
    vel: Vec
    waiting_time: int
    spawned_time: int
    sc_change_time: int
    sc_change_mode: int
    lvl_sc_changer_key: str

    def __init__(self, game_object, ghost_type: GhostType):
        super().__init__(game_object)

        # Load all ghosts sprites
        self.g_lib = self.game_object.ghosts_sprites
        # Load font
        self.font = pygame.font.Font(FONT_PATH, 8)
        # Choose ghost type
        self.ghost_type = ghost_type
        self.g_image = self.g_lib[ghost_type]
        self.e_image = self.g_lib['EYES_LEFT']
        # Animation
        self.a_move = Anim(['', '1'], 15)

        self.reset()

    def reset(self):

        # Get spawn pose
        spawn = self.game_object.field.get_cell_position(GHOSTS_POS[self.ghost_type])
        self.g_rect = pygame.Rect(spawn.x, spawn.y, CELL_SIZE, CELL_SIZE)
        self.target = self.game_object.pacman.f_pos
        self.state = GhostState.waiting
        self.next_state = GhostState.waiting
        self.frightened_ticks = 0
        self.vel = Dir.left if self.ghost_type == GhostType.BLINKY else Dir.up
        self.speed = nearest_divisor_of_num(GHOST_SPEED, CELL_SIZE)
        self.f_pos = self.game_object.field.get_cell_from_position(Vec(self.g_rect.centerx, self.g_rect.centery)).f_pos
        self.waiting_time = WAITING_TIME[self.ghost_type]
        self.spawned_time = pygame.time.get_ticks()

        # Find Blinky reference for inky
        self.ref_to_blinky = None

        # Scatter - chase
        self.behaviour_state = GhostState.scatter
        self.sc_change_time = self.spawned_time
        self.sc_change_mode = 0
        if self.game_object.level == 1:
            self.lvl_sc_changer_key = 'LVL1'
        elif 2 <= self.game_object.level <= 4:
            self.lvl_sc_changer_key = 'LVL2-4'
        else:
            self.lvl_sc_changer_key = 'LVL5+'

    def find_ref_to_blinky(self):
        for gh in self.game_object.ghosts:
            if gh.ghost_type == GhostType.BLINKY:
                self.ref_to_blinky = gh

    def clyde_out_8_cells(self):
        p = self.game_object.pacman.f_pos
        c = self.f_pos
        dist = int(((p.x - c.x) ** 2 + (p.y - c.y) ** 2) ** 0.5)
        return dist > 8

    def set_frightened_state(self):
        if self.state not in [GhostState.eaten, GhostState.waiting]:
            self.state = GhostState.frightened
            self.frightened_ticks = pygame.time.get_ticks()

    def choose_way_by_dist(self, ways: []):
        dists = []
        if len(ways) == 0:
            print('[ERROR]: ', self.ghost_type, self.f_pos)
        for way in ways:
            r = self.f_pos + way
            dist = ((self.target.x - r.x) ** 2 + (self.target.y - r.y) ** 2) ** 0.5
            dists += [dist]
        res = [ways[i] for i in range(len(dists)) if dists[i] == min(dists)]
        out = Dir.up if res.count(Dir.up) > 0 else \
              Dir.left if res.count(Dir.left) > 0 else \
              Dir.down if res.count(Dir.down) > 0 else \
              Dir.right if res.count(Dir.right) > 0 else None
        return out  # Prioritets: up, left, down, right

    def get_vec_of_move(self, g_type: GhostType, ways: []):
        res_way = Vec(0, 0)
        p_pos = GHOSTS_POS[GhostType.PINKY]

        # Ways where ghost can't go up
        if self.f_pos in GHOSTS_UP_BLOCKED_CELLS:
            if Dir.up in ways:
                ways.remove(Dir.up)

        # Calculate behavior of BLINKY
        if g_type == GhostType.BLINKY:
            if self.state in [GhostState.chase, GhostState.scatter]:  # Go fast to point
                self.target = self.game_object.pacman.f_pos if self.state == GhostState.chase else BLINKY_S_TARGET
                res_way = self.choose_way_by_dist(ways)
            if self.state == GhostState.frightened:
                way = random.choice([item for item in ways if item])
                res_way = way
            if self.state == GhostState.eaten:
                self.target = GHOSTS_POS[GhostType.BLINKY]
                res_way = self.choose_way_by_dist(ways)
        # Calculate behavior of PINKY
        if g_type == GhostType.PINKY:
            if self.state in [GhostState.chase, GhostState.scatter]:  # Go fast to point
                if self.f_pos in [p_pos, p_pos + Vec(0, -1), p_pos + Vec(-1, 0), p_pos + Vec(-1, -1)]:
                    ways += [Dir.up]  # If pinky in house, now he can exit
                if self.state == GhostState.chase:
                    self.target = self.game_object.pacman.f_pos + self.game_object.pacman.vel * 4
                    if self.game_object.pacman.vel == Dir.up:
                        self.target += Vec(-4, 0)
                else:
                    self.target = PINKY_S_TARGET
                res_way = self.choose_way_by_dist(ways)
            if self.state == GhostState.frightened:
                way = random.choice([item for item in ways if item])
                res_way = way
        # Calculate behavior of INKY
        if g_type == GhostType.INKY:
            if self.state in [GhostState.chase, GhostState.scatter]:  # Go fast to point
                if self.f_pos in HOUSE_CELLS:
                    ways += [Dir.up]  # If inky in house, now he can exit
                if self.state == GhostState.chase:
                    self.target = self.game_object.pacman.f_pos + self.game_object.pacman.vel * 2
                    if self.game_object.pacman.vel == Dir.up:
                        self.target += Vec(-2, 0)
                    # Mirroring besides blinky
                    if self.ref_to_blinky:
                        x = self.target.x - self.ref_to_blinky.f_pos.x
                        y = self.target.y - self.ref_to_blinky.f_pos.y
                        self.target += Vec(x, y)
                    else:
                        self.find_ref_to_blinky()
                else:
                    self.target = INKY_S_TARGETT
                res_way = self.choose_way_by_dist(ways)
            if self.state == GhostState.frightened:
                way = random.choice([item for item in ways if item])
                res_way = way
        # Calculate behavior of CLYDE
        if g_type == GhostType.CLYDE:
            if self.state in [GhostState.chase, GhostState.scatter]:  # Go fast to point
                if self.f_pos in HOUSE_CELLS:
                    ways += [Dir.up]  # If inky in house, now he can exit
                if self.state == GhostState.chase:
                    if self.clyde_out_8_cells():
                        self.target = self.game_object.pacman.f_pos
                    else:
                        self.target = CLYDE_S_TARGETT
                else:
                    self.target = CLYDE_S_TARGETT
                res_way = self.choose_way_by_dist(ways)
            if self.state == GhostState.frightened:
                way = random.choice([item for item in ways if item])
                res_way = way

        # Eaten state is the same for all types of ghosts
        if self.state == GhostState.eaten and self.ghost_type != GhostType.BLINKY:
            self.target = GHOSTS_POS[GhostType.PINKY]
            b_pos = GHOSTS_POS[GhostType.BLINKY]
            if self.f_pos in [b_pos, b_pos + Vec(-1, 0)]:
                ways += [Dir.down]  # Now ghost can enter the house
            if self.f_pos in [GHOSTS_POS[GhostType.PINKY], GHOSTS_POS[GhostType.PINKY] + Vec(-1, 0)]:
                ways = [Dir.up]
            res_way = self.choose_way_by_dist(ways)

        # If ghosts house
        # Ghost in house and want to exit
        if self.state in [GhostState.chase, GhostState.scatter] and self.f_pos in \
                [p_pos, p_pos + Vec(0, -1), p_pos + Vec(-1, 0), p_pos + Vec(-1, -1)]:
            res_way = Dir.up
        # Ghost in edge of house
        if self.state in [GhostState.chase, GhostState.scatter] and self.f_pos in \
                [p_pos + Vec(-1, 0), p_pos + Vec(-2, 0)]:
            res_way = Dir.right
        if self.state in [GhostState.chase, GhostState.scatter] and self.f_pos in \
                [p_pos + Vec(+1, 0), p_pos + Vec(+2, 0)]:
            res_way = Dir.left
        return res_way

    def check_crit_pos(self):
        crit_pos = Vec((self.g_rect.x - self.game_object.field.offset.x) % CELL_SIZE,
                       (self.g_rect.y - self.game_object.field.offset.y) % CELL_SIZE)
        return crit_pos.x == 0 and crit_pos.y == 0

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
        field_height = len(self.game_object.field.field) * CELL_SIZE
        offset_y = self.game_object.field.offset.y
        # Check Left teleportation
        if self.g_rect.y < offset_y:
            self.g_rect.y = offset_y + field_height - CELL_SIZE - self.speed
        # Check Right teleportation=
        elif self.g_rect.bottom > offset_y + field_height - self.speed - 1:
            self.g_rect.y = self.game_object.field.offset.y

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
                str(self.ghost_type) + anim
        self.g_image = self.g_lib[curr_body]

    # Base class methods)=============================================================================
    def process_event(self, event):
        pass

    def process_logic(self):
        if self.next_state != GhostState.eaten:
            self.next_state = self.state

        if self.state == GhostState.waiting and pygame.time.get_ticks() - self.spawned_time < self.waiting_time:
            pass
        else:
            if self.state == GhostState.waiting:
                self.state = self.behaviour_state
            # Animation
            self.a_move.add_tick()
            # Set eyes and body sprites
            self.set_eyes()
            self.set_body()

            # Scatter - chase
            if pygame.time.get_ticks() - self.sc_change_time > SC_CH_TURNS[self.lvl_sc_changer_key][self.sc_change_mode]:
                self.sc_change_time = pygame.time.get_ticks()
                self.sc_change_mode += 1
                self.behaviour_state = GhostState.chase if self.sc_change_mode % 2 else \
                    GhostState.scatter
                if self.state in [GhostState.scatter, GhostState.chase]:
                    self.state = self.behaviour_state
                    self.next_state = self.state
            # STATES===================================================================================
            # Hit pacman
            if self.game_object.pacman.hit_ghost(self):
                if GhostState.frightened in [self.state]:  # If hit pacman under energizer, pacman eat ghost
                    self.next_state = GhostState.eaten
                if self.state in [GhostState.chase, GhostState.scatter]:
                    self.game_object.pacman.kill()
            # Ghost on center
            if self.check_crit_pos():
                # STATES===================================================================================
                if self.next_state != self.state:
                    if self.next_state == GhostState.eaten:
                        self.game_object.pacman.eat_ghost_fruit(self)
                        self.state = GhostState.eaten
                    elif self.next_state in [GhostState.scatter, GhostState.chase]:
                        self.state = self.behaviour_state
                        self.next_state = self.state
                # Frightened state
                if self.state == GhostState.frightened:
                    self.speed = GHOST_SPEED // 2 if GHOST_SPEED > 1 else 1  # Set ghost speed
                    # Stop Frightening
                    if pygame.time.get_ticks() - self.frightened_ticks > FRIGHTENED_TICKS_LIMIT:
                        self.state = self.behaviour_state
                        self.frightened_ticks = 0

                # Eaten state
                elif self.state == GhostState.eaten:
                    self.speed = GHOST_SPEED * 2  # Set ghost speed
                    if self.ghost_type == GhostType.BLINKY and self.f_pos == GHOSTS_POS[GhostType.BLINKY]:
                        self.state = self.behaviour_state
                        self.next_state = self.state
                    elif self.f_pos == GHOSTS_POS[GhostType.PINKY]:
                        self.state = self.behaviour_state
                        self.next_state = self.state
                else:
                    self.speed = GHOST_SPEED  # Set ghost speed

                # Movement (Ghost on center)=====================================================================
                cell = self.game_object.field.get_cell_from_position(Vec(self.g_rect.centerx, self.g_rect.centery))
                self.old_f_pos = self.f_pos
                self.f_pos = cell.f_pos

                # Check around
                f = self.game_object.field.field
                pos = self.f_pos
                ways = [Dir.up if not f[pos.y - 1][pos.x].is_wall and pos + Dir.up != self.old_f_pos else None,
                        Dir.down if not f[pos.y + 1][pos.x].is_wall and pos + Dir.down != self.old_f_pos else None,
                        Dir.left if not f[pos.y][pos.x - 1].is_wall and pos + Dir.left != self.old_f_pos else None,
                        Dir.right if not f[pos.y][pos.x + 1].is_wall and pos + Dir.right != self.old_f_pos else None]
                ways = [item for item in ways if item is not None]
                way = self.get_vec_of_move(self.ghost_type, ways)
                self.vel = way

            self.move_to_target()

    def process_draw(self):
        ghost_size = CELL_SIZE * 2
        ghost_rect = pygame.Rect(self.g_rect.x - CELL_SIZE // 2, self.g_rect.y - CELL_SIZE // 2,
                                 self.g_rect.width + ghost_size, self.g_rect.height + ghost_size)
        if self.state == GhostState.waiting:
            ghost_rect.move_ip(-CELL_SIZE // 2, 0)
        # Draw ghost
        if self.state != GhostState.eaten:
            self.game_object.screen.blit(self.g_image, ghost_rect)

        # Draw his eyes
        self.game_object.screen.blit(self.e_image, ghost_rect)

        # Show ghost targets
        if SHOW_GHOSTS_TARGETS and self.target:
            x = (self.target.x * CELL_SIZE) + self.game_object.field.offset.x
            y = (self.target.y * CELL_SIZE) + self.game_object.field.offset.y
            clr = Color.RED if self.ghost_type == 'BLINKY' else Color.PINKY if self.ghost_type == 'PINKY' else \
                Color.BLUE if self.ghost_type == 'INKY' else Color.ORANGE
            # [TARGET] text
            text = self.font.render('[TARGET]', 1, clr)
            self.game_object.screen.blit(text, (x - 15, y - 20))
            # CROSS
            pygame.draw.line(self.game_object.screen, clr, (x + 5, y + 5), (x + CELL_SIZE - 5, y + CELL_SIZE - 5), 5)
            pygame.draw.line(self.game_object.screen, clr, (x + CELL_SIZE - 5, y + 5), (x + 5, y + CELL_SIZE - 5), 5)
            # OTHER (CLYDE CIRCLE)
            p_pos = self.game_object.pacman.f_pos
            f_offset = self.game_object.field.offset
            c_pos = Vec(p_pos.x * CELL_SIZE + f_offset.x, p_pos.y * CELL_SIZE + f_offset.y + CELL_SIZE // 2)
            if self.ghost_type == GhostType.CLYDE:
                pygame.draw.circle(self.game_object.screen, clr, (c_pos.x, c_pos.y), CELL_SIZE * 8, 5)


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
        slow_mo_ticks = pygame.time.get_ticks()  # Timer for slow mo
        limit = SLOW_MO_TICKS_LIMIT if isinstance(obj, Ghost) else SLOW_MO_TICKS_LIMIT * 2 // 3  # 2/3 of normal if fru
        while pygame.time.get_ticks() - slow_mo_ticks < limit:
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
        self.game_object.mixer.stop_all_sounds()
        self.game_object.mixer.play_sound('DEATH')
        self.a_death.curr_sprite_num = 0
        death_ticks = pygame.time.get_ticks()
        while pygame.time.get_ticks() - death_ticks < DEATH_TICKS_LIMIT:  # PLAY DEATH ANIMATION
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
