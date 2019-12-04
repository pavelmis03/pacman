import pygame

from src.animations import Anim
from src.base_classes import DrawableObject
from src.constants import *
from src.enums import *


class Food(DrawableObject):
    def __init__(self, game_object, cell_size, x, y, food_type: FoodType, fruit_code=0):
        super().__init__(game_object)
        self.cell_size = cell_size
        self.x = x
        self.y = y
        self.type = food_type
        self.fruit_type = int(fruit_code)
        # Load sprites for fruit food
        if str(self.fruit_type) in FRUIT_CODES:
            self.fruit_sprite = self.game_object.fruits_sprites[str(self.fruit_type)]
        # Animation for energizer food
        self.a_nrjzer = Anim(['SHOW', 'HIDE'], 200)

    def eat_up(self):
        # FRUIT
        if self.type == FoodType.FRUIT:
            self.game_object.mixer.play_sound('FRUIT')
            self.game_object.scores += SCORE_FOR_FRUIT[self.fruit_type]
            self.game_object.pacman.eat_ghost_fruit(self)
        # ENERGIZER
        if self.type == FoodType.ENERGIZER:
            self.game_object.mixer.play_sound('ENERGIZER')
            self.game_object.scores += SCORE_FOR_ENERGIZER
            # Set all ghosts to frightened if they aren't eaten
            for ghost in self.game_object.ghosts:
                ghost.set_frightened_state()
        # DOT
        if self.type == FoodType.DOT:
            self.game_object.scores += SCORE_FOR_DOT

        # Del our instance of class from Cell class and from game list
        self.game_object.field.get_cell_from_position(Vec(self.x, self.y)).food = None
        self.game_object.food.remove(self.game_object.food[self.game_object.food.index(self)])

    def draw_dot(self):
        food_size = int(self.cell_size * 0.25)
        x_space = self.x + self.cell_size // 2 - food_size // 2
        y_space = self.y + self.cell_size // 2 - food_size // 2
        pygame.draw.rect(self.game_object.screen, Color.DOTS_COLOR, (x_space, y_space, food_size, food_size), 0)

    def draw_fruit(self):
        self.game_object.screen.blit(self.fruit_sprite,
                                     (self.x - CELL_SIZE // 2, self.y - CELL_SIZE // 2, CELL_SIZE * 2, CELL_SIZE * 2))

    def draw_energizer(self):
        if self.a_nrjzer.curr_sprite == 'SHOW':
            food_size = int(self.cell_size * 0.4)
            x_space = self.x + self.cell_size // 2
            y_space = self.y + self.cell_size // 2
            pygame.draw.circle(self.game_object.screen, Color.DOTS_COLOR, (x_space, y_space), food_size, 0)

    # Base class methods)=============================================================================
    def process_logic(self):
        self.a_nrjzer.add_tick()

    def process_draw(self):
        # Почему-то создаются копии всей еды на карте, скорее всего это связанно с конструктором копирования
        if self in self.game_object.food:
            if self.type == FoodType.DOT:
                self.draw_dot()
            elif self.type == FoodType.ENERGIZER:
                self.draw_energizer()
            elif self.type == FoodType.FRUIT:
                self.draw_fruit()
