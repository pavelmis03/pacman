import sys
from cmath import inf

import pygame
from os import environ

from src.records_menu import RecordMenu
from src.sound_engine import *
from src.menu import *
from src.hud import *
from src.field import Field
from src.characters import *


class Game:
    # region Prototypes of variables
    screen: pygame.display
    field: Field
    objects: []
    food: []
    ghosts: []
    map_sprites: []
    fruits_sprites: []
    pacman_sprites: []
    ghosts_sprites: []
    map_spec_cells: []
    gh_start_poses: {}
    menu: MainMenu
    hud: HUD
    mixer: SoundMixer
    blinky: Ghost
    pinky: Ghost
    inky: Ghost
    clyde: Ghost
    pacman: Pacman
    lives: int
    scores: int
    music_choice: int
    eated_food: int
    change_level: bool
    game_over: bool
    start_game: bool
    current_map: str
    center_text_cell: Vec

    # endregion Prototypes of variables

    def __init__(self, width=size.DEF_SCREEN_SIZE.x, height=size.DEF_SCREEN_SIZE.y):
        self.width = width
        self.height = height
        self.size = [width, height]
        self.library_init()
        self.init_sprite_libs()
        # Default variables
        self.level = 1
        self.fruit = None
        self.fruit_lifetimer = 0

        self.reset()

    def change_music(self):
        self.music_choice = ((self.music_choice + 1) % MAX_MENU_MUSIC) + 1
        self.mixer.stop_all_sounds()
        self.mixer.play_sound('MENU' + str(self.music_choice), 0)

    def save_records(self, name):
        # Read
        with open(PATH_HIGHSCORES, 'r') as records:
            cur_table = dict()
            for line in records.readlines():
                cur_table[line.split(':')[0]] = int(line.split(':')[1])
        # Add
        if list(cur_table.keys()).count(str(name)) > 0:
            cur_table[str(name)] = self.scores if self.scores > cur_table[str(name)] else cur_table[str(name)]
        else:
            cur_table[str(name)] = self.scores

        # Write
        with open(PATH_HIGHSCORES, 'w') as records:
            for rec in cur_table.items():
                records.write(str(rec[0]) + ':' + str(rec[1]) + '\n')

    def update_lvl_bonus(self):
        #  Try to spawn bonus
        if (self.eated_food == (self.eated_food + len(self.food)) * 28//100 or
                self.eated_food == (self.eated_food + len(self.food)) * 69//100) and not self.fruit:
            cell = self.field.field[self.center_text_cell.y][self.center_text_cell.x - 1]
            self.fruit = Food(self, CELL_SIZE, cell.g_pos.x, cell.g_pos.y,
                              FoodType.FRUIT, REF_TABLE[self.level]['FRUIT'])
            cell.food = self.fruit
            self.food.append(self.fruit)
            self.objects.append(self.fruit)

            self.fruit_lifetimer = pygame.time.get_ticks()
            print('FRUIT SPAWNED! ' + str(self.fruit.fruit_type))
        # Remove bonus
        if self.fruit and pygame.time.get_ticks() - self.fruit_lifetimer > FRUIT_LIFETIME:
            cell = self.field.field[self.center_text_cell.y][self.center_text_cell.x - 1]
            self.food.remove(self.fruit)
            self.objects.remove(self.fruit)
            cell.food = None
            self.fruit = None

    # INITIALIZATION METHODS
    def reset(self, hard_reset=True):
        self.game_over = False
        self.start_game = False

        # Display main menu
        if hard_reset:
            # Start Main menu First
            self.init_menu()

            # Start menu loop
            while not self.start_game:
                self.menu.menu_loop()
            del self.menu

            # Drop mechanics variables
            self.lives = PACMAN_MAX_LIVES
            self.scores = 0
        # Set window caption
        pygame.display.set_caption('SHP Pacman')
        # Setup vars
        self.eated_food = 0
        self.objects = []
        self.gh_start_poses = {'BLINKY': Vec(999), 'PINKY': Vec(999), 'INKY': Vec(999), 'CLYDE': Vec(999)}
        self.map_spec_cells = []
        self.create_game_objects()
        self.change_level = False
        self.main_loop()

    def init_menu(self):
        # Set menu resolution
        size.resize(Vec(size.DEF_SCREEN_SIZE.x, size.DEF_SCREEN_SIZE.y))
        pygame.display.set_mode((size.DEF_SCREEN_SIZE.x, size.DEF_SCREEN_SIZE.y))
        # Play menu default music
        self.music_choice = random.randint(1, MAX_MENU_MUSIC)
        self.change_music()

        # Start Main menu First
        self.menu = MainMenu(self)
        self.menu.menu_loop()

        # Stop sound if we start game or close it
        self.mixer.stop_all_sounds()

    def create_game_objects(self):
        # Create hud, food, field
        self.field = Field(self, CELL_SIZE, l_map=self.current_map)
        size.resize(Vec(CELL_SIZE * len(self.field.field[0]),
                         (CELL_SIZE * len(self.field.field) + CELL_SIZE * 5)))
        pygame.display.set_mode((size.SCREEN_WIDTH, size.SCREEN_HEIGHT))

        self.hud = HUD(self)
        self.food = self.field.get_food()
        # Create pacman and ghosts
        pac_pos = self.field.get_cell_position(self.field.pacman_pos)
        x_offset = -CELL_SIZE // 2
        self.pacman = Pacman(self, pac_pos.x + x_offset, pac_pos.y)  # Add some offset to centering pcaman
        self.blinky = Ghost(self, GhostType.BLINKY)
        self.pinky = Ghost(self, GhostType.PINKY)
        self.inky = Ghost(self, GhostType.INKY)
        self.clyde = Ghost(self, GhostType.CLYDE)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

        # Add all food to object list
        for food in self.food:
            self.objects.append(food)

        self.objects += self.ghosts
        self.objects += [self.hud, self.field, self.pacman]

    def library_init(self):
        # Initialize all libs
        pygame.init()
        pygame.font.init()
        # Initialization of sound mixer
        self.mixer = SoundMixer()
        # Create and move a window
        self.screen = pygame.display.set_mode(self.size, flags=pygame.DOUBLEBUF)  # Create window
        environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (1, 30)  # Move window to start coordinates
        # Set window caption
        pygame.display.set_caption('SHP Pacman')
        # Setup the icon
        icon = pygame.image.load(WINDOW_ICON_PATH)
        pygame.display.set_icon(icon)

        # Load game config
        with open(CONFIG_PATH, 'r') as conf:
            c_lines = [row.replace('\n', '') for row in conf.readlines()]
            self.mixer.volume = float(c_lines[0].replace(' ', '').split(':')[1])  # Load music volume
            self.current_map = str(c_lines[1].replace(' ', '').split(':')[1])  # Load current map

    def init_sprite_libs(self):
        # Load all map sprite library
        self.map_sprites = dict()
        for ch in WALL_CODES:
            self.map_sprites[ch] = pygame.transform.scale(pygame.image.load(MAP_DIR + ch + '.png'),
                                                          (CELL_SIZE, CELL_SIZE))

        # Load all fruits sprite library(Need in Food class)
        self.fruits_sprites = dict()
        for ch in FRUIT_CODES:
            self.fruits_sprites[ch] = pygame.transform.scale(pygame.image.load(FRUITS_DIR + 'fruit' + ch + '.png'),
                                                             (CELL_SIZE * 2, CELL_SIZE * 2))

        # Load all pacman sprite library
        self.pacman_sprites = dict()
        for i in range(len(PAC_SPRITE_LIB.items())):
            self.pacman_sprites[list(PAC_SPRITE_LIB.items())[i][0]] = (
                pygame.transform.scale(pygame.image.load(list(PAC_SPRITE_LIB.items())[i][1]),
                                       (CELL_SIZE * 2, CELL_SIZE * 2)))

        # Load all ghosts sprite library
        self.ghosts_sprites = dict()
        for i in range(len(GHOSTS_SPRITE_LIB.items())):
            self.ghosts_sprites[list(GHOSTS_SPRITE_LIB.items())[i][0]] = (
                pygame.transform.scale(pygame.image.load(list(GHOSTS_SPRITE_LIB.items())[i][1]),
                                       (CELL_SIZE * 2, CELL_SIZE * 2)))

    # DISPLAY TEXTS
    def display_center_text(self, text, color, flip=True):
        font = pygame.font.Font(FONT_PATH, SCORES_HUD_FONT_SIZE)
        s_text = font.render(text, 1, color)
        pos = self.field.get_cell_position(self.center_text_cell)
        half_len_text = SCORES_HUD_FONT_SIZE * len(text) // 2
        self.screen.blit(s_text, (pos.x - half_len_text, pos.y))
        if flip:
            pygame.display.flip()

    def display_score_text(self, text: str, color, c_pos: Vec, t_size: int):
        font = pygame.font.Font(FONT_PATH, t_size)
        s_text = font.render(text, 1, color)
        text_center_y = SCORES_HUD_FONT_SIZE // 2
        self.screen.blit(s_text, (c_pos.x, c_pos.y - text_center_y))

    # UPDATES
    def main_loop(self):

        # Draw Ready text and wait delay before start game
        self.display_ready_screen()

        # If user click START - start game
        while not self.game_over and not self.change_level:  # Основной цикл работы программы
            self.game_update()

        # Change level
        if self.change_level:
            self.display_win_screen()
            self.level += 1
            self.reset(False)
        if self.game_over:
            self.display_lose_screen()
            self.out_rmenu = False
            record_menu = RecordMenu(self)
            while self.out_rmenu == False:
                record_menu.process_event(pygame.event.get())
                record_menu.process_logic()
                record_menu.process_draw()
            self.level = 1
            self.reset(True)
        print('BUG')

    def game_update(self):
        self.mixer.process_query_of_sounds()  # need to process the query of sounds if it used
        self.process_events()
        self.process_logic()
        self.process_draw()

    # SCREENS
    def display_ready_screen(self):
        # Draw
        self.screen.fill(BG_COLOR)  # Заливка цветом
        self.process_draw()
        self.display_center_text('READY!', Color.YELLOW)
        if not SKIP_CUTSCENES:
            # Play sound
            self.mixer.play_sound('START')

            # Waiting for the START sound to play
            start_ticks = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_ticks < self.mixer.sounds['START'].get_length() * 1000:
                for event in pygame.event.get():  # Обработка события выхода
                    if event.type == pygame.QUIT:
                        'YOU CLOSE PACMAN!'
                        sys.exit(0)
                for ghost in self.ghosts:
                    ghost.reset()

    def display_lose_screen(self):
        print('YOU LOSE(')
        self.mixer.stop_all_sounds()
        # Some delay (black field)
        wait_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - wait_time < 1000:
            self.screen.fill(BG_COLOR)
            pygame.display.flip()
            for event in pygame.event.get():  # Обработка всех событий
                if event.type == pygame.QUIT:  # Обработка события выхода
                    print('YOU CLOSE PACMAN!')
                    sys.exit(0)

        # Set menu resolution
        size.resize(Vec(size.DEF_SCREEN_SIZE.x, size.DEF_SCREEN_SIZE.y))
        pygame.display.set_mode((size.DEF_SCREEN_SIZE.x, size.DEF_SCREEN_SIZE.y))

    def display_win_screen(self):
        print('You win')
        # Some delay (pacman and field is visible)
        self.mixer.stop_all_sounds()
        delay_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - delay_time < 1500:  # 1.5 sec
            self.screen.fill(BG_COLOR)  # Заливка цветом
            self.field.process_draw()  # Рисуем поле
            self.pacman.process_draw()  # Рисуем пакмана
            self.hud.process_draw()  # Рисуем HUD
            if pygame.time.get_ticks() - delay_time > 400:
                pygame.display.flip()  # Флипаем экран если прошла небольшая задержка

        # Set menu resolution
        size.resize(Vec(size.DEF_SCREEN_SIZE.x, size.DEF_SCREEN_SIZE.y))
        pygame.display.set_mode((size.DEF_SCREEN_SIZE.x, size.DEF_SCREEN_SIZE.y))

        if not SKIP_CUTSCENES:
            # Play music
            self.mixer.play_sound('CUTSCENE', 2)

            # Play cutscene Ghost > Pacman
            pacman = Pacman(self, 0, 10)
            blinky = Ghost(self, GhostType.BLINKY)
            pacman.p_rect.right = size.SCREEN_WIDTH + 20
            blinky.g_rect.right = pacman.p_rect.right + blinky.g_rect.width + pacman.p_rect.width + 30
            pacman.p_rect.centery = size.SCREEN_CENTER[1]
            blinky.g_rect.centery = pacman.p_rect.centery
            b_speed = 0
            cutscene_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - cutscene_time < self.mixer.sounds['CUTSCENE'].get_length() * 1000:
                self.screen.fill(BG_COLOR)
                # FAKE PACMAN
                pacman.a_eat.add_tick()
                pacman.p_rect.x += Dir.left.x
                pacman.pacman_img = self.pacman_sprites[pacman.a_eat.curr_sprite]  # Переключаем спрайт
                pacman.pacman_img = pygame.transform.rotate(pacman.images[pacman.a_eat.curr_sprite], 180)
                pacman.process_draw()
                # FAKE GHOST
                blinky.a_move.add_tick()
                blinky.set_body()
                b_speed += 1
                blinky.g_rect.x += Dir.left.x - (1 if b_speed % 30 == 0 else 0)
                blinky.process_draw()
                pygame.display.flip()
                pygame.time.wait(SCREEN_RESPONSE * 2)  # Ждать SCREEN_RESPONCE миллисекунд

            # Play cutscene Pacman > Ghost
            pacman = Pacman(self, 0, 10)
            pacman.p_rect = pygame.transform.scale2x(pacman.images[pacman.a_eat.curr_sprite]).get_rect()
            blinky = Ghost(self, GhostType.BLINKY)
            pacman.p_rect.right = - pacman.p_rect.width * 2
            blinky.g_rect.right = pacman.p_rect.right + blinky.g_rect.width + pacman.p_rect.width
            pacman.p_rect.centery = size.SCREEN_CENTER[1]
            blinky.g_rect.centery = pacman.p_rect.centery
            p_speed = 0
            cutscene_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - cutscene_time < self.mixer.sounds['CUTSCENE'].get_length() * 1000:
                self.screen.fill(BG_COLOR)
                # FAKE PACMAN
                pacman.a_eat.add_tick()
                p_speed += 1
                pacman.p_rect.x += Dir.right.x + (1 if p_speed % 10 == 0 else 0)
                pacman.pacman_img = self.pacman_sprites[pacman.a_eat.curr_sprite]  # Переключаем спрайт
                pacman.pacman_img = pygame.transform.scale2x(pacman.images[pacman.a_eat.curr_sprite])
                pacman.process_draw()
                # FAKE GHOST
                blinky.vel = Dir.right
                blinky.a_move.add_tick()
                blinky.state = GhostState.frightened
                blinky.set_body()
                blinky.set_eyes()
                blinky.g_rect.x += Dir.right.x
                blinky.process_draw()
                pygame.display.flip()
                pygame.time.wait(SCREEN_RESPONSE)  # Ждать SCREEN_RESPONCE миллисекунд
                pygame.display.flip()
        # Some delay (black field)
        delay_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - delay_time < 1500:  # 1.5 sec
            self.screen.fill(BG_COLOR)  # Заливка цветом
            pygame.display.flip()  # Флипаем экран

    # =======================================BASE METHODS=======================================
    def process_events(self):
        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:  # Обработка события выхода
                print('YOU CLOSE PACMAN!')
                sys.exit(0)
            for item in self.objects:
                item.process_event(event)

    def process_logic(self):
        self.screen.fill(BG_COLOR)  # Заливка цветом для корректного отображения всех элементов

        # Запуск  process_logic() на всех объектах игры
        for item in self.objects:
            item.process_logic()

        # Обработка общей логики игры
        # Spawn fruits
        self.update_lvl_bonus()
        # End level
        if len(self.food) == 0:
            self.change_level = True

    def process_draw(self):
        for item in self.objects:
            item.process_draw()
        pygame.display.flip()  # Double buffering
        pygame.time.wait(SCREEN_RESPONSE)  # Ждать SCREEN_RESPONCE миллисекунд

    def __del__(self):
        # Save config
        with open(CONFIG_PATH, 'w') as conf:
            # Save music volume
            conf.write('MUSIC_VOLUME : {}'.format(self.mixer.volume))
            # Save current map
            conf.write('\nMAP : {}'.format(self.current_map if self.current_map else DEFAULT_MAP_FILE))
            # Wrie comment
            conf.write('\n#  Here you can change the name of the card on which you will play\
(in the way and in the name should not be spaces). You can change the value of \'MUSIC_VOLUME\', \
but this is useless as it will be overwritten when you turn IT off. Have fun :)')