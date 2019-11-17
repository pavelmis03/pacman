import pygame

from src.constants import Color
from src.base_classes import DrawableObject


class Field(DrawableObject):
    def __init__(self, game_object, cell_size=20, position=[0, 0]):
        super().__init__(game_object)
        # don't touch cell_size, game level is builded for it and window w & h
        # window width and height must be multiply of cell_size
        # on the original photo 28x30
        self.cell_size = cell_size
        self.offset = position
        self.cells = [
            "#######################################",
            "# . . . * . . . . ### . . . . * . . . #",
            "# . ### . ##### . ### . ##### . ### . #",
            "# * . . * . * . * . . * . * . * . . * #",
            "# . ### . # . ########### . # . ### . #",
            "# . . . * # . . . ### . . . # * . . . #",
            "####### . ##### . ### . ##### . #######",
            "      # . # . . * . . * . . # . #      ",
            "      # . # . ### - - ### . # . #      ",
            "####### . # . #         # . # . #######",
            "        * . * #         # * . *        ",
            "####### . # . #         # . # . #######",
            "      # . # . ########### . # . #      ",
            "      # . # * . . . . . . * # . #      ",
            "####### . # . ########### . # . #######",
            "# . . . * . * . . ### . . * . * . . . #",
            "# . ### . ##### . ### . ##### . ### . #",
            "# . . # * . * . * . . * . * . * # . . #",
            "### . # . # . ########### . # . # . ###",
            "# . * . . # . . . ### . . . # . . * . #",
            "# . ########### . ### . ########### . #",
            "# . . . . . . . * . . * . . . . . . . #",
            "#######################################"
        ]
        self.WALL = '#'
        self.bump = 2 # выпуклость стен, сделай больше и посмотри что выйдет))

    def process_draw(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                x = self.offset[0] + j*self.cell_size
                y = self.offset[1] + i*self.cell_size
                if self.cells[i][j] == self.WALL:
                    pygame.draw.rect(self.game_object.screen, Color.DBLUE, (x, y, self.cell_size, self.cell_size), self.bump)
                    pygame.draw.rect(self.game_object.screen, Color.BLUE, (x+self.bump, y+self.bump, self.cell_size-self.bump, self.cell_size-self.bump))