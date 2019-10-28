import os
from random import randrange
import pygame

from src.base_classes import DrawableObject
from src.constants import IMAGES_DIR


class Ball(DrawableObject):
    image = pygame.image.load(os.path.join(IMAGES_DIR, 'basketball.png'))

    def __init__(self, game_object):
        super().__init__(game_object)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(10, self.game_object.width - self.rect.width - 20)
        self.rect.y = randrange(10, self.game_object.height - self.rect.height - 20)
        self.shift_x = 1 if randrange(0, 2) == 1 else -1
        self.shift_y = 1 if randrange(0, 2) == 1 else -1

    def process_logic(self):
        if self.rect.left <= 0 or self.rect.right >= self.game_object.width:
            self.shift_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= self.game_object.height:
            self.shift_y *= -1
        self.rect.x += self.shift_x
        self.rect.y += self.shift_y

    def process_draw(self):
        self.game_object.screen.blit(self.image, self.rect)