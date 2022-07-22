from sys import exit

import pygame as pg

import Generation.generation
import Solving.solving
import container

gn = Generation.generation.MazeGen()
solve = Solving.solving.SolveMaze()


class Main(container.Container):

    def __init__(self):
        super().__init__()
        self._main()

    def _main(self):
        self.screen.fill("white")
        rects = gn.draw_maze()
        pg.display.update()
        pressed = False
        while not pressed:
            self._check_for_exit()
            pressed = bool(pg.key.get_pressed()[pg.K_SPACE])
        path_parts = gn.create_path_parts(rects)
        removed_walls, start, end = gn.generate_maze(rects, path_parts)
        solve.solve([x for x in path_parts if x not in removed_walls], rects, start, end)

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
