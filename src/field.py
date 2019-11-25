import pygame

from src.constants import Color, FIELD_MAP
from src.base_classes import DrawableObject, FieldObject


class Field(DrawableObject):
    def __init__(self, game_object, cell_size=20, position=[0, 0]):
        super().__init__(game_object)
        self.cell_size = cell_size
        self.offset = position
        self.clear()
        self.WALL = '#'
        self.bump = 2 # выпуклость стен

        self.objects = {}
        # этл словарь: отображение - класс


    def get_cell_pos(self, i, j):
        x = self.offset[0] + j * self.cell_size
        y = self.offset[1] + i * self.cell_size
        return [x, y]

    def draw_wall(self, x, y):
        pygame.draw.rect(self.game_object.screen, Color.DBLUE, (x, y, self.cell_size, self.cell_size), self.bump)
        pygame.draw.rect(self.game_object.screen, Color.BLUE, (x + self.bump, y + self.bump, self.cell_size - self.bump, self.cell_size - self.bump))

    def process_draw(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                c = self.cells[i][j]
                x, y = self.get_cell_pos(i, j)
                if self.cells[i][j] == self.WALL:
                    self.draw_wall(x, y)
                elif c in self.objects.keys():
                    self.objects[c].process_draw()


    def process_logic(self):
        # здесь объеты из self.objects меняют поле cells
        # которое затем отрисовывается в process_draw
        self.clear()
        for key in self.objects.keys():
            self.object[key].process_logic()

    def clear(self):
        self.cells = FIELD_MAP