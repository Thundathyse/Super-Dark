import pygame
from constants import *

def Carrier(screen, title, s1, s2, s3):
    # General shape of the key for the carrier
    pygame.draw.rect(screen, darkgray, (715, 200, 120, 200))
    pygame.draw.rect(screen, black, (725, 200, 105, 25))

    #Slots
    pygame.draw.rect(screen, black, (750, 250, 50, 20))
    pygame.draw.rect(screen, black, (750, 300, 50, 20))
    pygame.draw.rect(screen, black, (750, 350, 50, 20))

    #Text
    screen.blit(title, (730, 202))

    #Slot label
    screen.blit(s1, (752, 253))
    screen.blit(s2, (752, 303))
    screen.blit(s3, (752, 353))
