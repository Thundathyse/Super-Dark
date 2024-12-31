import pygame
from constants import *

class Tile:
    def __init__(self, x, y, wi, hi, color, mean):
        self.x = x
        self.y = y
        self.wi = wi
        self.hi = hi
        self.color = color
        self.mean = mean

    def show(self, screen):
        coord = (self.x, self.y, self.wi, self.hi)
        pygame.draw.rect(screen, self.color, coord)
        screen.blit(self.mean, (self.x, self.y))

    def hovanim(self, screen):
        animf = (self.x - (self.wi/12), self.y - (self.hi/12), self.wi + (self.wi/12), self.hi + (self.hi/12))
        pygame.draw.rect(screen, black, (self.x, self.y, self.wi, self.hi))
        pygame.draw.rect(screen, self.color, animf)
        pygame.draw.rect(screen, black, animf, 3)
        screen.blit(self.mean, (self.x - (self.wi/12), self.y - (self.hi/12)))


class inTile:
    def __init__(self, x, y, wi, hi, color, mean, bsprite, fsprite):
        self.x = x
        self.y = y
        self.wi = wi
        self.hi = hi
        self.color = color
        self.mean = mean
        self.bsprite = bsprite
        self.fsprite = fsprite

    def show(self, screen):
        coord = (self.x, self.y, self.wi, self.hi)
        pygame.draw.rect(screen, self.color, coord)
        screen.blit(self.mean, (self.x, self.y))

    def hovanim(self, screen):
        animf = (self.x - (self.wi / 12), self.y - (self.hi / 12), self.wi + (self.wi / 12), self.hi + (self.hi / 12))
        pygame.draw.rect(screen, black, (self.x, self.y, self.wi, self.hi))
        pygame.draw.rect(screen, self.color, animf)
        pygame.draw.rect(screen, black, animf, 3)
        screen.blit(self.mean, (self.x - (self.wi / 12) + 5, self.y - (self.hi / 12) + 5))
        screen.blit(self.bsprite, (330, 650))
        screen.blit(self.fsprite, (480, 650))