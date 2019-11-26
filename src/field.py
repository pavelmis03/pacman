import pygame

from src.constants import *
from src.base_classes import DrawableObject
from src.food import Food, FoodType


class Field(DrawableObject):
    def __init__(self, game_object, cell_size=18, position=None):
        # MAP_SIZE IS 28x31
        super().__init__(game_object)
        if not position:
            position = [(SCREEN_WIDTH - cell_size * 28) // 2, 50]
        self.cell_size = cell_size
        self.offset = position
        self.cells = FIELD_MAP
        self.WALL_CODE = '#'
        self.ENERGIZER_CODE = '@'
        self.POINT_CODE = '.'
        self.FRUIT_CODE = '$'
        self.GHOSTS_ENTER_CODE = '-'
        self.bump = 2  # Wall bump

    def get_food(self):
        food_objects = []
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                x = self.offset[0] + j * self.cell_size
                y = self.offset[1] + i * self.cell_size
                if self.cells[i][j] == self.POINT_CODE:  # Food
                    food_objects.append(Food(self.game_object, self.cell_size, x, y, FoodType.POINT))
                elif self.cells[i][j] == self.ENERGIZER_CODE:
                    food_objects.append(Food(self.game_object, self.cell_size, x, y, FoodType.ENERGIZER))
                elif self.cells[i][j] == self.FRUIT_CODE:  # Food
                    food_objects.append(Food(self.game_object, self.cell_size, x, y, FoodType.FRUIT))
        return food_objects

    def is_cell(self, ij):
        i, j = ij
        i = i >= 0 and i < len(self.cells)
        j = j >= 0 and j < len(self.cells[i])
        return i and j

    def is_wall(self, ij):
        i, j = ij
        return self.cells[i][j] == self.WALL_CODE

    def get_around(self, i, j):
        top = [i-1, j]
        topright = [i-1, j+1]
        right = [i, j+1]
        bottomright = [i+1, j+1]
        bottom = [i+1, j]
        bottomleft = [i+1, j-1]
        left = [i, j-1]
        topleft = [i-1, j-1]
        return [(coords if self.is_cell(coords) else False) for coords in [top, topright, right, bottomright, bottom, bottomleft, left, topleft]]

    def draw_wall(self, x, y, i, j):
        around = self.get_around(i, j)
        halfcell = self.cell_size // 2
        # centers:
        cx, cy = x + halfcell, y + halfcell
        if around[0] and self.is_wall(around[0]):
            # TOP
            pygame.draw.line(self.game_object.screen, Color.BLUE, (cx, cy), (cx, cy - halfcell), 2)
        if around[2] and self.is_wall(around[2]):
            # RIGHT
            pygame.draw.line(self.game_object.screen, Color.BLUE, (cx, cy), (cx + halfcell, cy), 2)
        if around[4] and self.is_wall(around[4]):
            # BOTTOM
            pygame.draw.line(self.game_object.screen, Color.BLUE, (cx, cy), (cx, cy + halfcell), 2)
        if around[6] and self.is_wall(around[6]):
            # LEFT
            pygame.draw.line(self.game_object.screen, Color.BLUE, (cx, cy), (cx - halfcell, cy), 2)

    def process_draw(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                x = self.offset[0] + j * self.cell_size
                y = self.offset[1] + i * self.cell_size
                # Draw wall
                if self.cells[i][j] == self.WALL_CODE:
                    self.draw_wall(x, y, i, j)
                if self.cells[i][j] == self.GHOSTS_ENTER_CODE:
                    pygame.draw.line(self.game_object.screen, Color.POINTS_COLOR, (x, y + self.cell_size // 2), (x + self.cell_size, y + self.cell_size // 2), 4)
