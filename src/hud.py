import sys
import pygame

from src.constants import *
from src.base_classes import *


class HUD(DrawableObject):
    score_text: None
    score_pos: None
    map_text: None
    map_pos: None
    title_text: None
    title_pos: None

    def __init__(self, game_object):
        super().__init__(game_object)

        self.hud_elements = []
        self.lives_hud_image = pygame.transform.scale(pygame.image.load(PATH_LIFE), (CELL_SIZE * 9//5, CELL_SIZE * 9//5))
        self.font = pygame.font.Font(FONT_PATH, SCORES_HUD_FONT_SIZE)

        self.lives_hud_rect = self.lives_hud_image.get_rect()
        self.lives_hud = []

        self.reset()

    def reset(self):
        # Level_text
        self.title_text = self.font.render('LEVEL ' + str(self.game_object.level), 1, Color.WHITE)
        self.title_pos = self.title_text.get_rect()
        self.title_pos.centerx, self.title_pos.y = size.SCREEN_CENTER.x, 0

        # Map_text
        self.map_text = self.font.render(str(self.game_object.current_map.split('.')[0]), 1, Color.WHITE)
        self.map_pos = self.map_text.get_rect()
        self.map_pos.x, self.map_pos.y = CELL_SIZE * 2, 0

        # Score text
        self.score_text = self.font.render(str(self.game_object.scores), 1, Color.WHITE)
        self.score_pos = self.score_text.get_rect()
        self.score_pos.x = CELL_SIZE * 3
        self.score_pos.y = CELL_SIZE

        self.update_lives()

    def update_lives(self):
        self.lives_hud = []
        for live in range(self.game_object.lives):
            r = pygame.Rect(CELL_SIZE + (CELL_SIZE * 2 * live),  # x
                            size.SCREEN_HEIGHT - CELL_SIZE * 2,  # y
                            CELL_SIZE * 2, CELL_SIZE * 2)  # width, height
            self.lives_hud.append(r)

    def process_logic(self):
        # Score text
        self.score_text = self.font.render(str(self.game_object.scores), 1, Color.WHITE)

    def process_draw(self):
        # Display on screen
        for live_obj in self.lives_hud:
            self.game_object.screen.blit(self.lives_hud_image, live_obj)
            self.game_object.screen.blit(self.score_text, self.score_pos)
            self.game_object.screen.blit(self.map_text, self.map_pos)
            self.game_object.screen.blit(self.title_text, self.title_pos)