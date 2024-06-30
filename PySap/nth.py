import pygame
import sys
from random import randint
from numpy import zeros, full, arange, resize, random
from time import time


def pram(cont):
    return [j for i in cont for j in i]


def depram(cont, s1, s2):
    return [[cont[s2 * x + y] for y in range(s2)] for x in range(s1)]


class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.c = 0

    def start(self):
        self.start_time = time()

    def end(self):
        if not self.c:
            self.end_time = time()
            self.c = 1


class Game:
    def __init__(self, size, config=None):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.image = pygame.image.load('doroga.png').convert()
        self.image = pygame.transform.scale(self.image, self.screen.get_size())
        self.sts = 1
        self.conets = 0
        self.timer = Timer()
        self.game()

    def game(self):
        self.start()
        self.board = Board(30, 16, self.screen, bombs=100)
        self.board.set_view2(20, 20, 20, 20, self.screen, 100)
        self.bombed = 0
        self.show = 0
        n = 1
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and (not self.sts) and (not self.conets):
                    res = self.board.get_click(event.pos)
                    self.bombed = res
                    self.conets = self.bombed
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and self.sts:
                        self.sts = 0
                        self.st()
                    if event.key == pygame.K_1 and (not self.sts) and (self.conets) and (not self.show):
                        self.conets = 0
                        self.bombed = 0
                        self.st()
                    if event.key == pygame.K_2 and (not self.sts) and (self.conets):
                        self.show = not self.show
            if self.show:
                self.board.show_bombs(self.screen)
            elif self.conets and self.bombed:
                self.fin('bombed')
            elif pram(self.board.board).count(self.board.pole) == self.board.bombs:
                print(self.board.bombs)
                self.conets = 1
                self.fin('win')

    def start(self):
        surf = pygame.Surface(self.screen.get_size())
        font = pygame.font.Font(None, 30)
        string_rendered = font.render('Нажмите [1] для начала в режиме игры 30X16 клеток', 1, pygame.Color('white'))
        x, y = self.screen.get_size()
        box = string_rendered.get_rect()
        surf.blit(self.image, (0, 0))
        surf.blit(string_rendered, (10 + box[2] // 2, y - 10 - box[3] // 2))
        self.screen.blit(surf, (0, 0))
        pygame.display.flip()

    def st(self):
        self.timer.start()
        self.timer.c = 0
        self.oard = Board(30, 16, self.screen, bombs=100)  # x, y
        self.board.set_view2(20, 20, 20, 20, self.screen, 100)
        self.board.render2(self.screen)
        pygame.display.flip()

    def fin(self, status=None):
        self.timer.end()
        font = pygame.font.Font(None, 30)
        if status == 'win':
            string_rendered = font.render(f'Победа Время: {self.timer.end_time - self.timer.start_time}', 1,
                                          pygame.Color('white'))
        elif status == 'bombed':
            string_rendered = font.render(f'Game over Time: {self.timer.end_time - self.timer.start_time}', 1,
                                          pygame.Color('white'))
        x, y = self.screen.get_size()
        box = string_rendered.get_rect()
        string_rendered2 = font.render('Нажмите [1] для начала в режиме игры 30X16 клеток', 1, pygame.Color('white'))
        box2 = string_rendered2.get_rect()
        string_rendered3 = font.render('Нажмите [2] для просмотра поля', 1, pygame.Color('white'))
        surf = pygame.Surface(self.screen.get_size())
        surf.blit(self.image, (0, 0))
        surf.blit(string_rendered, (x // 2 - box[2] // 2, y // 2 - box[3] // 2))
        surf.blit(string_rendered2, (10 + box2[2] // 2, y - 10 - box2[3] // 2))
        surf.blit(string_rendered3, (10 + box2[2] // 2, y - 30 - box2[3] // 2))
        self.screen.blit(surf, (0, 0))
        pygame.display.flip()


    def terminate(self):
        pygame.quit()
        sys.exit()


class Bomb:
    def __init__(self, cell_w, cell_h):
        self.bomb = pygame.image.load('mini-bombr.png').convert()
        self.bomb = pygame.transform.scale(self.bomb, (cell_w, cell_h))


class Board:
    def __init__(self, width, height, screen, bombs=0, cell_w=50, cell_h=50):
        self.pole = pygame.image.load('defaultr.jpg').convert()
        self.pole2 = pygame.image.load('src.jfif').convert()
        self.pole = pygame.transform.scale(self.pole, (cell_w, cell_h))
        self.pole2 = pygame.transform.scale(self.pole2, (cell_w, cell_h))
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
        self.gen_bomb_pole()
        self.nums = {0: self.pole2,
                     1: pygame.image.load('1.png').convert(),
                     2: pygame.image.load('2.png').convert(),
                     3: pygame.image.load('3.png').convert(),
                     4: pygame.image.load('4.png').convert(),
                     5: pygame.image.load('5.png').convert(),
                     6: pygame.image.load('6.png').convert(),
                     7: pygame.image.load('7.png').convert(),
                     8: pygame.image.load('8.png').convert()}

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

    def set_view2(self, left, right, top, bottom, screen, bombs=0):
        self.bombs = bombs
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.cell_w = (screen.get_size()[0] - self.left - self.right) // len(self.board[0])
        self.cell_h = (screen.get_size()[1] - self.top - self.bottom) // len(self.board)
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
        image = pygame.image.load('doroga.png').convert()
        image = pygame.transform.scale(image, screen.get_size())
        surf.blit(image, (0, 0))
        st = (self.left, self.top)
        for i in arange(1, len(self.board) + 1):
            for j in arange(1, len(self.board[0]) + 1):
                surf.blit(self.board[i - 1][j - 1], st)
                pygame.draw.rect(surf, (255, 255, 255), (st, (self.cell_w, self.cell_h)), 1)
                st = (st[0] + self.cell_w, st[1])
                self.coords[i - 1][j - 1] = (self.left + self.cell_w * j, self.top + self.cell_h * i)
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
                self.board[cell[1]][cell[0]] = pygame.transform.scale(self.bomb_pole[cell[1]][cell[0]].bomb,
                                                                      (self.cell_w, self.cell_h))
                return 1, [None]
            else:
                self.board[cell[1]][cell[0]] = pygame.transform.scale(self.nums[self.counts_pole[cell[1]][cell[0]]],
                                                                      (self.cell_w, self.cell_h))
            self.render2(self.screen)
            pygame.display.flip()
            return 0
        except:
            return None


if __name__ == '__main__':
    Game((1200, 1000))
