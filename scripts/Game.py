import sys
import pygame


from .Board import Board
from .Timer import Timer


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