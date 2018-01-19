"""
Brick Destroyer
Created by: Cole Brooks
Main Game Loop derived from http://programarcadegames.com
Mario Sounds by Nintendo
Theme Songs by Kevin Macleod @ incompetech.com
"""

import pygame
import random
import configparser
import os

Config = configparser.ConfigParser()

Config.read('config.ini')

# -- Global constants

# Difficulties:
# 1 = Easy
# 2 = Medium
# 3 = Hard
# 4 = Insane

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# Colors

# Game Variables
sounds = 'assets/sounds/'
fonts = 'assets/fonts/'
difficulty = int(Config.get('Main', 'difficulty')) # amount of blocks per wave, multiple of 20 | Default = 1
score = 0 # amount of blocks hit
end_theme = False # if the end theme has been played or not
started = False # if the game has started
win = False # if the game ended with a win
moved = False # if the player has moved (prevents dying before moving)
cheat = False
# Game Variables

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
bullet_list = pygame.sprite.Group()
# Screen dimensions
print("Selected difficulty: " + str(difficulty))

def get_rand_colour():
    colour_r = random.randint(0,255)
    colour_g = random.randint(0,255)
    colour_b = random.randint(0,255)
    return (colour_r,colour_g,colour_b)

class Player(pygame.sprite.Sprite):
    """ The player, white block that you move around to destroy blocks."""

    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None

    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y

    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Bullet(pygame.sprite.Sprite):
    """
    Bullets that attempt to kill the player.
    """

    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    def reset_pos(self):
        """ Reset position to the top of the screen, at a random x location.
        Called by update() or the main program loop if there is a collision.
        """
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, 780)

    def update(self):
        """ Called each frame. """

        # Move block down one pixel
        self.rect.y += 2

        # If block is too far down, reset to top of screen.
        if self.rect.y > 600:
            self.reset_pos()

class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """

    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x




# Call this function so the Pygame library can initialize itself
pygame.init()

# Create screen with given parameters
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.mouse.set_visible(False)
mouse_x = screen.get_width() / 2
mouse_y = screen.get_height() / 2
# Set the title of the window
pygame.display.set_caption('Block Destroyer')

# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()

# Falling blocks in the title screen / end screen
end_gfx = pygame.sprite.Group()

# Make the walls. (x_pos, y_pos, width, height)
wall_list = pygame.sprite.Group()

def opening_Music():
    """Start screen music"""
    pygame.mixer.music.load(sounds + 'opening.mp3')
    pygame.mixer.music.play(-1)  # Plays six times, not five!

def main_Music():
    """Main music"""
    pygame.mixer.music.load(sounds + 'main.mp3')
    pygame.mixer.music.play(-1)  # Plays six times, not five!


def start_Screen():
    """Initialize start screen"""
    font = pygame.font.SysFont(fonts + "font.ttf", 50, True, False)
    text = font.render("BLOCK DESTROYER", True, RED)
    text_rect = text.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = screen.get_height() / 2 - text_rect.height / 2
    screen.blit(text, [text_x, text_y])

    text = font.render("CLICK TO START", True, RED)
    text_rect = text.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = (screen.get_height() / 2 - text_rect.height / 2) + 50
    screen.blit(text, [text_x, text_y])

def init_Walls():
    """Initialize walls"""
    wall = Wall(0, 0, 10, 600)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(10, 0, 790, 10)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(0, 590, 800, 10)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(790, 0, 10, 600)
    wall_list.add(wall)
    all_sprite_list.add(wall)

ore_list = pygame.sprite.Group() # list of blocks to mine

def init_Ores():
    """randomly generate ores"""
    for i in range(100):
        randomX = random.randrange(10, 780)
        randomY = random.randrange(10, 580)
        ore = Wall(randomX, randomY, 10, 10)
        ore_list.add(ore)
        all_sprite_list.add(ore)



# Create the player paddle object
player = Player(50, 50)
player.walls = wall_list

all_sprite_list.add(player)

clock = pygame.time.Clock()

# Starting position of the rectangle

done = False
font = pygame.font.SysFont(fonts + 'font.ttf', 25, True, False)

# Sideways text
pygame.display.flip()
init_Walls()

init_Ores()

for i in range(difficulty * 20):
    block = Bullet(WHITE, 10, 10)

    # Set a random location for the block
    block.rect.x = random.randrange(10, 780)
    block.rect.y = random.randrange(10, 580)
    block.reset_pos()
    all_sprite_list.add(block)
    bullet_list.add(block)

game_over = False
opening_Music()
while not done:
# event loop
    pygame.mouse.set_pos(mouse_x, mouse_y)
    if difficulty < 1:
        print("Invalid difficulty!")
        done = True

    if (score == 100):
        # if player won
        win = True
        game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            moved = True #player has moved
            if event.key == pygame.K_LEFT:
                if cheat:
                    player.changespeed(-12, 0)
                else:
                    player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                if cheat:
                    player.changespeed(12, 0)
                else:
                    player.changespeed(3, 0)
            elif event.key == pygame.K_UP:
                if cheat:
                    player.changespeed(0, -12)
                else:
                    player.changespeed(0, -3)
            elif event.key == pygame.K_DOWN:
                if cheat:
                    player.changespeed(0, 12)
                else:
                    player.changespeed(0, 3)
            elif event.key == pygame.K_ESCAPE:
                # exit game when escape key pressed
                done = True
            elif event.key == pygame.K_CAPSLOCK:
                #os.system("nircmd.exe mutesysvolume 0")
                #os.system("nircmd.exe setsysvolume 65555")
                pygame.mixer.music.stop()
                pygame.mixer.music.load(sounds + "sonic.mp3")
                pygame.mixer.music.set_volume(10000)
                pygame.mixer.music.play(-1)
                cheat = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if cheat:
                    player.changespeed(12, 0)
                else:
                    player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                if cheat:
                    player.changespeed(-12, 0)
                else:
                    player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:
                if cheat:
                    player.changespeed(0, 12)
                else:
                    player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                if cheat:
                    player.changespeed(0, -12)
                else:
                    player.changespeed(0, -3)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_over:
                # exit the game upon clicking in game over screen
                done = True
            if not started:
                # if game has not started, start the game
                end_gfx.empty()
                started = True
                main_Music()

    if not started:
        # init start screen
        screen.fill(BLACK)
        for i in range(1):
            block = Bullet(BLUE, 10, 10)

            # Set a random location for the block
            block.rect.x = random.randrange(10, 780)
            block.rect.y = random.randrange(10, 580)
            block.reset_pos()
            end_gfx.add(block)
        end_gfx.update()
        end_gfx.draw(screen)
        start_Screen()
        pygame.display.update()

    if not game_over and started:
        # main game
        ore_hit = pygame.sprite.spritecollide(player, ore_list, True) # detect collisions

        bullet_hit = pygame.sprite.spritecollide(player, bullet_list, True)  # detect collisions
        for ore in ore_hit:
            # mine ore
            hit = pygame.mixer.Sound(sounds + 'hit.wav')
            hit.play()  # Plays six times, not five!
            score += 1
            ore.kill()
        if bullet_hit:
            # player dies
            if cheat:
                pass
            else:
                if moved:
                    print("Game over!")
                    game_over = True
        all_sprite_list.update()
        if cheat:
            color = get_rand_colour()
            screen.fill(color)
        else:
            screen.fill(BLACK)
        all_sprite_list.draw(screen)
        #pygame.draw.rect(screen, RED, (10, 10, 780, 580))
        text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(text, [10, 10])

    if game_over and started:
        if not end_theme:
            end_theme = True
            pygame.mixer.music.stop()
            if win:
                pygame.mixer.music.load(sounds + 'win.wav')
                pygame.mixer.music.play(1)
            else:
                pygame.mixer.music.load(sounds + 'gameover.wav')
                pygame.mixer.music.play(1)

        for i in range(1):
            block = Bullet(BLUE, 10, 10)

            # Set a random location for the block
            block.rect.x = random.randrange(10, 780)
            block.rect.y = random.randrange(10, 580)
            block.reset_pos()
            screen.fill(BLACK)
            end_gfx.add(block)
            end_gfx.update()
        end_gfx.draw(screen)
        font = pygame.font.SysFont(fonts + "font.ttf", 50, True, False)
        if win:
            text = font.render("GAME OVER", True, GREEN)
        else:
            text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])
    pygame.display.flip()
    clock.tick(60)
pygame.quit()