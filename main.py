#This file was created by Aaron Ko\

# import libraries and modules
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path
'''
gun
enemies
moving enemies
coins 
player death
player health
heal potion
different levels
map change
'''
#Creating different maps for different levels.
LEVEL1 = "map.txt"
LEVEL2 = "map2.txt"

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
        self.game_folder = path.dirname(__file__)
        #self.img_folder = path.join(self.game_folder, 'images')
        #self.snd_folder = path.join(self.game_folder, 'sounds')
        self.map_data = []
        #opening LEVEL1 variable or map.txt as file for map
        with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
    #Change level function
    def change_level(self, lvl):
         # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
         # reset criteria for changing level
        self.player.moneybag = 0
         # reset map data list to empty
        self.map_data = []
         # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    #     # add new map with the same things.
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1': 
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                #if tile == 'M':
                #    Mob(self, col, row)
                if tile == '3':
                    PowerUp(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'H':
                   Heal(self, col, row)

    # Create run method which runs the whole GAME
    def new(self):
        print("create new game...")
        #running all objects inside the game and all functions.
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.heal = pg.sprite.Group()
        self.weapons = pg.sprite.Group()
        #fsself.mobs = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                #adding all objects to game from the maps
                if tile == '1': 
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                #if tile == 'M':
                #    Mob(self, col, row)
                if tile == '3':
                    PowerUp(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'H':
                    Heal(self, col, row)


    def run(self):
        # runs the entire game and runs the functions draw update and events while using the clock
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
         pg.quit()
         sys.exit()
    #updating game as time goes on
    def update(self):
        self.all_sprites.update()
        #checking to see if the moneybag is 7 and when all coins are collected change map and level
        if self.player.moneybag > 6:
            self.change_level(LEVEL2)
    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw_text(self, surface, text, size, color, x, y):
        #setting the draw text to a certain color font size and font name
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)
        #draw function that draws the whole screen and displays your moneybag.
    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)

            pg.display.flip()

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            #if event.key == pg.K_e:
            #        self.player.weapon_drawn = False
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
    #create a start screen that requires user to click to send you to main game.
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
    #the function that waits for the user to press any key
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
# Instantiate the game... 
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()