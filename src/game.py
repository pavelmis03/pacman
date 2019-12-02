import sys
import pygame
from os import environ

from src.sound_engine import *
from src.menu import *
from src.hud import *
from src.field import Field
from src.characters import *


class Game:
    # region Prototypes of variables
    screen: pygame.display
    field: Field
    food: []
    ghosts: []
    map_sprites: []
    fruits_sprites: []
    pacman_sprites: []
    ghosts_sprites: []
    menu: MainMenu
    hud: HUD
    mixer: SoundMixer
    blinky: Ghost
    pinky: Ghost
    inky: Ghost
    clyde: Ghost
    pacman: Pacman

    # endregion Prototypes of variables

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.size = [width, height]
        self.library_init()
        self.init_sprite_libs()
        # Default variables
        self.game_over = False
        self.start_game = False
        self.lives = PACMAN_MAX_LIVES
        self.scores = 0

        self.objects = []
        self.create_game_objects()

        # Add mixer
        self.mixer = SoundMixer()  # Initialization of sound mixer

    def init_menu(self):
        # Play menu default music
        self.mixer.play_sound(random.choice(['MENU1', 'MENU2', 'MENU3']), -1)

        # Start Main menu First
        self.menu = MainMenu(self)
        self.menu.menu_loop()

        # Stop sound if we start game or close it
        self.mixer.stop_all_sounds()

    def create_game_objects(self):
        self.hud = HUD(self)
        self.field = Field(self)
        self.food = self.field.get_food()
        pac_pos = self.field.get_cell_position(self.field.pacman_pos)
        self.pacman = Pacman(self, pac_pos.x - CELL_SIZE // 2, pac_pos.y)  # Add some offset to centering pcaman
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
        # Create and move a window
        self.screen = pygame.display.set_mode(self.size, flags=pygame.DOUBLEBUF)  # Create window
        environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (1, 30)  # Move window to start coordinates
        # Set window caption
        pygame.display.set_caption('SHP Pacman')
        # Setup the icon
        icon = pygame.image.load(WINDOW_ICON_PATH)
        pygame.display.set_icon(icon)

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

    def display_center_text(self, text, color, flip=True):
        font = pygame.font.Font(FONT_PATH, SCORES_HUD_FONT_SIZE)
        s_text = font.render(text, 1, color)
        pos = self.field.get_cell_position(CENTER_TEXT_POS)
        half_len_text = SCORES_HUD_FONT_SIZE * len(text) // 2
        self.screen.blit(s_text, (pos.x - half_len_text, pos.y))
        if flip:
            pygame.display.flip()

    def display_score_text(self, text: str, color, c_pos: Vec, t_size: int):
        font = pygame.font.Font(FONT_PATH, t_size)
        s_text = font.render(text, 1, color)
        text_center_y = SCORES_HUD_FONT_SIZE // 2
        self.screen.blit(s_text, (c_pos.x, c_pos.y - text_center_y))

    def display_ready_screen(self):
        # Draw
        self.screen.fill(BG_COLOR)  # Заливка цветом
        self.process_draw()
        self.display_center_text('READY!', Color.YELLOW)
        # Play sound
        self.mixer.play_sound('GHOST')

        # Waiting for the START sound to play
        start_ticks = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_ticks < self.mixer.sounds['START'].get_length() * 100:
            for event in pygame.event.get():  # Обработка события выхода
                if event.type == pygame.QUIT:
                    sys.exit(0)

    def main_loop(self):
        # Start Main menu First
        self.init_menu()

        # Start menu loop
        while not self.start_game:
            self.menu.menu_loop()
        del self.menu

        # Draw Ready text and wait delay before start game
        self.display_ready_screen()

        # If user click START - start game
        while not self.game_over:  # Основной цикл работы программы
            self.game_update()

        # Game Over screen
        sys.exit(0)  # Выход из программы

    def game_update(self):
        self.mixer.process_query_of_sounds()  # need to process the query of sounds if it used
        self.process_events()
        self.process_logic()
        self.process_draw()

    def process_draw(self):
        for item in self.objects:
            item.process_draw()
        pygame.display.flip()  # Double buffering
        pygame.time.wait(SCREEN_RESPONSE)  # Ждать SCREEN_RESPONCE миллисекунд

    def process_logic(self):
        self.screen.fill(BG_COLOR)  # Заливка цветом
        for item in self.objects:
            item.process_logic()
        self.field.process_logic()

    def process_events(self):
        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:  # Обработка события выхода
                sys.exit(0)
            for item in self.objects:
                item.process_event(event)
