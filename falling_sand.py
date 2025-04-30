import pygame
import numpy as np
from copy import deepcopy
import random

# some constants
FPS = 60
W, H = 1000, 1000
SCALE = 10


paticle_map = {
        "air": {
            "color": None,
            "density": None,
            "state": 0,
            "gravity": 0,
                },
        "sand": {
            "color": "yellow",
            "density": 10,
            "state": 1,
            "gravity": 2,
            },
        "water": {
            "color": "blue",
            "density": 5,
            "state": 2,
            "gravity": 1,
            }
        }

class Particle:
    def __init__(self, name="air", color=None, density=-100, state=0, gravity=0):
        self.color = color
        self.density = density
        self.g = gravity,
        self.state = state
        self.processed = False
        self.name = name

    def update(self, grid, y, x):
        pass

class Wood(Particle):
    def __init__(self, name='wood', color='brown', density=30, state=4, gravity=2):
        super().__init__(name='wood', color='brown', density=30, state=4, gravity=2)

    def update(self, grid, y, x):
        pass
class Smoke(Particle):
    def __init__(self, name='smoke', color='white', density=-1, state=3, gravity=2):
        super().__init__(name='smoke', color='white', density=-1, state=3, gravity=2)

    def update(self, grid, y, x):
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

            elif sA and sA.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y][x+dir] = grid.board[y][x+dir], grid.board[y][x]

            elif sB and sB.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y][x-dir] = grid.board[y][x-dir], grid.board[y][x]

class Water(Particle):
    def __init__(self, name='water', color='blue', density=3, state=2, gravity=2):
        super().__init__(name='water', color='blue', density=3, state=2, gravity=2)

    def update(self, grid, y, x):
        if not self.processed:
            dir = np.random.choice([-1, 1])
            below = grid.board[y+1][x]
            sA = grid.board[y][x+dir]
            sB = grid.board[y][x-dir]
            belowA = grid.board[y+1][x+dir]
            belowB = grid.board[y+1][x-dir]
            if below and below.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y+1][x] = grid.board[y+1][x], grid.board[y][x]

            elif belowA and belowA.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y+1][x+dir] = grid.board[y+1][x+dir], grid.board[y][x]

            elif belowB and belowB.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y+1][x-dir] = grid.board[y+1][x-dir], grid.board[y][x]

            elif sA and sA.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y][x+dir] = grid.board[y][x+dir], grid.board[y][x]

            elif sB and sB.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y][x-dir] = grid.board[y][x-dir], grid.board[y][x]


class Sand(Particle):
    def __init__(self, name="sand", color="yellow", density=5, state=1, gravity=2):
        super().__init__(name=name, color=color, density=5, state=1, gravity=2)

    def update(self, grid, y, x):
        if not self.processed:
            dir = np.random.choice([-1, 1])
            below = grid.board[y+1][x]
            belowA = grid.board[y+1][x+dir]
            belowB = grid.board[y+1][x-dir]
            if below and below.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y+1][x] = grid.board[y+1][x], grid.board[y][x]

            elif belowA and belowA.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y+1][x+dir] = grid.board[y+1][x+dir], grid.board[y][x]

            elif belowB and belowB.density < self.density:
                self.processed = True
                below.processed = True
                grid.board[y][x], grid.board[y+1][x-dir] = grid.board[y+1][x-dir], grid.board[y][x]


class Grid:
    def __init__(self, width, height):
        self.w, self.h= width, height
        self.board = self._make_board()

    def _make_board(self):
        return [[Particle() for x in range(self.w)] for y in range(self.h)]

    def within_cols(self, x):
        return x >= 0 and x < self.w-1

    def within_rows(self, y):
        return y >= 0 and y < self.h-1


    def rules(self):
        for y in range(self.h-1, -1, -1):
            for x in range(self.w-1, -1, -1):
                particle = self.board[y][x]
                particle.update(self, y, x)

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
    # pygame setup
    #curr = 0
    #particles = [Sand, Water]
    sand = True
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    dt = 0
    running = True
    grid = Grid(W//SCALE, H//SCALE)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.quit()
        if keys[pygame.K_SPACE]:
            sand = (sand + 1) %4
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            x, y = mx//SCALE, my//SCALE
            if sand == 0:
                make_matrix(5, y, x, grid, Sand)
            elif sand == 1:
                make_matrix(5, y, x, grid, Water)
            elif sand == 2:
                make_matrix(5, y, x, grid, Smoke)
            elif sand == 3:
                make_matrix(5, y, x, grid, Wood)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        grid.draw(screen)
        grid.rules()
        grid.update_processed()

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60
        dt = clock.tick(60) / 100

    pygame.quit()





if __name__ == "__main__":
    main()

