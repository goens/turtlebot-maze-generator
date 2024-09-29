#!/usr/bin/env python3

#from cvc5.pythonic import *
import numpy as np
import random
import networkx as nx
from PIL import Image, ImageDraw


# We represent an n by m maze as an adjacency matrix
# and index the points by their coordinates
# So there is a path from (i,j) to (i',j') iff
# maze[i,j,i',j'] = 1
def init_maze(n : int,m : int) -> np.ndarray:
    return np.zeros((n,m,n,m),np.int8)

def random_maze(n : int,m : int) -> np.ndarray:
    maze = init_maze(n,m)
    for i in range(n-1):
        for j in range(m-1):
            if random.choice([True,False]):
              maze[i,j,i+1,j] = 1
            if random.choice([True,False]):
              maze[i,j,i,j+1] = 1
    return maze

def to_adjacency_matrix(maze : np.ndarray) -> np.ndarray:
    n,m,n2,m2 = maze.shape
    assert(n == n2)
    assert(m == m2)
    for i in range(n-1):
        for j in range(m-1):
                if maze[i,j,i+1,j] == 0:
                  draw_wall((j + 1) * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size)
                if maze[i,j,i,j+1] == 0:
                  draw_wall(j * cell_size, (i + 1) * cell_size, (j + 1) * cell_size, (i + 1) * cell_size)


def get_adjacency_graph(maze : np.ndarray) -> nx.Graph:
    n,m,n2,m2 = maze.shape
    assert(n == n2)
    assert(m == m2)
    for i in range(n-1):
        for j in range(m-1):
                if maze[i,j,i+1,j] == 0:
                  draw_wall((j + 1) * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size)
                if maze[i,j,i,j+1] == 0:
                  draw_wall(j * cell_size, (i + 1) * cell_size, (j + 1) * cell_size, (i + 1) * cell_size)


def draw_maze(maze : np.ndarray, cell_size=100, wall_color=(0,0,0), wall_width=4):
    n,m,n2,m2 = maze.shape
    assert(n == n2)
    assert(m == m2)
    image = Image.new('RGB', (cell_size*n, cell_size*m), color = (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # capture draw in here
    def draw_wall(x0 : int, y0 : int, x1 : int, y1 : int):
        draw.line([x0, y0, x1, y1], fill=wall_color, width=wall_width)

    for i in range(n-1):
        for j in range(m-1):
                # (i,j) = 1 means there is *no* wall between points i and j
                if maze[i,j,i+1,j] == 0:
                  draw_wall((j + 1) * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size)
                if maze[i,j,i,j+1] == 0:
                  draw_wall(j * cell_size, (i + 1) * cell_size, (j + 1) * cell_size, (i + 1) * cell_size)

    # Save the image
    image.save('maze.png')


rand_maze = random_maze(2,2)
print(rand_maze)
draw_maze(rand_maze)
