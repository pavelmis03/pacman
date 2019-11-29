import sys
import pygame

from src.constants import *
from src.base_classes import *


class HUD(DrawableObject):
    def __init__(self, game_object):
        super().__init__(game_object)

        self.hud_elements = []
        self.lives_hud_image = pygame.transform.scale(pygame.image.load(PATH_LIFE), (CELL_SIZE * 2, CELL_SIZE * 2))
        self.font = pygame.font.Font(FONT_PATH, SCORES_HUD_FONT_SIZE)
        self.score_position = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 20)
        self.lives_hud_rect = self.lives_hud_image.get_rect()
        self.lives_hud = []
        self.update_lives()

    def update_lives(self):
        for live in range(self.game_object.lives):
            r = pygame.Rect(20 + (self.lives_hud_rect.width * live),  # x
                            SCREEN_HEIGHT - self.lives_hud_rect.height - 10,  # y
                            CELL_SIZE, CELL_SIZE)  # width, height
            self.lives_hud.append(r)

    def process_draw(self):
        # Update scores of pacman and position of text dependence of its length
        score_text = self.font.render('ОЧКИ: ' + str(self.game_object.scores), 1, Color.WHITE)
        self.score_position = score_text.get_rect()
        self.score_position.right = SCREEN_WIDTH - 10
        self.score_position.bottom = SCREEN_HEIGHT - 10

        # Display on screen
        for live_obj in self.lives_hud:
            self.game_object.screen.blit(self.lives_hud_image, live_obj)
            self.game_object.screen.blit(score_text, self.score_position)