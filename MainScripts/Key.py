import pygame
from constants import *

def Carrier(screen, title, s1, s2, s3):
    # General shape of the key for the carrier
    pygame.draw.rect(screen, darkgray, (715, 200, 120, 200))
    pygame.draw.rect(screen, black, (723, 200, 105, 25))

    #Slots
    pygame.draw.rect(screen, black, (740, 250, 75, 20))
    pygame.draw.rect(screen, black, (740, 300, 75, 20))
    pygame.draw.rect(screen, black, (740, 350, 75, 20))

    #Text
    screen.blit(title, (728, 202))

    #Slot label
    screen.blit(s1, (742, 253))
    screen.blit(s2, (742, 303))
    screen.blit(s3, (742, 353))
