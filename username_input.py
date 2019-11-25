#!/usr/bin/python3
import pygame_textinput
import pygame
import main_menu

def getText(size):
    pygame.init()
    textinput = pygame_textinput.TextInput()
    screen = pygame.display.set_mode((size[0], size[1]))
    clock = pygame.time.Clock()
    while True:
        screen.fill((225, 225, 225))

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == 13:
                    return textinput.get_text()
                    main_menu.mainMenu()
                if e.key == 27:
                    return '-1'
                    main_menu.mainMenu()

        textinput.update(events)
        screen.blit(textinput.get_surface(), (10, 10))

        pygame.display.update()
        clock.tick(30)