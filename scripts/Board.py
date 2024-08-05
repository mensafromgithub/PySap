import pygame
from random import randint
from numpy import zeros, full, arange, resize, random
from collections import Counter


from objects.Bomb import Bomb


def pram(cont):
    return [j for i in cont for j in i]


class Board:
    def __init__(self, width, height, screen, bombs=0, cell_w=50, cell_h=50):
        self.pole = pygame.image.load('data/defaultr.jpg').convert()
        self.pole2 = pygame.image.load('data/src.jfif').convert()
        self.pole = pygame.transform.scale(self.pole, (cell_w, cell_h))
        self.pole2 = pygame.transform.scale(self.pole2, (cell_w, cell_h))
        self.image = pygame.image.load('data/doroga.png').convert()
        self.image = pygame.transform.scale(self.image, screen.get_size())
        self.board = full((height, width), self.pole, dtype='object')
        self.coords = [[(0, 0)] * width for i in range(height)]
        self.bomb_pole = zeros((height, width), dtype='object')
        self.counts_pole = zeros((height, width))
        self.screen = screen
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.bombs = bombs
        self.right = self.left
        self.bottom = self.top
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.cells_cost = {0: None,
                     1: None,
                     2: None,
                     3: None,
                     4: None,
                     5: None,
                     6: None,
                     7: None,
                     8: None,
                     9: 0}
        self.nums = {0: self.pole2,
                     1: pygame.image.load('data/1.png').convert(),
                     2: pygame.image.load('data/2.png').convert(),
                     3: pygame.image.load('data/3.png').convert(),
                     4: pygame.image.load('data/4.png').convert(),
                     5: pygame.image.load('data/5.png').convert(),
                     6: pygame.image.load('data/6.png').convert(),
                     7: pygame.image.load('data/7.png').convert(),
                     8: pygame.image.load('data/8.png').convert()}

    def gen_bomb_pole(self):
        c = 0
        for i in arange(len(self.board)):
            for j in arange(len(self.board[0])):
                if randint(0, 1) and c < self.bombs:
                    self.bomb_pole[i][j] = Bomb(self.cell_w, self.cell_h)
                    c += 1
                else:
                    self.bomb_pole[i][j] = 0
        self.bomb_pole = self.bomb_pole.ravel()
        random.default_rng().shuffle(self.bomb_pole[:], axis=0)
        self.bomb_pole = resize(self.bomb_pole, (len(self.board), len(self.board[0])))
        self.counts_up()

    def counts_up(self):
        c = 0
        for i in arange(len(self.board)):
            for j in arange(len(self.board[0])):
                for x in arange(-1, 2):
                    for y in arange(-1, 2):
                        if 0 <= i + x < len(self.board) and 0 <= j + y < len(self.board[0]):
                            c += 0 if self.bomb_pole[i + x][j + y] == 0 else 1
                if self.board[i][j] != self.pole:
                    self.board[i][j] = pygame.transform.scale(self.nums[self.counts_pole[i][j]])
                self.counts_pole[i][j] = c
                c = 0
        self.cells_counts_up()

    def cells_counts_up(self):
        self.cells_cost = Counter(pram(self.counts_pole))
        self.cells_cost[9] = 0
        for i in range(9):
            self.cells_cost[i] = 1 - (self.cells_cost[i] / len(self.board) / len(self.board[0])) / 100

    def set_view2(self, left, right, top, bottom, screen, bombs=0):
        self.bombs = bombs
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.cell_w = (screen.get_size()[0] - self.left - self.right) // len(self.board[0])
        self.cell_h = (screen.get_size()[1] - self.top - self.bottom) // len(self.board)
        for i in arange(1, len(self.board) + 1):
            for j in arange(1, len(self.board[0]) + 1):
                self.coords[i - 1][j - 1] = (self.left + self.cell_w * j, self.top + self.cell_h * i)
        self.res_pole()
        self.render2(screen)
        self.gen_bomb_pole()

    def res_pole(self):
        self.pole = pygame.transform.scale(self.pole, (self.cell_w, self.cell_h))
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j] = self.pole

    def render2(self, screen):
        surf = pygame.Surface(screen.get_size())
        surf.blit(self.image, (0, 0))
        st = (self.left, self.top)
        for i in arange(1, len(self.board) + 1):
            for j in arange(1, len(self.board[0]) + 1):
                surf.blit(self.board[i - 1][j - 1], st)
                pygame.draw.rect(surf, (255, 255, 255), (st, (self.cell_w, self.cell_h)), 1)
                st = (st[0] + self.cell_w, st[1])
            st = (self.left, st[1] + self.cell_h)
        screen.blit(surf, (0, 0))

    def show_bombs(self, screen):
        for i in arange(len(self.board)):
            for j in arange(len(self.board[0])):
                if self.bomb_pole[i][j] != 0:
                    self.board[i][j] = self.bomb_pole[i][j].bomb
        self.render2(screen)
        pygame.display.flip()

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        return self.on_click(cell)

    def get_cell(self, pos):
        for i in arange(len(self.coords)):
            for j in arange(len(self.coords[0])):
                if (self.coords[i][j][0] - self.cell_size < pos[0] < self.coords[i][j][0]) and (
                        self.coords[i][j][1] - self.cell_size < pos[1] < self.coords[i][j][1]):
                    return (j, i)

    def on_click(self, cell):
        try:
            if self.bomb_pole[cell[1]][cell[0]]:
                return 1, 9, 1
            elif self.board[cell[1]][cell[0]] == self.pole:
                return 0, 9, 0
            else:
                self.board[cell[1]][cell[0]] = pygame.transform.scale(self.nums[self.counts_pole[cell[1]][cell[0]]],
                                                                      (self.cell_w, self.cell_h))
            self.render2(self.screen)
            pygame.display.flip()
            return 0, self.counts_pole[cell[1]][cell[0]], 1
        except:
            return 0, 9, 0
