import os
import sys
from os import environ

from src.constants import *
import pygame


class DrawableObject:

    def __init__(self, game_object):
        self.game_object = game_object

    def process_event(self, event):
        pass

    def process_logic(self):
        pass

    def process_draw(self):
        pass


class InputBox(DrawableObject):
    def __init__(self, game_object, prefix='', pos=Vec(50, 50), size=Vec(250, 30),
                 clr=(255, 255, 255), mx_len=10, text=''):
        super().__init__(game_object)
        self.text = text
        self.prefix = prefix
        self.max_text_len = mx_len
        self.rect = pygame.Rect(pos.x, pos.y, size.x, size.y)
        self.font = pygame.font.Font(FONT_PATH, size.y * 2 // 3)
        self.color = clr
        self.focused = False

    def process_event(self, event):
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[0:-1]
            elif event.key == pygame.K_RETURN:
                pass
            elif event.key == pygame.K_MINUS:
                self.text.append("_")
            elif event.key <= 127 and len(self.text) < self.max_text_len:
                self.text += chr(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.focused = self.rect.collidepoint(event.pos[0], event.pos[1])

    def process_draw(self):
        pygame.draw.rect(self.game_object.screen, Color.BLACK, self.rect, 0)
        pygame.draw.rect(self.game_object.screen, self.color, (self.rect.x - 3, self.rect.y - 3,
                                                               self.rect.width + 6, self.rect.height + 6), 1)
        if len(str(self.text)) != 0 or self.prefix != '':
            self.game_object.screen.blit(self.font.render((self.prefix + str(self.text)), 1, self.color),
                                         self.rect)


class Button(DrawableObject):
    def __init__(self, game_object, pos=Vec(50, 50), size=Vec(120, 30), b_clr=(128, 255, 255), t_clr=(255, 255, 255), code=' '):
        super().__init__(game_object)
        self.text = ''
        self.img = None
        self.tumbler = False
        self.enabled = False
        self.b_color = b_clr
        self.t_color = t_clr
        self.rect = pygame.Rect(pos.x, pos.y, size.x, size.y)
        self.font_size = size.y * 2 // 3
        self.font = pygame.font.Font(FONT_PATH, self.font_size)
        self.d_text = self.font.render(self.text, 1, self.t_color)
        self.code = code

    def set_image(self, img: str):
        self.img = pygame.transform.scale(pygame.image.load(img), (self.rect.width, self.rect.height))

    def on_click(self):
        if self.tumbler:
            self.enabled = not self.enabled
        self.game_object.on_button_click(self)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.on_click()

    def process_draw(self):
        self.d_text = self.font.render(self.text, 1, self.t_color)
        pygame.draw.rect(self.game_object.screen, Color.GREEN if self.enabled else self.b_color, self.rect, 0)
        pygame.draw.rect(self.game_object.screen, Color.WHITE, (self.rect.x - 3, self.rect.y - 3,
                                                                self.rect.width + 6, self.rect.height + 6), 2)
        if self.img:
            self.game_object.screen.blit(self.img, self.rect)
        else:
            text_rect = pygame.Rect(self.rect.centerx - self.d_text.get_width() // 2,
                                    self.rect.centery - self.d_text.get_height() // 2,
                                    self.d_text.get_width() * 2, self.d_text.get_height() * 2)
            self.game_object.screen.blit(self.d_text,
                                         text_rect)


class MapCell(Button):
    def __init__(self, game_object, f_pos=Vec(0, 0), code=' '):
        super().__init__(game_object)
        self.char = ''
        self.f_pos = f_pos
        pos = Vec((self.f_pos.x * (CELL_SIZE + 1)) + 110, (self.f_pos.y * (CELL_SIZE + 1)) + 110)
        self.rect = pygame.Rect(pos.x, pos.y, CELL_SIZE, CELL_SIZE)
        self.code = code
        self.bg_color = Color.GRAY

    def set_char(self, code):
        self.code = code

    def process_event(self, event):
        super().process_event(event)

    def process_draw(self):
        self.d_text = self.font.render(self.text, 1, self.t_color)
        pygame.draw.rect(self.game_object.screen, self.bg_color, self.rect, 0)
        if self.img:
            self.game_object.screen.blit(self.img, self.rect)


class LevelCreator:
    objects: []
    screen: pygame.display
    map_sprites: dict
    fruits_sprites: dict
    lvl_name_input: InputBox
    lvl_w: InputBox
    lvl_h: InputBox
    save_button: Button
    open_button: Button
    made_map_button: Button
    map: []
    selectedCode: str

    def __init__(self):
        self.close = False
        self.lvls_dir = 'levels/'
        self.size = [SCREEN_WIDTH + 200, SCREEN_HEIGHT + 100]

        self.library_init()
        self.reset()

    def on_button_click(self, button):
        if button == self.save_button:
            with open(os.getcwd() + '/' + self.lvls_dir + self.lvl_name_input.text, 'w') as file:
                for y in range(int(self.lvl_h.text)):
                    for x in range(int(self.lvl_w.text)):
                        print(str(y + 1) + '|' + self.map[y][x].code, end='')
                        file.write(self.map[y][x].code)
                    file.write('\n')
                    print('')
                self.sync_map_and_objects()
                file.close()
        if button == self.open_button:
            with open(os.getcwd() + '/' + self.lvls_dir + self.lvl_name_input.text, 'r') as file:
                lines = file.readlines()
                print('|'.join(lines))
                self.lvl_h.text = len(lines)
                self.lvl_w.text = len(lines[0]) - 1
                self.map = list()
                for y in range(int(self.lvl_h.text)):
                    self.map.append([])
                    for x in range(int(self.lvl_w.text)):
                        self.map[y].append(MapCell(self, Vec(x, y), str(lines[y][x])))
                        if str(self.map[y][-1].code) in WALL_CODES:
                            self.map[y][-1].set_image(MAP_DIR + str(lines[y][x]) + '.png')
                        if str(self.map[y][-1].code) == '.':
                            self.map[y][-1].set_image(FRUITS_DIR + 'dot.png')
                        if str(self.map[y][-1].code) == '0':
                            self.map[y][-1].set_image(FRUITS_DIR + 'energizer.png')
                        if str(self.map[y][-1].code) == '@':
                            self.map[y][-1].set_image(PACMAN_DIR + 'pacman2.png')
                        if str(self.map[y][-1].code) == 'b':
                            self.map[y][-1].set_image(GHOSTS_DIR + 'ghost1.png')
                        if str(self.map[y][-1].code) == 'p':
                            self.map[y][-1].set_image(GHOSTS_DIR + 'ghost2.png')
                        if str(self.map[y][-1].code) == 'i':
                            self.map[y][-1].set_image(GHOSTS_DIR + 'ghost3.png')
                        if str(self.map[y][-1].code) == 'c':
                            self.map[y][-1].set_image(GHOSTS_DIR + 'ghost4.png')
                self.sync_map_and_objects()
                file.close()
        if button == self.made_map_button:
            self.map = list()
            for y in range(int(self.lvl_h.text)):
                self.map.append([])
                for x in range(int(self.lvl_w.text)):
                    self.map[y].append(MapCell(self, Vec(x, y), code=' '))
            self.sync_map_and_objects()
        if button in self.walls_btn:
            self.selectedCode = button.code if button.enabled else ' '
            for wall in self.walls_btn:
                if wall != button:
                    wall.enabled = False
            for fruit in self.fruit_btn:
                fruit.enabled = False
        if button in self.fruit_btn:
            self.selectedCode = button.code if button.enabled else ' '
            for fruit in self.fruit_btn:
                if fruit != button:
                    fruit.enabled = False
            for wall in self.walls_btn:
                wall.enabled = False
        if isinstance(button, MapCell):
            button.set_char(self.selectedCode if button.code != self.selectedCode else ' ')
            if button.code == ' ':
                button.set_image(SPRITES_DIR + 'empty.png')
            elif button.code in WALL_CODES:
                button.set_image(MAP_DIR + self.selectedCode + '.png')
            elif button.code in FRUIT_CODES:
                button.set_image(FRUITS_DIR + 'fruit' + self.selectedCode + '.png')
            elif button.code == '.':
                button.set_image(FRUITS_DIR + 'dot.png')
            elif button.code == '0':
                button.set_image(FRUITS_DIR + 'energizer.png')
            elif button.code == '@':
                button.set_image(PACMAN_DIR + 'pacman2.png')
            elif button.code == 'b':
                button.set_image(GHOSTS_DIR + 'ghost1.png')
            elif button.code == 'p':
                button.set_image(GHOSTS_DIR + 'ghost2.png')
            elif button.code == 'i':
                button.set_image(GHOSTS_DIR + 'ghost3.png')
            elif button.code == 'c':
                button.set_image(GHOSTS_DIR + 'ghost4.png')
            else:
                print('ERROR! Inknown map code!')

    def sync_map_and_objects(self):
        for obj in self.objects:
            if isinstance(obj, MapCell):
                del obj
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                self.objects += [self.map[y][x]]

    def reset(self):
        # Load all map sprite library
        self.map_sprites = dict()
        for ch in WALL_CODES:
            self.map_sprites[ch] = pygame.transform.scale(pygame.image.load(MAP_DIR + ch + '.png'),
                                                          (CELL_SIZE, CELL_SIZE))
        # Load all fruits sprite library(Need in Food class)
        self.fruits_sprites = dict()
        for ch in FRUIT_CODES:
            self.fruits_sprites[ch] = pygame.transform.scale(pygame.image.load(FRUITS_DIR + 'fruit' + ch + '.png'),
                                                             (CELL_SIZE * 2, CELL_SIZE * 2))
        self.selectedCode = ' '

        self.objects = []
        # Input field for level name
        self.lvl_name_input = InputBox(self, 'Level name: ', Vec(100, 20), Vec(320, 24), mx_len=8, text='LVL1')
        self.lvl_w = InputBox(self, 'Map width: ', Vec(100, 70), Vec(170, 24), mx_len=2, text='28')
        self.lvl_h = InputBox(self, 'Map height: ', Vec(300, 70), Vec(200, 24), mx_len=2, text='31')

        # Save and open buttons
        self.save_button = Button(self, Vec(430, 21), Vec(50, 22), Color.BLACK, Color.WHITE)
        self.open_button = Button(self, Vec(490, 21), Vec(50, 22), Color.BLACK, Color.WHITE)
        self.made_map_button = Button(self, Vec(510, 71), Vec(70, 22), Color.BLACK, Color.WHITE)
        self.made_map_button.text = 'CREATE'
        self.save_button.text = 'SAVE'
        self.open_button.text = 'OPEN'

        # Wall buttons
        self.walls_btn = []
        for wall_code in WALL_CODES:
            num = WALL_CODES.index(wall_code)
            btn = Button(self, Vec(30, 100 + (30 * num + 5)),
                         Vec(20, 20), Color.BLACK, Color.CYAN, code=wall_code)
            btn.tumbler = True
            btn.set_image(MAP_DIR + wall_code + '.png')
            self.walls_btn += [btn]
        # Fruit buttons
        self.fruit_btn = []
        for fruit_code in '.01@bpic':
            num = '.01@bpic'.index(fruit_code)
            btn = Button(self, Vec(60, 100 + (30 * num + 5)),
                         Vec(20, 20), Color.BLACK, Color.CYAN, code=fruit_code)
            btn.tumbler = True
            if fruit_code == '.':
                btn.set_image(FRUITS_DIR + 'dot.png')
            if fruit_code == '0':
                btn.set_image(FRUITS_DIR + 'energizer.png')
            if fruit_code == '1':
                btn.set_image(FRUITS_DIR + 'fruit1.png')
            if fruit_code == '@':
                btn.set_image(PACMAN_DIR + 'pacman2.png')
            if fruit_code == 'b':
                btn.set_image(GHOSTS_DIR + 'ghost1.png')
            if fruit_code == 'p':
                btn.set_image(GHOSTS_DIR + 'ghost2.png')
            if fruit_code == 'i':
                btn.set_image(GHOSTS_DIR + 'ghost3.png')
            if fruit_code == 'c':
                btn.set_image(GHOSTS_DIR + 'ghost4.png')
            self.fruit_btn += [btn]
        self.objects += self.walls_btn + self.fruit_btn
        self.objects += [self.made_map_button, self.lvl_w, self.lvl_h, self.lvl_name_input, self.save_button, self.open_button]
        self.map = []
        for cell in self.map:
            self.objects += cell

    def library_init(self):
        # Initialize all libs
        pygame.init()
        pygame.font.init()
        # Create and move a window
        self.screen = pygame.display.set_mode(self.size, flags=pygame.DOUBLEBUF)  # Create window
        environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (1, 30)  # Move window to start coordinates
        # Set window caption
        pygame.display.set_caption('Pacman Level Creator')
        # Setup the icon
        icon = pygame.transform.scale(pygame.image.load(MAP_DIR + '/O.png'), (32, 32))
        pygame.display.set_icon(icon)

    # Base methods)=================
    def main_loop(self):
        while not self.close:
            self.process_events()
            self.process_logic()
            self.process_draw()

        sys.exit(0)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Обработка события выхода
                self.close = True
            for item in self.objects:
                item.process_event(event)

    def process_logic(self):
        for item in self.objects:
            item.process_logic()

    def process_draw(self):
        self.screen.fill(BG_COLOR)  # Заливка цветом
        for item in self.objects:
            item.process_draw()
        pygame.display.flip()  # Double buffering
        pygame.time.wait(5)  # Ждать 5 миллисекунд


def lvl_creator_main():
    lc = LevelCreator()
    lc.main_loop()


if __name__ == '__main__':
    lvl_creator_main()