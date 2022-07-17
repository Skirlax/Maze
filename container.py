import pygame as pg


class Container:
    screen = pg.display.set_mode((1800, 900))

    screen_width = screen.get_width()
    screen_height = screen.get_height()
    rect_size = 100
    rects_in_row = screen_width // rect_size
    rects_in_column = screen_height // rect_size
    clock = pg.time.Clock()
    fps = 75
