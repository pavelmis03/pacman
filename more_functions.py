import pygame
import main_menu
import username_input

def drawText(file, param, font_decor, table, x, y):
    fnt = pygame.font.SysFont(font_decor, 25, bold=True, italic=False)
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
                    t = ts[i]
                    ts[i] = ts[j]
                    ts[j] = t
        ts.reverse()
        new_s = []
        new_s.append("Name                                              Score")
        new_s.append("                                                       ")
        rng = 0
        if (len(ts) > 14):
            rng = 14

        else:
            rng = len(ts)
        for i in range(rng):
            new_s.append(ts[i][0] + ' ' * (55 - len(ts[i][0]) - len(ts[i][1])) + ts[i][1])
        text = []
        for i in range(len(new_s)):
            text.append(new_s[i])
    for i in range(len(text)):
        temp_text = fnt.render(text[i], 1, (0, 0, 0))
        main_menu.screen.blit(temp_text, (x, y + 40 * i))
    file.close()


def correctName(name):
    if (len(name) > 30 or len(name) < 3):
        return False
    for i in range(len(name)):
        if not(name[i].isalpha()):
            return False
    return True

def records_registration(score):
    name = username_input.getText(main_menu.size)
    if (name == '-1'):
        return
    if (correctName(name)):
        f = open('highscores.txt', 'a')
        f.write(name + ' ' * (55 - len(name) - len(str(score))) + str(score) + "\n")
        f.close()
        f = open('highscores.txt', 'r')
        s = f.readlines()
        ts = []
        for i in range(len(s)):
            ts.append(s[i].split())
        for i in range(1, len(s)):
            for j in range(i + 1, len(s)):
                if (float(ts[i][1]) >= float(ts[j][1])):
                    t = ts[i]
                    ts[i] = ts[j]
                    ts[j] = t
        f.close()
        main_menu.mainMenu()
    else:
        records_registration(score)