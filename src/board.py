import pygame

from src.base_classes import DrawableObject
from src.constants import Color


class Board(DrawableObject):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.rect = pygame.rect.Rect(400, 500, 100, 20)
        self.shift = 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.shift += -3
            elif event.key == pygame.K_d:
                self.shift += 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                self.shift = 0

    def process_logic(self):
        self.rect.x += self.shift

    def process_draw(self):
        pygame.draw.rect(self.game_object.screen, Color.RED, self.rect, 5)