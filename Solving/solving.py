import copy

import pygame as pg
from stopwatch import Stopwatch
import container

sw = Stopwatch().reset()

class SolveMaze(container.Container):
    def __init__(self):
        super().__init__()

    def create_walls_dict(self, rects, path_parts):
        # Creating a list of dictionaries containing rect id and all its walls, so it's easier to orient in.
        walls = []

        for index, rect in enumerate(rects):
            wall_names = []

            current_parts = list(filter(lambda x: x["connects"][0][0] == rect[0] or x["connects"][1][0] == rect[0], path_parts))
            if rect[0].x == 0:
                wall_names.append("left")
            if rect[0].x == self.screen_width - self.rect_size:
                wall_names.append("right")
            if rect[0].y == 0:
                wall_names.append("up")
            if rect[0].y == self.screen_height - self.rect_size:
                wall_names.append("down")

            if not current_parts:
                walls.append({"rect_number": index, "walls": wall_names})
                continue
            for part in current_parts:
                if part["side"] == "top":
                    if part["connects"][0][0] == pg.Rect(rect[0].x, rect[0].y + self.rect_size, self.rect_size,
                                                         self.rect_size):
                        wall_names.append("down")
                    if part["connects"][1][0] == pg.Rect(rect[0].x, rect[0].y - self.rect_size, self.rect_size,
                                                         self.rect_size):
                        wall_names.append("up")


                if part["side"] == "left":
                    if part["connects"][0][0] == pg.Rect(rect[0].x + self.rect_size, rect[0].y, self.rect_size,
                                                         self.rect_size):
                        wall_names.append("right")
                    if part["connects"][1][0] == pg.Rect(rect[0].x - self.rect_size, rect[0].y, self.rect_size,
                                                         self.rect_size):
                        wall_names.append("left")



                if current_parts.index(part) == len(current_parts) - 1:
                    wall_names = list(set(wall_names))
                    walls.append({"rect_number": index, "walls": wall_names})




        return walls

    def solve(self, path_parts, rects, start, end):
        # Main algorithm part. This is just a wall follower with focus on the left wall.

        rotation = 0
        path = [start[0]]
        current_position = [start[0].x, start[0].y]
        end_position = [end[0].x, end[0].y]
        walls = self.create_walls_dict(rects, path_parts)
        rects = [x[0] for x in rects]
        sw.start()

        while current_position != end_position:
            possible_moves = ["left", "right", "up", "down"]
            current_rect_index = rects.index(
                pg.Rect(current_position[0], current_position[1], self.rect_size, self.rect_size))
            current_walls = [x for x in walls if x["rect_number"] == current_rect_index]
            possible_moves = [x for x in possible_moves if x not in current_walls[0]["walls"]]

            if rotation >= 360:
                rotation = 0

            if self.get_orientation_name(rotation, "left") in possible_moves:
                possible_moves_choice = self.get_orientation_name(rotation, "left")
                move_value = self.move_value(possible_moves_choice, current_position)
                rotation += 90
            elif self.get_orientation_name(rotation, "up") in possible_moves:
                possible_moves_choice = self.get_orientation_name(rotation, "up")
                move_value = self.move_value(possible_moves_choice, current_position)


            # and self.get_orientation_name(rotation,
            #                               "left") not in possible_moves

            elif self.get_orientation_name(rotation, "right") in possible_moves:
                possible_moves_choice = self.get_orientation_name(rotation, "right")
                move_value = self.move_value(possible_moves_choice, current_position)
                rotation -= 90
            else:
                rotation += 180
                continue

            current_position = move_value
            path.append(pg.Rect(current_position[0], current_position[1], self.rect_size, self.rect_size))

            self.visualize(current_position, possible_moves_choice,start[0])
        self.filter_best_path(path,end[0],start[0])
            # time.sleep(0.2)

        # if rotation >= 360:
        #     rotation = 0
        #
        # if self.get_orientation_name(rotation, "up") in possible_moves and self.get_orientation_name(rotation,
        #                                                                                              "left") not in possible_moves:
        #     possible_moves_choice = self.get_orientation_name(rotation, "up")
        #     move_value = self.move_value(possible_moves_choice, current_position)
        # elif self.get_orientation_name(rotation, "left") in possible_moves:
        #     possible_moves_choice = self.get_orientation_name(rotation, "left")
        #     move_value = self.move_value(possible_moves_choice, current_position)
        #     rotation += 90
        #
        # elif self.get_orientation_name(rotation, "right") in possible_moves and self.get_orientation_name(rotation,
        #                                                                                                   "up") not in possible_moves:
        #     possible_moves_choice = self.get_orientation_name(rotation, "right")
        #     move_value = self.move_value(possible_moves_choice, current_position)
        #     rotation -= 90
        # else:
        #     rotation += 180
        #     continue

    def move_value(self, direction, current_position):
        # From direction where we want to move, this method return position where to move to.
        if direction == "left":
            return [current_position[0] - self.rect_size, current_position[1]]

        elif direction == "right":
            return [current_position[0] + self.rect_size, current_position[1]]

        elif direction == "up":
            return [current_position[0], current_position[1] - self.rect_size]

        elif direction == "down":
            return [current_position[0], current_position[1] + self.rect_size]

    def visualize(self, position, move_value, start):
        # Drawing the blue circle and erasing the previous one.
        move_value = self.opposite(move_value)
        move_value = self.move_value(move_value, position)
        pg.draw.circle(self.screen, "blue", (position[0] + self.rect_size // 2, position[1] + self.rect_size // 2), 15)

        if move_value[0] != start[0] or move_value[1] != start[1]:
            pg.draw.circle(self.screen, "white", (move_value[0] + self.rect_size // 2, move_value[1] + self.rect_size // 2),
                           15)

        pg.display.update()

    def opposite(self, direction):

        if direction == "left":
            return "right"
        elif direction == "right":
            return "left"
        elif direction == "up":
            return "down"
        elif direction == "down":
            return "up"

    def get_orientation_name(self, orientation, move_choice):
        # If we are headed some direction, different from the base one,
        # return what is the new direction from the base one.
        if orientation < 0:
            orientation += 360
        if orientation == 0:
            return move_choice
        elif orientation == 90:
            if move_choice == "left":
                return "down"
            elif move_choice == "right":
                return "up"
            elif move_choice == "up":
                return "left"
            elif move_choice == "down":
                return "right"

        elif orientation == 180:
            return self.opposite(move_choice)

        elif orientation == 270:

            if move_choice == "left":
                return "up"
            elif move_choice == "right":
                return "down"
            elif move_choice == "up":
                return "right"
            elif move_choice == "down":
                return "left"
        elif orientation == 360:
            return move_choice

    def filter_best_path(self, path, end_position, start_position):

        best_path = []
        elements_to_remove = []

        for index, element in enumerate(copy.deepcopy(path)):
            if index == 0:
                continue
            dups = [x[0] for x in list(enumerate(path))[index - 1:] if x[1] == element]
            if len(dups) > 1:
                for x in range(dups[0] + 1,dups[-1] + 1):
                    elements_to_remove.append(x)


        elements_to_remove = list(set(elements_to_remove))
        rects_to_remove = [path[y] for y in elements_to_remove]
        for rect in rects_to_remove:
            path.remove(rect)
        path.remove(end_position)
        path.remove(start_position)
        for x in path:
            pg.draw.circle(self.screen, "purple", (x[0] + self.rect_size // 2, x[1] + self.rect_size // 2),
                           10)
                # [path.remove(x) for x in range(dups[0],dups[-1] + 1)]
