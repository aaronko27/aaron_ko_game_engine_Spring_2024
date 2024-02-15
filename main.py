# This file was created by: Chris Cozort

# import libraries and modules
import pygame as pg
#imports everything in settings.py
from settings import *
# imports everything from sprites.py
from sprites import *
# imports random
from random import randint
# imports sys
import sys
from os import path

# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    # Create run method which runs the whole GAME
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player1 = Player(self, 1, 1)
        self.all_sprites.add(self.player1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)

    def run(self):
        # 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            #defines quit method
    def quit(self):
         pg.quit()
         sys.exit()
# defines update
    def update(self):
        self.all_sprites.update()
    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            pg.display.flip()

    def events(self):
         #quits game if you lose.w
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     #move the character left
            #     if event.key == pg.K_a:
            #         self.player1.move(dx=-1)
            #     #move the character right
            #     if event.key == pg.K_d:
            #         self.player1.move(dx=1)
            #     #move the character downds
            #     if event.key == pg.K_s:
            #         self.player1.move(dy=1)
            #     #move the character up
            #     if event.key == pg.K_w:
            #         self.player1.move(dy=-1)

# Instantiate the game... 
g = Game()
# use game method run to run
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()
