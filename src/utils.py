import random
def make_matrix(width, y, x, grid, particle):
    for i in range(-width//2, width//2):
        for j in range(-width//2, width//2):
            if random.random() > 0.5:
                if grid.within_rows(y+i) and grid.within_cols(x+j):
                    grid.board[y+i][x+j] = particle()
