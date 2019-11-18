import pygame
from src.base_classes import DrawableObject
from src.constants import Color

class Food(DrawableObject):
    def __init__(self, game_object, x, y):
        super().__init__(game_object)
        self.x = x
        self.y = y

    def draw_food(self):
        pygame.draw.circle(self.game_object.screen, Color.YELLOW, (self.x, self.y), 3)

    def draw_superfood(self):
        pygame.draw.circle(self.game_object.screen, Color.YELLOW, (self.x, self.y), 7)


    def process_draw(self):
        self.draw_superfood()