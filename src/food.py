import pygame
from src.base_classes import DrawableObject
from src.constants import Color
from enum import  Enum


class FoodType(Enum):  # Class - enum. Need to recognize type of food object
    POINT = 1
    ENERGIZER = 2
    FRUIT = 3


class Food(DrawableObject):
    def __init__(self, game_object, cell_size, x, y, food_type: FoodType):
        super().__init__(game_object)
        self.cell_size = cell_size
        self.x = x
        self.y = y
        self.type = food_type

    def draw_point(self):
        food_size = int(self.cell_size * 0.25)
        x_space = self.x + self.cell_size // 2 - food_size // 2
        y_space = self.y + self.cell_size // 2 - food_size // 2
        pygame.draw.rect(self.game_object.screen, Color.POINTS_COLOR, (x_space, y_space, food_size, food_size), 0)

    def draw_fruit(self):
        food_size = int(self.cell_size * 0.4)
        x_space = self.x + self.cell_size // 2
        y_space = self.y + self.cell_size // 2
        pygame.draw.circle(self.game_object.screen, Color.RED, (x_space, y_space), food_size, 0)

    def draw_energizer(self):
        food_size = int(self.cell_size * 0.35)
        x_space = self.x + self.cell_size // 2
        y_space = self.y + self.cell_size // 2
        pygame.draw.circle(self.game_object.screen, Color.POINTS_COLOR, (x_space, y_space), food_size, 0)

    def process_draw(self):
        if self.type == FoodType.POINT:
            self.draw_point()
        elif self.type == FoodType.ENERGIZER:
            self.draw_energizer()
        elif self.type == FoodType.FRUIT:
            self.draw_fruit()
