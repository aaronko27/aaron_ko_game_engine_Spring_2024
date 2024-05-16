#This file was created by : aaron Ko
import pygame as pg
from settings import *
from os import path
from random import choice
# Define a vector class for easier vector operations
vec = pg.math.Vector2



def load_level(file_path):
    """Load a level from a text file."""
    with open(file_path, "r") as file:
        return [list(line.strip()) for line in file]

def display_level(level):
    """Display a level."""
    for row in level:
        print("".join(row))

level1 = load_level("map.txt")
level2 = load_level("map2.txt")
level3 = load_level("map3.txt")

SPRITESHEET = "theBell.png"
#dir = path.dirname(__file__)
#img_folder = path.join(dir, 'images')
#class Spritesheet:
    # utility class for loading and parsing spritesheets
    #def __init__(self, filename):
    #    self.spritesheet = pg.image.load(filename).convert()

    #def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        #image = pg.Surface((width, height))
        #image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        #image = pg.transform.scale(image, (width * 4, height * 4))
        #return image
    
#class Animated_sprite(Sprite):
#    def __init__(self):
#        Sprite.__init__(self)
#        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
#        self.load_images()
#        self.image = self.standing_frames[0]
#        self.rect = self.image.get_rect()
#        self.jumping = False
#        self.walking = False
#        self.current_frame = 0
#        self.last_update = 0



# Player class representing the player character
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Initialize the sprite
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN) 
         # Color the player sprite green
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0 
        #self.spritesheet = Spritesheet(path.join(img_folder, 'theBell.png'))
        #self.load_images()
         # Velocity components
        self.x = x * TILESIZE
          # Initial x position
        self.y = y * TILESIZE
          # Initial y position
        self.dir = vec(0,0)
          # Direction vector
        self.moneybag = 0  
        # Counter for coins collected
        self.speed = 300  
        # Player movement speed
        self.font = pg.font.Font(None, 36) 
         # Font for displaying messages
        self.message = None  
        # Message to be displayed
        self.hitpoints = 100  
        # Player health
        self.weapon_drawn = False 
         # Flag to indicate if weapon is drawn


    def teleport(self):
        # Generate random coordinates for teleportation
        new_x = choice(range(WIDTH))
        new_y = choice(range(HEIGHT))
        
        # Check if the new position is valid (not colliding with walls)
        while pg.sprite.spritecollideany(self, self.game.walls):
            new_x = choice(range(WIDTH))
            new_y = choice(range(HEIGHT))

        # Teleport the player to the new position
        self.rect.x = new_x
        self.rect.y = new_y
    #display function that allows you to display messages
    def display_message(self, message):
        self.message = self.font.render(message, True, WHITE)
    def set_dir(self, d):
        self.dir = d
        # return (0,0)
    def get_dir(self):
        return self.dir
    #Get keys function allows you to move your character using the wasd keys or the up down left right keys.
    def get_keys(self):
        self.vx, self.vy = 0, 0
        #know what the key you pressed was so that you can update what happens when you press a certain key
        keys = pg.key.get_pressed()
        #left or A key allow you to move left
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_m]:
            with open("map3.txt", "w") as file:
                file.write("Hello, world!")
                
        #right or D key allow you to move right
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed 
        #Up or W key allow you to move up
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        #keys Down and s allow you to move down
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        #gun key is e and you shoot up
        if keys[pg.K_e]:
            print("trying to shoot...")
            #calls the pew function
            self.pew()

        if keys[pg.K_u]:
            # Toggle mobs on/off
            self.game.toggle_mobs()

        if keys[pg.K_b]:
            #display_level(level3)
            self.game_folder = path.dirname(__file__)
            with open(path.join(self.game_folder, lvl), 'rt') as f:
                    for line in f:
                        print(line)
                        self.map_data.append(line)
    #     # add new map with the same things.
            for row, tiles in enumerate(self.map_data):
                print(row)
                for col, tile in enumerate(tiles):
                    print(col)
                #sets 1 equal to a wall in map2.txt
                    if tile == '1': 
                        print("a wall at", row, col)
                        Wall(self, col, row)
                #sets P equal to player in the map2.txt
                    if tile == 'P':
                        self.player = Player(self, col, row)
                #sets C equal to coins in the map2.txt
                    if tile == 'C':
                        Coin(self, col, row)
                #if tile == 'M':
                #    Mob(self, col, row)
                #sets 3 equal to Poweruos on the map2.txt
                    if tile == '3':
                        PowerUp(self, col, row)
                #sets M equal to the mobs on map2.txt
                    if tile == 'M':
                        Mob(self, col, row)
                #sets H equal to health in map2.txt
                    if tile == 'H':
                        Heal(self, col, row)
                    if tile == 'K':
                        MegaMob(self, col, row)        
            
            
            #make it so that if you click the key f your sword gets drawn if you don't have it drawn
        if keys[pg.K_f]:
            if not self.weapon_drawn:
                #draw a sword if it isn't already drawn
                Sword(self.game, self.rect.x + self.dir[0]*32, self.rect.y + self.dir[1]*32, abs(32*self.dir[0])+5, abs(32*self.dir[1])+5)
                self.weapon_drawn = True
        #make it so that if you click the key g your sword gets taken away
        if keys[pg.K_g]:
            self.weapon_drawn = False


    def pew(self):
        p = PewPew(self.game, self.rect.x, self.rect.y)
        print(p.rect.x)
        print(p.rect.y)

    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
    


    #this function prevents you from running through walls and makes them solid. 
    def collide_with_walls(self, dir):
        #if you collide with walls you get moved back as far as you moved into the wall
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
                self.hitpoints -= 10
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
                self.hitpoints -= 10

    #This function tells you what happens when you collide with a object and allws you to control what happens when they collide
    
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        #if hits is the if statement that shows what happened when you collide with an object
        if hits:
            #If you collide with the coin your moneybag gets added by 1
            if str(hits[0].__class__.__name__) == "Coin":
                #adds 1 coin to the money bag
                self.moneybag += 1
            #If you collide with mob you lose 100 health
            if str(hits[0].__class__.__name__) == "Mob":
                print(hits[0].__class__.__name__)
                #display in terminal that you collided with the mob
                print("collided with mob")
                #subtract 10 health when you collide with the mob
                self.hitpoints -= 10
                #print out your current health 
                print("You have " + str(self.hitpoints) + " Health")
            #if your health is 0 than you die and quit the game
                # if self.hitpoints <= 0:
                #     #when you have less than or equal to 0 health, your game quits
                #     print("You died")
                #     quit()

            if str(hits[0].__class__.__name__) == "MegaMob":
                print(hits[0].__class__.__name__)
                #display in terminal that you collided with the mob
                print("collided with mob")
                #You die when you hit him
                self.hitpoints -= 100
                #print out your current health 
                print("You died")
                quit()


            #If you collect a heal power up then you heal 500 health
            if str(hits[0].__class__.__name__) == "Heal":
                #add 50 to your current health
                self.hitpoints += 100
                #print your current health in terminal
                print("You healed, now you have " + str(self.hitpoints) + " Health")
            #Collecting a powerup heals you
            if str(hits[0].__class__.__name__) == "PowerUp":
                #add 50 to your current speed
                self.speed += 50

    #The update function calls the functions to allow you to move by clicking keys
    #prevents you from running through walls and puts the objects on the map
    #Also it lets the code know if you collide with an object whether to delete the object or not.
    def update(self):
        #get_keys function gets called allowing you to constantly move your player and allow actions to happen
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        #adds collision with all groups 
        #if your collide with groups ends with True then your player deletes the object once you collide with it.
        #if your collide with group ends with False then your player can't delete the object
        #delete object
        self.collide_with_group(self.game.coins, True)
        #delete object
        self.collide_with_group(self.game.power_ups, True)
        #keep object
        self.collide_with_group(self.game.mobs, False)
        #delete object
        self.collide_with_group(self.game.mega_mobs, False)

        self.collide_with_group(self.game.heal, True)
        #Coins message
        #if self.moneybag == 7:
        #    self.display_message("Congratulations! You collected 7 coins!")
          
        #coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        #if coin_hits:
         #   print("I got a coin")
    #Edited stuff
        #display screen
    def draw_message(self):
        if self.message:
            #display your message 
            self.game.screen.blit(self.message, (350, 350))
    
    
    
#sword class  
class Sword(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites, game.weapons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h))
        #make the sword the color light blue
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        #get the shape of your sword
        self.rect.w = w
        self.rect.h = h
        #get coordinates of your sword
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        #print you created a sword in the terminal
        print("I created a sword")
    #function that affects what happens when you collide with a mob 
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        #if hits function
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                #print your hurt a mob in terminal
                print("you hurt a mob!")
                #subtract 50 health from a mob
                hits[0].hitpoints -= 50
    #updates sword constantly
    def update(self):
        # self.collide_with_group(self.game.coins, True)
        # if self.game.player.dir
        self.rect.x = self.game.player.rect.x + self.game.player.dir[0]*32
        self.rect.y = self.game.player.rect.y + self.game.player.dir[1]*32
        #get the image of the sword
        self.rect.width = abs(self.game.player.get_dir()[0]*32)+5
        self.rect.width = abs(self.game.player.get_dir()[1]*32)+5
        #get the image of the sword
        self.image.get_rect()
        #doesn't delete the mob 
        self.collide_with_group(self.game.mobs, False)
        if not self.game.player.weapon_drawn:
            #remove the sword when your sword isn't drawn
            self.kill()
#Wall class that displays the walls
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #sets the wall to a certain color
        self.image.fill(WALLCOLOR)
        #creates the box shape for the walls 
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#Coin class that shows the code for coins
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #Sets the coins to a certain color and shape
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #make the coin yellow
        self.image.fill(YELLOW)
        #set the coin to a certain shape
        self.rect = self.image.get_rect()
        #get the coordinates of the coin
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
#Heal Class 
class Heal(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.heal
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #sets the heal potion to a certain color and shape
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #set coin to the color blue
        self.image.fill(BLUE)
        #set coin to the shape rectangle
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
#Class for powerup that makes it look a certain wayh
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #Self.image creates the image and shape of powerup
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #set the color of the image to white
        self.image.fill(WHITE)
        #make the shape of it a rectangle
        self.rect = self.image.get_rect()
        #get the coordinates of the game 
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class PewPew(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.dir = self.game.player.dir
        print("I created a pew pew...")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        # if hits:
        #     if str(hits[0].__class__.__name__) == "Coin":
        #         self.moneybag += 1
    def update(self):
        self.collide_with_group(self.game.mobs, True)
        self.rect.x += self.dir[0]*self.speed
        self.rect.y += self.dir[1]*self.speed



#Creates the mob
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #Creates the mob image
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #color the mob red
        self.image.fill(RED)
        #set the shape of the mob
        self.rect = self.image.get_rect()
        #get the coordinates of the mob
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        #get the speed of the mob
        self.speed = 300
        #health of the mob
        self.hitpoints = 100
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.can_move = True
    #collides with walls function that prevents mobs from running through walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            #doesn't delete walls when you collide with it
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                #move the opposite direction when you collide with a wall
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    #updates what happens when you collide with a mob
    def update(self):
        #kill the mob when the mob has less than 1 health
        if self.hitpoints < 1:
            self.kill()
        self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        if self.can_move:
            if self.rect.x < self.game.player.rect.x:
                self.vx = 100
            if self.rect.x > self.game.player.rect.x:
                self.vx = -100    
            if self.rect.y < self.game.player.rect.y:
                self.vy = 100
            if self.rect.y > self.game.player.rect.y:
                self.vy = -100
            self.rect.x = self.x
            self.collide_with_walls('x')
            self.rect.y = self.y
            self.collide_with_walls('y')
        

class MegaMob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #Creates the mob image
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #color the mob red
        self.image.fill(PURPLE)
        #set the shape of the mob
        self.rect = self.image.get_rect()
        #get the coordinates of the mob
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        #get the speed of the mob
        self.speed = 1000
        #health of the mob
        self.hitpoints = 1000
        self.rect.x = x * TILESIZE
        self.can_move = True
        self.rect.y = y * TILESIZE
    #collides with walls function that prevents mobs from running through walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            #doesn't delete walls when you collide with it
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                #move the opposite direction when you collide with a wall
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    #updates what happens when you collide with a mob
    def update(self):
        #kill the mob when the mob has less than 1 health
        if self.hitpoints < 1:
            self.kill()
        self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        if self.can_move:
            if self.rect.x < self.game.player.rect.x:
                self.vx = 100
            if self.rect.x > self.game.player.rect.x:
                self.vx = -100    
            if self.rect.y < self.game.player.rect.y:
                self.vy = 100
            if self.rect.y > self.game.player.rect.y:
                self.vy = -100
            self.rect.x = self.x
            self.collide_with_walls('x')
            self.rect.y = self.y
            self.collide_with_walls('y')