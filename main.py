from sys import exit

import pygame as pg

import Generation.generation
import container

gn = Generation.generation.MazeGen()


class Main(container.Container):

    def __init__(self):
        super().__init__()
        self._main()

    def _main(self):
        rects = gn.draw_maze()
        path_parts = gn.create_path_parts(rects)
        gn.generate_maze(rects, path_parts)

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
