import random

import pygame as pg

import container


class MazeGen(container.Container):
    def __init__(self):
        super().__init__()

    def draw_maze(self):
        # Just drawing the rectangles visible before pressing space.
        rects = []
        index = 0
        for x in range(0, self.screen_width, self.rect_size):
            for y in range(0, self.screen_height, self.rect_size):
                rects.append(
                    [pg.draw.rect(self.screen, "black", (x, y, self.rect_size, self.rect_size), 2), index])
                index += 1

        return rects

    def create_path_parts(self, rects):
        # Path parts are the walls
        path_parts = []

        column_starts = [x[1] for x in rects if x[0].y == 0]
        for index, rect in enumerate(rects):

            path_parts.append({"rect": index,
                               "free": True, "side": "left", "connects": (
                    rects[index], rects[index - self.rects_in_column] if index >= self.rects_in_column else None)})

            path_parts.append({"rect": index, "free": True, "side": "top",
                               "connects": (
                                   rects[index],
                                   rects[index - 1] if index > 0 and index not in column_starts else None)})

            if (index + 1) % self.rects_in_row == 0:
                path_parts.append({"rect": index, "free": True, "side": "bottom", "connects": (
                    rects[index], rects[
                        index + 1] if index + 1 not in column_starts and index + 1 < self.rects_in_row * self.rects_in_column else None)})

        return [x for x in path_parts if x["connects"][0] is not None and x["connects"][1] is not None]

    def generate_maze(self, rects, path_parts):
        # Generating the maze using slightly edited version of Kruskal's algorithm.
        # For description thanks to: http://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm
        run = True

        first_side = True
        selected_set = None
        blocked_walls = []

        while run:
            if first_side:
                random_wall = random.choice(path_parts)
                first_side = False
                selected_set = random_wall["connects"][0][1]
            else:
                selected_set_parts = [x for x in path_parts if x["connects"][0][1] == selected_set or x["connects"][1][
                    1] == selected_set and x not in blocked_walls]
                random_wall = random.choice(selected_set_parts)

            rect_1 = random_wall["connects"][0]
            rect_2 = random_wall["connects"][1]

            if rect_1[1] != rect_2[1]:
                self.remove_side(rects[random_wall["rect"]][0], random_wall["side"])
                rect_2[1] = selected_set
                rect_1[1] = selected_set
                blocked_walls.append(random_wall)
                # time.sleep(0.1)

            for x in path_parts:
                if x["connects"][0][1] != x["connects"][1][1]:
                    break

            else:
                run = False

        bottoms = [x for x in rects if x[0].y == self.rects_in_column * self.rect_size - self.rect_size]
        tops = [x for x in rects if x[0].y == 0]
        bottom = random.choice(bottoms)
        top = random.choice(tops)
        self.remove_side(bottom[0], "bottom")
        self.remove_side(top[0], "top")
        return blocked_walls, bottom, top

    def remove_side(self, rect, side, color="white"):
        # Removing graphic representation of a wall.
        if side == "left":
            pg.draw.rect(self.screen, color, (rect.topleft[0] - 2, rect.topleft[1], 4, rect.height))
        elif side == "right":
            pg.draw.rect(self.screen, color, (rect.topright[0] - 2, rect.topright[1], 4, rect.height))
        elif side == "top":
            pg.draw.rect(self.screen, color, (rect.topleft[0], rect.topleft[1] - 2, rect.width, 4))
        elif side == "bottom":
            pg.draw.rect(self.screen, color, (rect.bottomleft[0], rect.bottomleft[1] - 2, rect.width, 4))
        pg.display.update()
