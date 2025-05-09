from src.particles import Particle
from src.settings import *
import random
import pygame
class Grid:
    def __init__(self, width, height):
        self.w, self.h= width, height
        self.board = self._make_board()

    def _make_board(self):
        return [[Particle() for x in range(self.w)] for y in range(self.h)]

    def reset(self):
        self.board = self._make_board()

    def within_cols(self, x):
        return x > 0 and x < self.w-1

    def within_rows(self, y):
        return y > 0 and y < self.h-1

    def swap(self, y1, x1, y2, x2):
        self.board[y1][x1], self.board[y2][x2] = self.board[y2][x2], self.board[y1][x1]


    def rules(self, dt):
        if random.random() < 0.5:
            for y in range(self.h, -1, -1):
                for x in range(self.w-1, -1, -1):
                    if self.within_cols(x) and self.within_rows(y):
                        particle = self.board[y][x]
                        if particle.state != 0:
                            particle = self.board[y][x]
                            print(particle.health)
                            if particle.health < 1:
                                self.board[y][x] = Particle()
                            particle.update(self, y, x, dt)
        else:
            for y in range(0, self.h):
                for x in range(0, self.w):
                    if self.within_cols(x) and self.within_rows(y):
                        particle = self.board[y][x]
                        if particle.state != 0:
                            particle = self.board[y][x]
                            particle.update(self, y, x, dt)


    def update_processed(self):
        for y in range(self.h-1):
            for x in range(1, self.w-1):
                self.board[y][x].processed = False


    def draw(self, screen):
        for y, row in enumerate(self.board):
            for x, particle in enumerate(row):
                if particle.state != 0:
                    pygame.draw.rect(screen, particle.color, pygame.rect.Rect([x*SCALE, y*SCALE, SCALE, SCALE]))
