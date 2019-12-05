from src.base_classes import DrawableObject
from src.constants import *
import pygame


class Slider(DrawableObject):
    def __init__(self, game_object, title, val, mini, maxi, rect):
        super().__init__(game_object)

        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.rect = pygame.Rect(rect)
        self.rect.move_ip(-self.rect.width // 2, 0)
        self.panel = pygame.Surface((self.rect.width, self.rect.height))
        self.hit = False  # indicates slider movement due to mouse interaction
        # Holder
        self.holder = pygame.Surface((20, 20))
        self.holder_rect = self.holder.get_rect()

        font = pygame.font.Font(FONT_PATH, 15)
        self.text = font.render(title, 1, Color.WHITE)
        self.txt_rect = self.text.get_rect(center=(self.rect.width // 2, self.text.get_rect().height))

    def process_draw(self):
        self.panel.fill(BG_COLOR)
        self.panel.blit(self.text, self.txt_rect)  # this surface never changes
        # Slider Holder
        self.holder.fill(Color.GREEN)
        self.holder.set_colorkey(Color.GREEN)
        pygame.draw.circle(self.holder, Color.BLACK, self.holder.get_rect().center, 8, 0)
        pygame.draw.circle(self.holder, Color.DOTS_COLOR, self.holder.get_rect().center, 6, 0)

        # Dynamic position
        pos = (10 + int((self.val - self.mini) / (self.maxi - self.mini) * (self.rect.width - 20)),
               self.rect.height - 18)
        self.holder_rect = self.holder.get_rect(center=pos)
        # Slider background
        pygame.draw.rect(self.panel, Color.GRAY, [pos[0] - 10, self.rect.height - 20, self.rect.width - pos[0], 5], 0)
        pygame.draw.rect(self.panel, Color.DOTS_COLOR, [10, self.rect.height - 20, pos[0] - 10, 5], 0)
        self.panel.blit(self.holder, self.holder_rect)
        self.holder_rect.move_ip(self.rect.x, self.rect.y)  # move slider holder

        # Blit to screen
        self.game_object.screen.blit(self.panel, (self.rect.x, self.rect.y))

    def process_event(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.holder_rect.collidepoint(pos):
                self.hit = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.hit = False

    def process_logic(self):
        if self.hit:
            pos = pygame.mouse.get_pos()
            self.val = (pos[0] - self.rect.x - 10) / (self.rect.width - 20) * \
                       (self.maxi - self.mini) + self.mini
            if self.val < self.mini:
                self.val = self.mini
            if self.val > self.maxi:
                self.val = self.maxi


class Button(DrawableObject):
    def __init__(self, game_object, rect, b_clr=Color.CYAN, t_clr=Color.WHITE, text=' '):
        super().__init__(game_object)
        # Color
        self.b_color = b_clr
        self.t_color = t_clr
        # Rect
        self.rect = pygame.Rect(rect)
        # Text
        self.text = text
        self.font_size = self.rect.height * 4 // 5
        self.font = pygame.font.Font(FONT_PATH, self.font_size)
        self.d_text = self.font.render(self.text, 1, self.t_color)

    def on_click(self):
        self.game_object.change_music()

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.on_click()

    def process_draw(self):
        # Text
        self.d_text = self.font.render(self.text, 1, self.t_color)
        text_rect = pygame.Rect(self.rect.centerx - self.d_text.get_width() // 2,
                                self.rect.centery - self.d_text.get_height() // 2,
                                self.d_text.get_width() * 2, self.d_text.get_height() * 2)
        # Btn
        pygame.draw.rect(self.game_object.screen, self.b_color, self.rect, 0)
        pygame.draw.rect(self.game_object.screen, self.t_color, (self.rect.x - 1, self.rect.y - 1,
                                                                 self.rect.width + 2, self.rect.height + 2), 2)
        # Draw
        self.game_object.screen.blit(self.d_text, text_rect)
