import time
import pygame as pg

FPS = 30

frames = ["Frame 1", "Frame 2", "Frame 3", "Frame 4"]
clock = pg.time.Clock()

last_update = 0


def animate():
    global last_update
    now = pg.time.get_ticks()
    if now - last_update > 350:
        print(now)
        last_update = now
    

while True:
    clock.tick(FPS)
    animate()
