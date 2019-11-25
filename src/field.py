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

    def draw_wall(self, x, y):
        pygame.draw.rect(self.game_object.screen, Color.DBLUE, (x, y, self.cell_size, self.cell_size), self.bump)
        pygame.draw.rect(self.game_object.screen, Color.BLUE,
                         (x + self.bump, y + self.bump, self.cell_size - self.bump, self.cell_size - self.bump))

    def process_draw(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                x = self.offset[0] + j * self.cell_size
                y = self.offset[1] + i * self.cell_size
                # Draw wall
                if self.cells[i][j] == self.WALL_CODE:
                    self.draw_wall(x, y)