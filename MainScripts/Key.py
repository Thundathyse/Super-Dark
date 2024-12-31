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

def Key(screen, title, titlet, cert, te):
    # General shape of the key for the key
    pygame.draw.rect(screen, black, (300, 610, 400, 130))

    #Slot
    pygame.draw.rect(screen, white, (310, 640, 100, 80))
    pygame.draw.rect(screen, white, (450, 640, 100, 80))


    #Text
    screen.blit(title, (310, 615))
    screen.blit(titlet, (450, 615))
    screen.blit(cert, (590, 615))
    screen.blit(te, (580, 630))

def turnBanner(screen, turn, nom):
    # General shape of the key for the key
    pygame.draw.rect(screen, black, (300, 100, 400, 30))
    #Text
    screen.blit(turn, (310, 105))
    screen.blit(nom, (470, 105))

