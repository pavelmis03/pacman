import sys
import pygame

from src.constants import *
from src.base_classes import *


class HUD(DrawableObject):
    def __init__(self, game_object):
        super().__init__(game_object)

        self.hud_elements = []
        self.lifes_hud_image = pygame.image.load(PATH_HEART_IMG).convert()
        self.font = pygame.font.Font(FONT_PATH, SCORES_HUD_FONT_SIZE)
        self.score_position = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30)
        self.lifes_hud_rect = self.lifes_hud_image.get_rect()
        self.lifes_hud = []


    def process_draw(self):
        # Update amount of pacman lifes
        for life in range(self.game_object.lifes):
            # 1.2 - stretch coef of spacing between images
            r = pygame.Rect(20 + (self.lifes_hud_rect.width * life * 1.2),  # x
                            SCREEN_HEIGHT - self.lifes_hud_rect.height - 15,  # y
                            0, 0)  # width, height
            self.lifes_hud.append(r)

        # Update scores of pacman
        score_text = self.font.render(str(self.scores), 1, (Color.WHITE))
        # Blit on screen
        for life_obj in self.lifes_hud:
            self.game_object.screen.blit(self.lifes_hud_image, life_obj)
            self.game_object.screen.blit(score_text, score_position)