import pygame
from constants import *

def Carrier(screen, title, s1, s2, s3):
    # General shape of the key for the carrier
    pygame.draw.rect(screen, darkgray, (715, 200, 150, 200))
    pygame.draw.rect(screen, black, (735, 200, 105, 25))

    #Slots
    pygame.draw.rect(screen, black, (720, 250, 50, 20))
    pygame.draw.rect(screen, black, (720, 280, 50, 20))
    pygame.draw.rect(screen, black, (720, 310, 50, 20))

    #Text
    screen.blit(title, (740, 202))

    #Slot label
    screen.blit(s1, (722, 253))
    screen.blit(s2, (722, 283))
    screen.blit(s3, (722, 313))
