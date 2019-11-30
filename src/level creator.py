import sys
from os import environ

from src.base_classes import DrawableObject
from src.constants import *
from src.field import Field
import pygame


class InputBox(DrawableObject):
    def __init__(self, game_object, prefix='', pos=Vec(50, 50), size=Vec(250, 30), clr=(255, 255, 255)):
        super().__init__(game_object)
        self.text = ''
        self.prefix = prefix
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
            elif event.key <= 127:
                self.text += chr(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.focused = self.rect.collidepoint(event.pos[0], event.pos[1])

    def process_draw(self):
        pygame.draw.rect(self.game_object.screen, Color.BLACK, self.rect, 0)
        pygame.draw.rect(self.game_object.screen, self.color, (self.rect.x - 3, self.rect.y - 3,
                                                               self.rect.width + 6, self.rect.height + 6), 1)
        if len(self.text) != 0 or self.prefix != '':
            self.game_object.screen.blit(self.font.render((self.prefix + self.text), 1, self.color),
                                         self.rect)


class Button(DrawableObject):
    def __init__(self, game_object, pos=Vec(50, 50), size=Vec(120, 30), b_clr=(128, 255, 255), t_clr=(255, 255, 255)):
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

    def set_image(self, img: str):
        self.img = pygame.transform.scale(pygame.image.load(img), (self.rect.width, self.rect.height))

    def on_click(self):
        if self.tumbler:
            self.enabled = not self.enabled
        else:
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


class LevelCreator:
    objects: []
    screen: pygame.display

    def __init__(self):
        self.close = False
        self.lvls_dir = 'src/levels/'
        self.size = SCREEN_SIZE

        self.library_init()
        self.reset()

    def reset(self):
        self.objects = []
        lvl_name = InputBox(self, 'Level name: ', Vec(50, 50), Vec(400, 24))
        for wall_code in WALL_CODES:
            num = WALL_CODES.index(wall_code)
            btn = Button(self, Vec(30, 100 + (30 * num + 5)),
                         Vec(20, 20), Color.BLACK, Color.CYAN)
            btn.tumbler = True
            btn.set_image(MAP_DIR + wall_code + '.png')
            self.objects += [btn]
        for fruit_code in FRUIT_CODES:
            num = FRUIT_CODES.index(fruit_code)
            btn = Button(self, Vec(60, 100 + (30 * num + 5)),
                         Vec(20, 20), Color.BLACK, Color.CYAN)
            btn.tumbler = True
            btn.set_image(FRUITS_DIR + 'fruit' + fruit_code + '.png')
            self.objects += [btn]
        self.objects += [lvl_name]

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