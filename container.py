import pygame as pg

class Container:
    screen = pg.display.set_mode((1800, 900))
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    clock = pg.time.Clock()
    fps = 60