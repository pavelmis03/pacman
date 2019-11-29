import pygame

from src.constants import *
from src.base_classes import DrawableObject
from src.food import Food, FoodType
from src.helpers import *


# Class of field's cell
class Cell(DrawableObject):
    def __init__(self, game_object, f_pos=Vec(0, 0), g_pos=Vec(0, 0), size=20, img=None):
        super().__init__(game_object)

        self.f_pos = f_pos  # Field x (0; 28) y (0; 31)
        self.g_pos = g_pos  # Global x (0; SCREEN_WIDTH) y (0; SCREEN_HEIGHT)
        self.size = size

        self.img = img
        self.is_wall = False
        self.is_door = False

        self.food = None

    def get_rect(self):
        return pygame.Rect(self.g_pos.x, self.g_pos.y, self.size, self.size)

    def process_draw(self):
        if self.img:
            self.game_object.screen.blit(self.img, pygame.Rect(self.g_pos, Vec(self.size, self.size)))

    def __repr__(self):
        return 'Cell: X{}, Y{}, WALL{}'.format(self.f_pos, self.g_pos, self.is_wall)


class Field(DrawableObject):
    def __init__(self, game_object, cell_size=CELL_SIZE, position=None):
        # MAP_SIZE IS 28x31
        super().__init__(game_object)
        if not position:
            position = Vec((SCREEN_WIDTH - cell_size * 28) // 2, 50)
        self.cell_size = cell_size
        self.offset = position
        self.pacman_pos = PACMAN_SPAWN_POS  # If 'decoder' find PACMAN_CODE on map, it put coordinates to this variable

        # Load all map sprites
        self.sprites = self.game_object.map_sprites

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
                cell = Cell(self.game_object, Vec(x, y), self.get_cell_position(Vec(x, y)), self.cell_size)
                m_cell = self.map[y][x]
                # Walls
                if m_cell in WALL_CODES:
                    cell.is_wall = True
                    cell.img = self.sprites[m_cell]
                # Door
                if m_cell == GHOSTS_ENTER_CODE:
                    cell.is_wall = True
                    cell.is_door = True
                # Pacman
                if m_cell == PACMAN_CODE:
                    self.pacman_pos = Vec(x, y)
                # Food
                if m_cell == DOT_CODE:
                    cell.food = Food(self.game_object, self.cell_size, cell.g_pos.x, cell.g_pos.y, FoodType.DOT)
                if m_cell == ENERGIZER_CODE:
                    cell.food = Food(self.game_object, self.cell_size, cell.g_pos.x, cell.g_pos.y, FoodType.ENERGIZER)
                if m_cell in FRUIT_CODES:
                    cell.food = Food(self.game_object, self.cell_size, cell.g_pos.x, cell.g_pos.y, FoodType.FRUIT, m_cell)
                # Add cell to field
                self.field[y].append(cell)

    # Return global position of field's cell
    def get_cell_position(self, pos):
        return Vec(self.offset[0] + self.cell_size * pos.x, self.offset[1] + self.cell_size * pos.y)

    # Return field's cell using global pos
    def get_cell_from_position(self, pos: Vec):
        if self.offset.x < pos.x < self.offset.x + (len(self.field[0]) * self.cell_size) and \
                self.offset.y < pos.y < self.offset.y + (len(self.field) * self.cell_size):
            y = (pos.y - self.offset.y) // self.cell_size
            x = (pos.x - self.offset.x) // self.cell_size
            return self.field[y][x]
        else:
            return None

    # Decode food codes to Food classes and return getted list
    def get_food(self):
        food_objects = []
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                if self.field[y][x].food:
                    food_objects.append(self.field[y][x].food)
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
                if cell.is_wall and not cell.is_door:  # Wall
                    self.draw_wall(Vec(x, y))
                if cell.is_door:  # Door
                    self.draw_door(Vec(x, y))
