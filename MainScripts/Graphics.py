import pygame
import constants

class Tile:
    def __init__(self, x, y, wi, hi, color):
        self.x = x
        self.y = y
        self.wi = wi
        self.hi = hi
        self.color = color
        #self.animf = (self.x - 5, self.y - 5, self.wi + 10, self.hi + 10)

    def show(self, screen):
        coord = (self.x, self.y, self.wi, self.hi)
        pygame.draw.rect(screen, self.color, coord)

    def hovanim(self, screen):
        animf = (self.x - 5, self.y - 5, self.wi + 10, self.hi + 10)
        pygame.draw.rect(screen, self.color, animf)
        pygame.draw.rect(screen, black, (self.x, self.y, self.wi, self.hi), 3)
