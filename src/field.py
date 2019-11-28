import pygame

from src.constants import *
from src.base_classes import DrawableObject
from src.food import Food, FoodType
from src.helpers import *


# Class of field's cell
class Cell(DrawableObject):
    def __init__(self, game_object, f_pos=Point(0, 0), g_pos=Point(0, 0), size=20, img=None):
        super().__init__(game_object)

        self.f_pos = f_pos  # Field x (0; 28) y (0; 31)
        self.g_pos = g_pos  # Global x (0; SCREEN_WIDTH) y (0; SCREEN_HEIGHT)
        self.size = size

        self.img = img
        self.is_wall = False
        self.is_door = False

    def get_rect(self):
        return pygame.Rect(self.g_pos.x, self.g_pos.y, self.size, self.size)

    def process_draw(self):
        if self.img:
            self.game_object.screen.blit(self.img, pygame.Rect(self.g_pos, Point(self.size, self.size)))

    def __repr__(self):
        return 'Cell: X{}, Y{}, WALL{}'.format(self.f_pos, self.g_pos, self.is_wall)


class Field(DrawableObject):
    def __init__(self, game_object, cell_size=CELL_SIZE, position=None):
        # MAP_SIZE IS 28x31
        super().__init__(game_object)
        if not position:
            position = [(SCREEN_WIDTH - cell_size * 28) // 2, 50]
        self.cell_size = cell_size
        self.offset = position
        self.pacman_pos = PACMAN_SPAWN_POS  # If 'decoder' find PACMAN_CODE on map, it put coordinates to this variable

        # Load all map sprites
        self.sprites = dict()
        for ch in WALL_CODES:
            self.sprites[ch] = pygame.transform.scale(pygame.image.load(MAP_SPRITES_DIR + ch + '.png'),
                                                      (self.cell_size, cell_size))

        # Map = array of chars
        self.map = FIELD_MAP
        # Field = array of Cells()
        self.field = []

        # Create map
        self.decode_map_to_field()

    # Convert list of strings(MAP) to field class
    def decode_map_to_field(self):
        for y in range(len(self.map)):
            self.field.append([])
            for x in range(len(self.map[y])):
                cell = Cell(self.game_object, Point(x, y), self.get_cell_position(Point(x, y)), self.cell_size)
                # Walls
                if self.map[y][x] in WALL_CODES:
                    cell.is_wall = True
                    cell.img = self.sprites[self.map[y][x]]
                # Door
                if self.map[y][x] == GHOSTS_ENTER_CODE:
                    cell.is_door = True
                # Door
                if self.map[y][x] == PACMAN_CODE:
                    self.pacman_pos = Point(x, y)
                self.field[y].append(cell)

    # Return global position of field's cell
    def get_cell_position(self, pos):
        return Point(self.offset[0] + self.cell_size * pos.x, self.offset[1] + self.cell_size * pos.y)

    # Decode food codes to Food classes and return getted list
    def get_food(self):
        food_objects = []
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                glob_x = self.offset[0] + x * self.cell_size
                glob_y = self.offset[1] + y * self.cell_size
                if self.map[y][x] == DOT_CODE:  # Food
                    food_objects.append(Food(self.game_object, self.cell_size, glob_x, glob_y, FoodType.DOT))
                elif self.map[y][x] == ENERGIZER_CODE:
                    food_objects.append(Food(self.game_object, self.cell_size, glob_x, glob_y, FoodType.ENERGIZER))
                elif self.map[y][x] == FRUIT_CODE:  # Food
                    food_objects.append(Food(self.game_object, self.cell_size, glob_x, glob_y, FoodType.FRUIT))
        return food_objects

    def draw_wall(self, pos):
        self.game_object.screen.blit(self.field[pos.y][pos.x].img, self.field[pos.y][pos.x].get_rect())

    # Draw door to ghosts house
    def draw_door(self, pos):
        cell = self.field[pos.y][pos.x]
        pygame.draw.line(self.game_object.screen, Color.DOTS_COLOR, (cell.get_rect().x, cell.get_rect().y + 16),
                         (cell.get_rect().x + cell.size, cell.get_rect().y + 16), 3)

    def process_draw(self):
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                cell = self.field[y][x]
                if cell.is_wall:  # Wall
                    self.draw_wall(Point(x, y))
                if cell.is_door:  # Door
                    self.draw_door(Point(x, y))
