import pygame

from src.constants import Color
from src.base_classes import DrawableObject


class Field(DrawableObject):
    def __init__(self, game_object, cell_size=20):
        super().__init__(game_object)
        # don't touch cell_size, game level is builded for it and window w & h
        # window width and height must be multiply of cell_size
        # on the original photo 28x30
        self.cell_size = cell_size
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

    def process_draw(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                x = j*self.cell_size
                y = i*self.cell_size
                if self.cells[i][j] == self.WALL:
                    color = Color.BLUE
                else:
                    color = Color.BLACK
                pygame.draw.rect(self.game_object.screen, color, (x, y, x+self.cell_size, y+self.cell_size))