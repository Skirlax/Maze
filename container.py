import pygame as pg


class Container:
    # Basic properties of the maze algorithm.
    # Screen size can be set to whatever, as long as: size % rect_size == 0

    screen = pg.display.set_mode((1000, 1000))

    screen_width = screen.get_width()
    screen_height = screen.get_height()
    rect_size = 50
    rects_in_row = screen_width // rect_size
    rects_in_column = screen_height // rect_size
    clock = pg.time.Clock()
    fps = 75
