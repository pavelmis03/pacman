import sys
import pygame
from src.constants import *


class UI_Button:
    # label - Label of button; rect  - position of button, click_action - function after click
    def __init__(self, label, page=None, rect=None, font=None, click_action=''):
        self.page = page
        self.label = str(label)
        self.rect = rect
        self.font = font
        self.normal_color = UI_BTN_NORM_CLR
        self.active_color = UI_BTN_ACT_CLR
        self.click_action = click_action
        self.hovered = False

        self.quit = True

    def procedure_events(self, event):
        # User Events
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position
        # If mouse in Button
        if self.rect.left < mouse_pos[0] < self.rect.right and \
                self.rect.top < mouse_pos[1] < self.rect.bottom:
            self.hovered = True
            # Press Left Mouse Key
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                exec(self.click_action)
        else:
            self.hovered = False

    def process_draw(self, screen):
        self.text_surface = self.font.render(self.label, False, self.active_color if self.hovered else self.normal_color)
        screen.blit(self.text_surface, (self.rect.x, self.rect.y))


class MainMenu:
    def __init__(self, game):
        # Default values
        self.curr_click_act = ''
        self.game = game
        self.additional_text = None

        # Init font engine
        pygame.font.init()
        self.font_menu = pygame.font.Font(FONT_PATH, TITLE_SIZE)
        self.menu_items = []
        self.logo = pygame.image.load(PATH_LOGO);
        self.logo_rect = self.logo.get_rect()
        self.display_logo = True

    def setup_elements(self, menu_names=None, menu_actions=None, x0=SCREEN_CENTER[0] // 2, y0=300):
        # Add menu items(buttons)
        self.menu_items = []
        for i in range(len(menu_names)):
            self.menu_items.append(UI_Button(menu_names[i], click_action=menu_actions[i]))

        item_num = 0
        # Setup buttons
        for item in self.menu_items:
            item_num += 1
            # Font
            item.font = self.font_menu
            # Reference to self
            item.page = self
            # Button position
            item.rect = pygame.Rect((x0, UI_BTN_SIZE[1] * item_num + y0), UI_BTN_SIZE)

    def menu_loop(self):
        #Start
        self.setup_elements(['ИГРАТЬ', 'УПРАВЛЕНИЕ', 'РЕКОРДЫ', 'СОЗДАТЕЛИ', 'ВЫХОД'],
                           ['menu_action_play(self.page)', 'menu_action_controls(self.page)',
                            'menu_action_highscores(self.page)', 'menu_action_credits(self.page)',
                            'menu_action_exit(self.page)'])

        #Loop
        while self.curr_click_act not in ['PLAY', 'EXIT']:
            self.process_events()
            self.process_draw()
        self.game.start_game = True

    def process_events(self):
        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:  # Обработка события выхода
                self.game.start_game = True
                self.game.game_over = True
                sys.exit()
            for item in self.menu_items:
                item.procedure_events(event)

    def process_draw(self):
        self.game.screen.fill(BG_COLOR)  # Заливка цветом
        for item in self.menu_items:
            item.process_draw(self.game.screen)

        # Additional text
        if self.additional_text:
            for i in range(len(self.additional_text[0])):
                temp_text = self.additional_text[1].render(self.additional_text[0][i], 1, TEXT_COLOR)
                self.game.screen.blit(temp_text, (self.additional_text[2], self.additional_text[3] + 40 * i))

        # Logo
        if self.display_logo:
            self.game.screen.blit(self.logo, (SCREEN_CENTER[0] - self.logo_rect.width // 2,
                                              self.logo_rect.height // 2))

        pygame.display.flip()  # Double buffering
        pygame.time.wait(RESPONSE)  # Ждать 10 миллисекунд


def menu_action_back(menu):
    menu.additional_text = None
    menu.setup_elements(['ИГРАТЬ', 'УПРАВЛЕНИЕ', 'РЕКОРДЫ', 'СОЗДАТЕЛИ', 'ВЫХОД'],
                       ['menu_action_play(self.page)', 'menu_action_controls(self.page)',
                        'menu_action_highscores(self.page)', 'menu_action_credits(self.page)',
                        'menu_action_exit(self.page)'])
    menu.display_logo = True


def menu_action_play(menu):
    menu.curr_click_act = 'PLAY'
    menu.additional_text = None
    menu.game.start_game = True
    menu.display_logo = False


def menu_action_controls(menu):
    menu.curr_click_act = 'CONTROLS'
    menu.setup_elements(['НАЗАД'], ['menu_action_back(self.page)'], x0=35, y0=SCREEN_HEIGHT - 100)
    menu.additional_text = None
    display_data(menu, PATH_CONTROLS, 'r', True, 50, 50, 'KEY', 'VALUE')
    menu.display_logo = False


def menu_action_highscores(menu):
    menu.curr_click_act = 'HIGHSCORES'
    menu.setup_elements(['НАЗАД'], ['menu_action_back(self.page)'], x0=35, y0=SCREEN_HEIGHT - 100)
    menu.additional_text = None
    display_data(menu, PATH_HIGHSCORES, 'r', True, 50, 50, 'NAME', 'SCORE')
    menu.display_logo = False


def menu_action_credits(menu):
    menu.curr_click_act = 'CREDITS'
    menu.setup_elements(['НАЗАД'], ['menu_action_back(self.page)'], x0=35, y0=SCREEN_HEIGHT - 100)
    menu.additional_text = None
    display_data(menu, PATH_CREDITS, 'r', False, 50, 50, '', '')
    menu.display_logo = False


def menu_action_exit(menu):
    menu.curr_click_act = 'EXIT'
    exit()

####################################################################################################################################
# Can display text on screen
def display_data(menu, file, param, is_table, x, y, table_head1='', table_head2=''):
    fnt = pygame.font.Font(FONT_PATH, 30)
    file = open(file, param, encoding="utf-8")
    text = file.readlines()
    text = [line.rstrip() for line in text]
    if is_table:
        ts = []
        for i in range(len(text)):
            ts.append(text[i].split(':'))
        for i in range(len(text)):
            for j in range(len(text)):
                try:
                    a = float(ts[i][1])
                    b = float(ts[j][1])
                    if a >= b:
                        t = ts[i]
                        ts[i] = ts[j]
                        ts[j] = t
                except ValueError:
                    pass
        new_s = ['{:<7}      {:^5}'.format(str(table_head1), str(table_head2))]
        for i in range(len(ts)):
            new_s.append('{:<7}      {:^5}'.format(ts[i][0], ts[i][1]))
        text = []
        for i in range(len(new_s)):
            text.append(new_s[i])
    menu.additional_text = [text, fnt, x, y]
    file.close()