
import sys, pygame

size = [1200, 800]
screen = pygame.Surface(size)
window = pygame.display.set_mode((size))
pygame.font.init()

def drawText(file, param, font_decor, table, x, y):
    fnt = pygame.font.Font(None, 30)
    file = open(file, param)
    text = file.readlines()
    text = [line.rstrip() for line in text]
    if (table):
        ts = []
        for i in range(len(text)):
            ts.append(text[i].split())
        for i in range(len(text)):
            for j in range(i + 1, len(text)):
                if (float(ts[i][1]) >= float(ts[j][1])):
                    t = ts[i];
                    ts[i] = ts[j]
                    ts[j] = t
        new_s = []
        new_s.append("Name                                              Score")
        for i in range(1, len(ts)):
            new_s.append(ts[i][0] + ' ' * (55 - len(ts[i][0]) - len(ts[i][1])) + ts[i][1])
        text = []
        for i in range(len(new_s)):
            text.append(new_s[i])
    for i in range(len(text)):
        temp_text = fnt.render(text[i], 1, (0, 0, 0))
        screen.blit(temp_text, (x, y + 40 * i))
    file.close()

class Menu:
    def __init__(self, punkts_name, punkts_act, punkts_settings, text_file):
        self.punkts_act = punkts_act
        self.punkts_name = punkts_name
        self.punkts = []
        self.text_file = text_file
        for i in range(len(self.punkts_name)):
            self.punkts.append((size[0] // punkts_settings[0] - punkts_settings[1], (size[1] - punkts_settings[2] + i * 80) // punkts_settings[3], self.punkts_name[i], (11, 0, 77), (250, 250, 30), i))

    def render(self, screen, font, punkt):
        for i in self.punkts:
            if punkt == i[5]:
                screen.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                screen.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def menu(self):
        self.done = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while self.done:
            screen.fill((0, 100, 200))
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if ((mp[0] > i[0] and mp[0] < i[0] + 155) and (mp[1] > i[1] - 30 and mp[1] < i[1] + 30)):
                    punkt = i[5]
            self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                        else:
                            punkt = len(self.punkts) - 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                        else:
                            punkt = 0
                    if e.key == 13:
                        exec(self.punkts_act[punkt])
                mp = pygame.mouse.get_pos()
                for i in self.punkts:
                    if ((mp[0] > i[0] and mp[0] < i[0] + 155) and (mp[1] > i[1] - 30 and mp[1] < i[1] + 30)):
                        if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1):
                            exec(self.punkts_act[punkt])
            if (self.text_file != ''):
                drawText(self.text_file[0], self.text_file[1], self.text_file[2], self.text_file[3], self.text_file[4], self.text_file[5])
            window.blit(screen, (0, 0))
            pygame.display.flip()

def mainMenu():
    punkts_name = [u'Играть', u'Уравление', u'Таблица рекордов', u'О нас', u'Выход']
    punkts_act = ['self.done = False', 'keyInfo()', 'records()', 'ourInfo()', 'exit()']
    punkts_settings = (2, 100, 160, 2)
    main_menu = Menu(punkts_name, punkts_act, punkts_settings, '')
    main_menu.menu()

def ourInfo():
    punkts_name = ['Назад']
    punkts_act = ['mainMenu()']
    punkts_settings = (1, size[0] - 50, 50, 1)
    text = ('/home/prom/PycharmProjects/first_big_project/our_info.txt', 'r', 'None', False, 100, 50)
    info_menu = Menu(punkts_name, punkts_act, punkts_settings, text)
    info_menu.menu()

def keyInfo():
    punkts_name = ['Назад']
    punkts_act = ['mainMenu()']
    punkts_settings = (1, size[0] - 50, 50, 1)
    text = ('/home/prom/PycharmProjects/first_big_project/key_info.txt', 'r', 'None', False, 100, 50)
    info_menu = Menu(punkts_name, punkts_act, punkts_settings, text)
    info_menu.menu()

def records():
    punkts_name = ['Назад']
    punkts_act = ['mainMenu()']
    punkts_settings = (1, size[0] - 50, 50, 1)
    text = ('/home/prom/PycharmProjects/first_big_project/highscores.txt', 'r', 'None', True, 100, 50)
    info_menu = Menu(punkts_name, punkts_act, punkts_settings, text)
    info_menu.menu()


def main():
    mainMenu()
    # game();

if __name__ == '__main__':
    main()                                                                                                                                                                                                                                                                                                                                                                                                                                                                
