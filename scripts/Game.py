import sys
import pygame
from os import listdir
from os.path import isfile, join
from json import loads, dumps
from pickle import load, dump
import time


from .Board import Board
from .Timer import Timer
from objects.Bomb import Bomb


def pram(cont):
    return [j for i in cont for j in i]


def depram(cont, s1, s2):
    return [[cont[s2 * x + y] for y in range(s2)] for x in range(s1)]


class Game:
    def __init__(self, size, config=None):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.image = pygame.image.load('data/doroga.png').convert()
        self.image = pygame.transform.scale(self.image, self.screen.get_size())
        self.timer = Timer()
        self.bombed = 0
        self.show = 0
        self.sts = 1
        self.conets = 0
        self.game()

    def game(self):
        self.start()
        t = 0
        c = 0
        while 1:
            if time.time() - t >= 10:
                c = 0
                t = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and (not self.sts) and (not self.conets):
                    res = self.board.get_click(event.pos)
                    self.bombed = res[0]
                    self.conets = self.bombed
                    t = 0
                    c += 0 if res[0] else 1
                    self.score += 100 * self.board.cells_cost[res[1]] * c
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print(self.save_board('Vasya'))
                    if event.key == pygame.K_w:
                        print(self.load_board('Vasya_1'))
                    if event.key == pygame.K_LCTRL and event.key == pygame.K_s:
                        print(self.make_save())
                    if event.key == pygame.K_1 and self.sts:
                        t = 0
                        c = 0
                        self.st()
                    if event.key == pygame.K_1 and (not self.sts) and (self.conets) and (not self.show):
                        t = 0
                        c = 0
                        self.st()
                    if event.key == pygame.K_2 and (not self.sts) and (self.conets):
                        self.show = not self.show
            if self.conets:
                if self.show:
                    self.board.show_bombs(self.screen)
                elif self.bombed:
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

    def st(self, board=None):
        self.score = 0
        self.sts = 0
        self.conets = 0
        self.bombed = 0
        self.timer.start()
        self.board = Board(30, 16, self.screen, bombs=100)  # x, y
        self.board.set_view2(20, 20, 20, 20, self.screen, 100)
        if board:
            self.board.bombs = board['board']['bombs']
            for i in range(len(board['board']['bomb_pole'])):
                for j in range(len(board['board']['bomb_pole'][0])):
                    if board['board']['bomb_pole'][i][j]:
                        board['board']['bomb_pole'][i][j] = Bomb(self.board.cell_w, self.board.cell_h)
            self.board.bomb_pole = board['board']['bomb_pole']
            self.board.counts_up()
            self.board.cells_counts_up()
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
        string_rendered4 = font.render(f'Score: {self.score}', 1, pygame.Color('white'))
        surf = pygame.Surface(self.screen.get_size())
        surf.blit(self.image, (0, 0))
        surf.blit(string_rendered4, (x // 2 - box[2] // 2, y // 2 - box[3] // 2))
        surf.blit(string_rendered, (x // 2 - box[2] // 2, y // 2 - 30 - box[3] // 2))
        surf.blit(string_rendered2, (10 + box2[2] // 2, y - 10 - box2[3] // 2))
        surf.blit(string_rendered3, (10 + box2[2] // 2, y - 30 - box2[3] // 2))
        self.screen.blit(surf, (0, 0))
        pygame.display.flip()


    def terminate(self):
        self.make_save()
        pygame.quit()
        sys.exit()

    def make_save(self):
        try:
            onlyfiles = sorted([f for f in listdir('saves') if isfile(join('saves', f))])
            op = [[0 for j in range(len(self.board.board[0]))] for i in range(len(self.board.board))]
            bo = [[0 for j in range(len(self.board.board[0]))] for i in range(len(self.board.board))]
            for i in range(len(self.board.board)):
                for j in range(len(self.board.board[0])):
                    if self.board.board[i][j] != self.board.pole:
                        op[i][j] = 1
                    if self.board.bomb_pole[i][j]:
                        bo[i][j] = 1
            js = {'board': {'op': op, 'count_pole': self.board.counts_pole.tolist(), 'bomb_pole': bo, 'bombs': self.board.bombs}, 'game': {'sts': self.sts, 'conets': self.conets, 'start_time': self.timer.start_time, 'end_time': self.timer.end_time}}
            if onlyfiles:
                with open('saves/save_' + str(int(onlyfiles[-1][-6]) + 1) + '.json', 'w') as f:
                    f.write(dumps(js))
            else:
                with open('saves/save_0.json', 'w') as f:
                    f.write(dumps(js))
            return 1
        except:
            return 0

    def load_save(self):
        try:
            return 1
        except:
            return 0

    def save_board(self, name):
        try:
            bo = [[0 for j in range(len(self.board.board[0]))] for i in range(len(self.board.board))]
            for i in range(len(self.board.board)):
                for j in range(len(self.board.board[0])):
                    if self.board.bomb_pole[i][j]:
                        bo[i][j] = 1
            js = {'board': {'bomb_pole': bo, 'bombs': self.board.bombs}}
            with open('boards/' + name + '.json', 'w') as f:
                f.write(dumps(js))
            return 1
        except:
            return 0

    def load_board(self, name):
        try:
            with open('boards/' + name + '.json', 'r') as f:
                js = loads(f.read())
                self.st(js)
            return 1
        except:
            return 0
