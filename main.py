import random
from sys import exit
import pygame as pg
import Generation.generation
import container

gn = Generation.generation.MazeGeneration()

class Main(container.Container):

    def __init__(self):
        super().__init__()
        self._main()

    def _main(self):
        # neighboars = gn.find_neighbors(rects, 50)
        maze = gn.generate_maze()
        gn.visulaize(maze)
        print(maze)
        while True:
            self._check_for_exit()
            self.clock.tick(self.fps)
            pg.display.update()

    def _check_for_exit(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit(0)


if __name__ == "__main__":
    Main()