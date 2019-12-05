import pygame

from src.base_classes import DrawableObject
from src.characters import Dir
from src.constants import size, Color, BG_COLOR, ALPHABET
from src.ui_elements import Button, InputBox, Text


class RecordMenu(DrawableObject):
    def __init__(self, game_object):
        super().__init__(game_object)

        self.reset()

    def reset(self):
        # Default values
        btn_next = Button(self.game_object, (size.SCREEN_WIDTH // 2 - 150, size.SCREEN_HEIGHT * 3//4, 300, 50),
                          Color.DOTS_COLOR, Color.WHITE, 'CONTINUE', id=0)

        # Title
        title = Text(self.game_object, 'YOUR SCORE: ' + str(self.game_object.scores),
                     (size.SCREEN_WIDTH//2 - 100, 60, 200, 40), Color.CYAN, id=5)

        # First letter of initial
        btn_1arr_up = Button(self.game_object, (size.SCREEN_WIDTH * 1//4 + 10, size.SCREEN_HEIGHT//2 - 180, 40, 40),
                             Color.BLACK, Color.CYAN, '-', id=11)
        self.ib1 = Text(self.game_object, 'A', (size.SCREEN_WIDTH * 1//4, size.SCREEN_HEIGHT//2 - 140, 60, 100),
                            Color.WHITE, id=12)
        btn_1arr_down = Button(self.game_object, (size.SCREEN_WIDTH * 1//4 + 10, size.SCREEN_HEIGHT//2 - 40, 40, 40),
                               Color.BLACK, Color.CYAN, '+', id=13)
        # Second letter of initial
        btn_2arr_up = Button(self.game_object, (size.SCREEN_WIDTH * 2//4 - 20, size.SCREEN_HEIGHT//2 - 180, 40, 40),
                             Color.BLACK, Color.CYAN, '-', id=21)
        self.ib2 = Text(self.game_object, 'A', (size.SCREEN_WIDTH * 2//4 - 30, size.SCREEN_HEIGHT//2 - 140, 60, 100),
                            Color.WHITE, id=22)
        btn_2arr_down = Button(self.game_object, (size.SCREEN_WIDTH * 2//4 - 20, size.SCREEN_HEIGHT//2 - 40, 40, 40),
                                Color.BLACK, Color.CYAN, '+', id=23)
        # Thrid letter of initial
        btn_3arr_up = Button(self.game_object, (size.SCREEN_WIDTH * 3//4 - 50, size.SCREEN_HEIGHT//2 - 180, 40, 40),
                             Color.BLACK, Color.CYAN, '-', id=31)
        self.ib3 = Text(self.game_object, 'A', (size.SCREEN_WIDTH * 3//4 - 60, size.SCREEN_HEIGHT//2 - 140, 60, 100),
                            Color.WHITE, id=32)
        btn_3arr_down = Button(self.game_object, (size.SCREEN_WIDTH * 3//4 - 50, size.SCREEN_HEIGHT//2 - 40, 40, 40),
                               Color.BLACK, Color.CYAN, '+', id=33)
        self.objects = [btn_next, title,
                        btn_1arr_up, self.ib1, btn_1arr_down,
                        btn_2arr_up, self.ib2, btn_2arr_down,
                        btn_3arr_up, self.ib3, btn_3arr_down]

    def change_letter(self, obj, dir):
        step = 1 if dir == Dir.down else -1
        ib = self.ib1 if obj.id//10 == 1 else self.ib2 if obj.id//10 == 2 else self.ib3
        ib.text = ALPHABET[(ALPHABET.find(ib.text) + step) % len(ALPHABET)]

    def process_event(self, event):
        for ev in event:
            for obj in self.objects:
                obj.process_event(ev)

    def process_logic(self):
        for obj in self.objects:
            if isinstance(obj, Button):
                if obj.id == 0:
                    if obj.click:
                        self.game_object.save_records(self.ib1.text + self.ib2.text + self.ib3.text)
                        self.game_object.out_rmenu = True
                if obj.id in [11, 21, 31]:
                    if obj.click:
                        self.change_letter(obj, Dir.up)
                if obj.id in [13, 23, 33]:
                    if obj.click:
                        self.change_letter(obj, Dir.down)
            obj.process_logic()

    def process_draw(self):
        self.game_object.screen.fill(BG_COLOR)  # Заливка цветом для корректного отображения всех элементов
        for obj in self.objects:
            obj.process_draw()
        pygame.display.flip()