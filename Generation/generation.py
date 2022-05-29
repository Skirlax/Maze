import copy
import random
import time

from mazelib import Maze
from mazelib.generate.Prims import Prims
import pygame as pg
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

import container


class MazeGeneration(container.Container):
    def __init__(self):
        super().__init__()


    def draw_the_grid(self, rect_size):
        walls = []
        rects = []
        for y in range(0, self.screen_height,rect_size):
            for x in range(0, self.screen_width, rect_size):
                rect = pg.Rect(x, y, rect_size, rect_size)
                walls.append([[rect.topleft, rect.topright, rect.bottomright, rect.bottomleft],"b"])
                rects.append([rect, "u"])

        return walls, rects

    def generate_maze(self, walls, rects):
        maze = rects
        cell = random.choice(maze)
        cell[1] = "v"
        given_walls = walls.index(cell)
        random_walls = random.choice(given_walls)
        random_wall = random.choice(random_walls[0])

        for rect in rects:
            if rect[0].collidepoint(random_wall) and rect[1] == "u":
                rect[1] = "v"
                cell = rect
                break




