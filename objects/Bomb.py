import pygame


class Bomb:
    def __init__(self, cell_w, cell_h):
        self.bomb = pygame.image.load('data/mini-bombr.png').convert()
        self.bomb = pygame.transform.scale(self.bomb, (cell_w, cell_h))