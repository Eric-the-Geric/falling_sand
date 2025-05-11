import pygame
from src.grid import Grid
from src.particles import (
        Fire,
        Water,
        Smoke,
        Concrete,
        Lava,
        Smoke,
        Sand,
        Wood,
        Acid,
        Particle
        )
from src.settings import *
from src.utils import make_matrix

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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pause = not pause
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.quit()
        if keys[pygame.K_1]:
            sand = 0
        if keys[pygame.K_2]:
          sand = 1
        if keys[pygame.K_3]:
          sand = 2
        if keys[pygame.K_4]:
          sand = 3
        if keys[pygame.K_5]:
            sand = 4
        if keys[pygame.K_6]:
            sand = 5
        if keys[pygame.K_7]:
            sand = 6
        if keys[pygame.K_8]:
            sand = 7
        if keys[pygame.K_r]:
            grid.reset()
       # if keys[pygame.K_SPACE]:
       #     pause = not pause


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
            elif sand == 4:
                #make_matrix(5, y, x, grid, Fire)
                grid.board[y][x] = Fire()
            elif sand == 5:
                make_matrix(5, y, x, grid, Lava)
            elif sand == 6:
                make_matrix(5, y, x, grid, Concrete)

            elif sand == 7:
                make_matrix(5, y, x, grid, Acid)
        if pygame.mouse.get_pressed()[2]:
            mx, my = pygame.mouse.get_pos()
            x, y = mx//SCALE, my//SCALE
            make_matrix(5, y, x, grid, Particle)
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        grid.draw(screen)
        if not pause:
            grid.rules(dt)
            grid.update_processed()

        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60
        dt = clock.tick(FPS) / 1001

    pygame.quit()


if __name__ == "__main__":
    main()

