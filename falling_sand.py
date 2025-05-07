import pygame
import numpy as np
from copy import deepcopy
import random

# some constants
FPS = 60
W, H = 1400, 1000
SCALE = 10
G = 2

class Particle:
    def __init__(self, name="air", color=None, density=-100, state=0):
        self.color = color
        self.density = density
        self.state = state
        self.processed = False
        self.name = name
        self.is_flammable = False
        self.converts_to = None
        self.v = 1

    def update(self, grid, y, x, dt):
        pass
    def convert(self):
        pass

class Liquid(Particle):
    def __init__(self, spread=2, name="air", color=None, density=-100, state=0):
        super().__init__(name=name, color=color, density=density, state=state)
        self.v = 1
        self.spread = spread

    def update(self, grid, y, x, dt):
        if not self.processed:
            self.v += G*dt
            dir = np.random.choice([-1, 1])
            below = grid.board[y+1][x]
            sA = grid.board[y][x+dir]
            sB = grid.board[y][x-dir]
            belowA = grid.board[y+1][x+dir]
            belowB = grid.board[y+1][x-dir]
            d = int(self.v)
            s = int(self.spread)
            if below.density < self.density:
                while d <= self.v:
                    if grid.within_cols(x) and grid.within_rows(y+d):
                        below = grid.board[y+d][x]
                        if below.density < self.density:
                            grid.swap(y+d, x, y, x)
                            below.processed = True
                            self.processed = True
                            d +=1
                        else:
                            d+=1
                    else:
                        self.v = 1
                        break


            if belowA.density < self.density:
                while d >=1:
                    if grid.within_cols(x+dir*d) and grid.within_rows(y+d):
                        belowA = grid.board[y+d][x+dir*d]
                        if belowA.density < self.density:
                            grid.swap(y+d, x+dir*d, y, x)
                            belowA.processed = True
                            self.processed = True
                            d-=1
                        else:
                            d-=1
                    else:
                        self.v = 1
                        break

            if belowB.density < self.density:
                while d >=1:
                    if grid.within_cols(x-dir*d) and grid.within_rows(y+d):
                        belowB = grid.board[y+d][x-dir*d]
                        if belowB.density < self.density:
                            grid.swap(y+d, x-dir*d, y, x)
                            belowA.processed = True
                            self.processed = True
                            d -=1
                        else:
                            d -=1
                    else:
                        self.v = 1
                        break

            elif sA.density < self.density:
                while s >=1:
                    if grid.within_cols(x+dir*s) and grid.within_rows(y):
                        sA = grid.board[y][x+dir*s]
                        if sA.density < self.density:
                            grid.swap(y, x+dir*s, y, x)
                            sA.processed = True
                            self.processed = True
                            s-=1
                        else:
                            s-=1
                    else:
                        break


            elif sB.density < self.density:
                while s >=1:
                    if grid.within_cols(x-dir*s) and grid.within_rows(y):
                        sB = grid.board[y][x-dir*s]
                        if sB.density < self.density:
                            grid.swap(y, x-dir*s, y, x)
                            sB.processed = True
                            self.processed = True
                            s-=1
                        else:
                            s-=1
                    else:
                        break
            else:
                self.v = 1
                self.processed = True

class Fire(Particle):
    def __init__(self, name='fire', color='red', density=30, state=5):
        super().__init__(name='fire', color='red', density=30, state=5)

    def update(self, grid, y, x, dt):
        if not self.processed:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    pass


class Wood(Particle):
    def __init__(self, name='wood', color='brown', density=30, state=4):
        super().__init__(name='wood', color='brown', density=30, state=4)

    def update(self, grid, y, x, dt):
        pass

class Smoke(Particle):
    def __init__(self, name='smoke', color='white', density=-1, state=3):
        super().__init__(name='smoke', color='white', density=-1, state=3)

    def update(self, grid, y, x, dt):
        if not self.processed:
            dir = np.random.choice([-1, 1])
            below = grid.board[y-1][x]
            sA = grid.board[y][x+dir]
            sB = grid.board[y][x-dir]
            belowA = grid.board[y-1][x+dir]
            belowB = grid.board[y-1][x-dir]
            if below and below.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y-1][x] = grid.board[y-1][x], grid.board[y][x]

            elif belowA and belowA.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y-1][x+dir] = grid.board[y-1][x+dir], grid.board[y][x]

            elif belowB and belowB.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y-1][x-dir] = grid.board[y-1][x-dir], grid.board[y][x]

            elif sA and sA.density < self.density and random.random() < 0.2:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y][x+dir] = grid.board[y][x+dir], grid.board[y][x]

            elif sB and sB.density < self.density and random.random() < 0.2:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y][x-dir] = grid.board[y][x-dir], grid.board[y][x]

class Water(Liquid):
    def __init__(self, name='water', color='blue', density=3, state=2):
        super().__init__(spread=4, name='water', color='blue', density=3, state=2)

class Sand(Particle):
    def __init__(self, name="sand", color="yellow", density=5, state=1):
        super().__init__(name=name, color=color, density=density, state=state)

    def update(self, grid, y, x, dt):
        if not self.processed:
            self.v += G*dt
            dir = np.random.choice([-1, 1])
            below = grid.board[y+1][x]
            belowA = grid.board[y+1][x+dir]
            belowB = grid.board[y+1][x-dir]
            d = int(self.v)
            if below.density < self.density:
                while d >= 1:
                    if grid.within_cols(x) and grid.within_rows(y+d):
                        below = grid.board[y+d][x]
                        if below.density < self.density:
                            grid.swap(y+d, x, y, x)
                            below.processed = True
                            self.processed = True
                            d -=1
                        else:
                            d-=1
                    else:
                        self.v = 1
                        break


            if belowA.density < self.density:
                while d >=1:
                    if grid.within_cols(x+dir*d) and grid.within_rows(y+d):
                        belowA = grid.board[y+d][x+dir*d]
                        if belowA.density < self.density:
                            grid.swap(y+d, x+dir*d, y, x)
                            belowA.processed = True
                            self.processed = True
                            d-=1
                        else:
                            d-=1
                    else:
                        self.v = 1
                        break

            if belowB.density < self.density:
                while d >=1:
                    if grid.within_cols(x-dir*d) and grid.within_rows(y+d):
                        belowB = grid.board[y+d][x-dir*d]
                        if belowB.density < self.density:
                            grid.swap(y+d, x-dir*d, y, x)
                            belowA.processed = True
                            self.processed = True
                            d -=1
                        else:
                            d -=1
                    else:
                        self.v = 1
                        break

            else:
                self.v = 1


class Grid:
    def __init__(self, width, height):
        self.w, self.h= width, height
        self.board = self._make_board()

    def _make_board(self):
        return [[Particle() for x in range(self.w)] for y in range(self.h)]

    def reset(self):
        self.board = self._make_board()

    def within_cols(self, x):
        return x >= 0 and x < self.w-1

    def within_rows(self, y):
        return y >= 0 and y < self.h-1

    def swap(self, y1, x1, y2, x2):
        self.board[y1][x1], self.board[y2][x2] = self.board[y2][x2], self.board[y1][x1]


    def rules(self, dt):
        if random.random() < 0.5:
            for y in range(self.h-1, -1, -1):
                for x in range(self.w-1, -1, -1):
                    particle = self.board[y][x]
                    particle.update(self, y, x, dt)
        else:
            for y in range(0, self.h-1):
                for x in range(0, self.w):
                    particle = self.board[y][x]
                    particle.update(self, y, x, dt)


    def update_processed(self):
        for y in range(self.h-1):
            for x in range(1, self.w-1):
                self.board[y][x].processed = False


    def draw(self, screen):
        for y, row in enumerate(self.board):
            for x, particle in enumerate(row):
                if particle.state == 1 or particle.state == 2 or particle.state==3 or particle.state==4:
                    pygame.draw.rect(screen, particle.color, pygame.rect.Rect([x*SCALE-1, y*SCALE-1, SCALE, SCALE]))


def make_matrix(width, y, x, grid, particle):
    for i in range(-width//2, width//2):
        for j in range(-width//2, width//2):
            if random.random() > 0.5:
                if grid.within_rows(y+i) and grid.within_cols(x+j):
                    grid.board[y+i][x+j] = particle()


def main():
    sand = 0
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    dt = 0
    running = True
    grid = Grid(W//SCALE, H//SCALE)
    pause = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.quit()
        if keys[pygame.K_1]:
            sand = 0
        elif keys[pygame.K_2]:
            sand = 1
        elif keys[pygame.K_3]:
            sand = 2
        elif keys[pygame.K_4]:
            sand = 3
        if keys[pygame.K_r]:
            grid.reset()
        if keys[pygame.K_SPACE]:
            pause = not pause


        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            x, y = mx//SCALE, my//SCALE
            if sand == 0:
                make_matrix(5, y, x, grid, Sand)
                #grid.board[y][x] = Sand()
            elif sand == 1:
                make_matrix(5, y, x, grid, Water)
                #grid.board[y][x] = Water()
            elif sand == 2:
                make_matrix(5, y, x, grid, Smoke)
            elif sand == 3:
                make_matrix(5, y, x, grid, Wood)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        grid.draw(screen)
        if not pause:
            grid.rules(dt)
            grid.update_processed()

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60
        dt = clock.tick(60) / 100

    pygame.quit()





if __name__ == "__main__":
    main()

