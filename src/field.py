import pygame

from src.constants import Color
from src.base_classes import DrawableObject
from src.food import Food

class Field(DrawableObject):
    def __init__(self, game_object, cell_size=15, position=[0, 0]):
        super().__init__(game_object)
        # don't touch cell_size, game level is builded for it and window w & h
        # window width and height must be multiply of cell_size
        # on the original photo 28x30
        self.game_object = game_object
        self.cell_size = cell_size
        self.offset = position
        self.cells = [
            "############################",
            "#............##............#",
            "#.#### #####.##.#####.####.#",
            "#.#### #####.##.#####.####.#",
            "#@#### #####.##.#####.####@#",
            "#..........................#",
            "#.####.##.########.##.####.#",
            "#.####.##.########.##.####.#",
            "#......##....##....##......#",
            "######.##### ## #####.######",
            "     #.##### ## #####.#     ",
            "     #.##          ##.#     ",
            "     #.## ###  ### ##.#     ",
            "######.## #      # ##.######",
            "      .   #      #   .      ",
            "######.## #      # ##.######",
            "     #.## ######## ##.#     ",
            "     #.##          ##.#     ",
            "     #.## ######## ##.#     ",
            "######.## ######## ##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#.####.#####.##.#####.####.#",
            "#@..##................##..@#",
            "###.##.##.########.##.##.###",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################"
        ]
        self.WALL = '#'
        self.Super_FOOD = '@'
        self.FOOD = '.'
        self.bump = 2 # выпуклость стен, сделай больше и посмотри что выйдет))

    def get_Food(self):
        objects = []
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                x = self.offset[0] + j*self.cell_size + 10
                y = self.offset[1] + i*self.cell_size + 10
                if self.cells[i][j] == self.FOOD or self.cells[i][j] == '*': #не понял, зачем нужна *, но на ее месте лодна быть "еда"
                    objects.append(Food(self.game_object, x, y, 0))
                elif self.cells[i][j] == self.Super_FOOD:
                    objects.append(Food(self.game_object, x, y, 1))
        return objects

    def process_draw(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                x = self.offset[0] + j*self.cell_size
                y = self.offset[1] + i*self.cell_size
                if self.cells[i][j] == self.WALL:
                    pygame.draw.rect(self.game_object.screen, Color.DBLUE, (x, y, self.cell_size, self.cell_size), self.bump)
                    pygame.draw.rect(self.game_object.screen, Color.BLUE, (x+self.bump, y+self.bump, self.cell_size-self.bump, self.cell_size-self.bump))
                elif self.cells[i][j] == self.FOOD:
                    pass
