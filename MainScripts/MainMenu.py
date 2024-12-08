import pygame
from constants import *

pygame.init()
screen = pygame.display.set_mode((400, 400))

menu = True

# Clock
clock = pygame.time.Clock()

hovcol = r
hovcolb = white

font = pygame.font.Font(None, 25)  # None uses the default font, 36 is the font size
ng = font.render(" > New Game", True, hovcol) # middle is antialias
qu = font.render(" > Quit", True, hovcolb)

while menu:
    time_delta = clock.tick(60) / 1000.0  # Seconds passed since the last frame

    mox, moy = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if start:
                with open('master.py') as m:
                    exec(m.read())
                    menu = False
            else:
                menu = False

    ng = font.render(" > New Game", True, hovcol)  # middle is antialias
    qu = font.render(" > Quit", True, hovcolb)

    screen.fill(black)

    if moy < 25:
        hovcol = r
        hovcolb = white
        start = True
    else:
        hovcol = white
        hovcolb = r
        start = False

    screen.blit(ng,(20,20))
    screen.blit(qu,(20,40))

    # Update the display
    pygame.display.flip()
    clock.tick(60)
pygame.quit()