import pygame

class Tile:
    def __init__(self, x, y, wi, hi, color):
        self.x = x
        self.y = y
        self.wi = wi
        self.hi = hi
        self.color = color

    def show(self, screen):
        coord = (self.x, self.y, self.wi, self.hi)
        pygame.draw.rect(screen, self.color, coord)
