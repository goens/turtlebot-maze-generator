#!/usr/bin/env python3

#from cvc5.pythonic import *
import numpy as np
import random
import networkx as nx
from PIL import Image, ImageDraw


def init_maze(n : int, m : int) -> np.ndarray:
    return np.zeros((n,m,n,m),np.int8)

# We represent an n by m maze as an adjacency matrix
# and index the points by their coordinates
# So there is a path from (i,j) to (i',j') iff
# maze[i,j,i',j'] = 1
# This means there is *no* wall in that case.
def random_maze(n : int,m : int) -> np.ndarray:
    maze = init_maze(n+1,m+1)
    for i in range(n):
        for j in range(m):
            if i + 1 < n:
                if random.choice([True,False]):
                  maze[i,j,i+1,j] = 1
            if j + 1 < m:
                if random.choice([True,False]):
                  maze[i,j,i,j+1] = 1
    return maze

def to_walls(maze : np.ndarray) -> np.ndarray:
    n,m,n2,m2 = maze.shape
    assert(n == n2)
    assert(m == m2)

    #there is one more set of walls than cells
    #(because of the boundaries)
    walls = np.zeros(n+1,m+1,n+1,m+1)

    for i in range(n):
        for j in range(m):
            if i == 0:
                walls[i,j,i+1,j] = 1
            if j == 0:
                walls[i,j,i,j+1] = 1
            if i + 1 < n:
                walls[i,j,i+1,j] = 1 - maze[i,j,i+1,j]
            if j + 1 < m:
                walls[i,j,i+1,j] = 1 - maze[i,j,i+1,j]




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


def draw_maze(maze : np.ndarray, cell_size=100, wall_width=4):
    n,m,n2,m2 = maze.shape
    assert(n == n2)
    assert(m == m2)
    image = Image.new('RGB', (cell_size*n, cell_size*m), color = (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # capture draw in here
    def draw_wall(x1 : int, y1 : int, x2 : int, y2 : int, wall_color=(0,0,0)):
        coord_x1 = cell_size/2. + x1 * cell_size
        coord_y1 = cell_size/2. + y1 * cell_size
        coord_x2 = cell_size/2. + x2 * cell_size
        coord_y2 = cell_size/2. + y2 * cell_size
        draw.line([coord_x1,coord_y1,coord_x2,coord_y2], fill=wall_color, width=wall_width)

    for i in range(n):
        for j in range(m):
            # (i,j) = 1 means there is *no* wall between points i and j
            if i + 1 < n:
                print(f"{(i,j)} -> {(i+1,j)} : {not maze[i,j,i+1,j]}")
                if maze[i,j,i+1,j] == 0:
                    wall_color=(0,0,0)
                else:
                    wall_color=(192,192,192)
                draw_wall(i, j, i+1, j, wall_color=wall_color)
                #image.save(f"maze_{i}_{j}_1.png")

            if j + 1 < m:
                print(f"{(i,j)} -> {(i,j+1)} : {not maze[i,j,i,j+1]}")
                if maze[i,j,i,j+1] == 0:
                    wall_color=(0,0,0)
                else:
                    wall_color=(192,192,192)
                draw_wall(i, j, i, j + 1, wall_color=wall_color)
                image.save(f"maze_{i}_{j}_2.png")

    # Save the image
    image.save('maze.png')


rand_maze = random_maze(4,4)
print(rand_maze)
draw_maze(rand_maze)
