# game_components/collectibles/apple.py

"""
Apple Class

This class represents the apple collectible in the game, handling the loading of the apple image,
determining initial positioning, and respawn functionality when collected by the player. 
The apple can respawn at a default or random location.
"""

import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, APPLE_IMAGE_PATH

class Apple(pygame.sprite.Sprite):

    # Default x- & y-pos
    x_default_pos = 200
    y_default_pos = 200

    # Apple scale factor
    apple_scale_num = 0.5

    def __init__(self):
        super().__init__()
        self.image = apple_surf = pygame.image.load(APPLE_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, self.apple_scale_num)
        self.rect = self.image.get_rect(center=(self.x_default_pos, self.y_default_pos))

    # Respawn apple to new location
    def respawn(self, avoid_spawn_coordinates=None, default_spawn_location=False):

        # Check if default spawn location in enabled
        if default_spawn_location == True:
            self.rect.center = (self.x_default_pos, self.y_default_pos) # Spawn to default position
        # Spawn to random position
        else:
            
            coordinate_list = avoid_spawn_coordinates # Store spawn avoidance coordinates (dictionary)

            spawn_margin = 4 # Minimum spawn distance from screen edge (in pixels)

            # Set minimum spawn distance from screen edge
            x_min_pos = int(self.image.get_width() / 2) + spawn_margin
            x_max_pos = int(SCREEN_WIDTH - self.image.get_width() / 2) - spawn_margin

            y_min_pos = int(self.image.get_height() / 2) + spawn_margin
            y_max_pos = int(SCREEN_HEIGHT - self.image.get_height() / 2) - spawn_margin

            # Create random spawn coordinates
            x_pos = random.randint(x_min_pos, x_max_pos)
            y_pos = random.randint(y_min_pos, y_max_pos)

            # Check if spawn coordinates are within the spawn avoidance coordinates
            while True: # Loop until valid spawn coordinates are found
                valid_spawn = False # Spawn validity flag

                player_spawn_margin = 60 # Minimum spawn distance from player (in pixels)

                # Create spawn avoidance coordinates ranges (Creates a rectangle area around texts and player)
                # Highscore text
                x_start_highscore = int(coordinate_list["highscore"]["x_pos"] - coordinate_list["highscore"]["width"] / 2) - int(self.image.get_width() / 2) - spawn_margin
                x_end_highscore = int(coordinate_list["highscore"]["x_pos"] + coordinate_list["highscore"]["width"] / 2) + int(self.image.get_width() / 2) + spawn_margin
                y_start_highscore = spawn_margin # Calculated value equals -1, so set to value of spawn_margin instead
                y_end_highscore = int(coordinate_list["highscore"]["y_pos"] + coordinate_list["highscore"]["height"] / 2) + int(self.image.get_height() / 2) + spawn_margin

                # Countdown text
                x_start_countdown = int(coordinate_list["countdown_timer"]["x_pos"] - coordinate_list["countdown_timer"]["width"] / 2) - int(self.image.get_width() / 2) - spawn_margin
                x_end_countdown = int(coordinate_list["countdown_timer"]["x_pos"] + coordinate_list["countdown_timer"]["width"] / 2) + int(self.image.get_width() / 2) + spawn_margin
                y_start_countdown = int(coordinate_list["countdown_timer"]["y_pos"] - coordinate_list["countdown_timer"]["height"] / 2) - int(self.image.get_height() / 2) - spawn_margin
                y_end_countdown = int(coordinate_list["countdown_timer"]["y_pos"] + coordinate_list["countdown_timer"]["height"] / 2) + int(self.image.get_height() / 2) + spawn_margin

                # Player
                x_start_player = int(coordinate_list["player"]["x_pos"] - coordinate_list["player"]["width"] / 2) - int(self.image.get_width() / 2) - player_spawn_margin
                x_end_player = int(coordinate_list["player"]["x_pos"] + coordinate_list["player"]["width"] / 2) + int(self.image.get_width() / 2) + player_spawn_margin
                y_start_player = int(coordinate_list["player"]["y_pos"] - coordinate_list["player"]["height"] / 2) - int(self.image.get_height() / 2) - player_spawn_margin
                y_end_player = int(coordinate_list["player"]["y_pos"] + coordinate_list["player"]["height"] / 2) + int(self.image.get_height() / 2) + player_spawn_margin

                # Check player coordinates ranges: Make sure values does not exceed screen boundaries
                if x_start_player < 0: 
                    x_start_player = 0 + int(self.image.get_width() / 2) + player_spawn_margin + spawn_margin
                if x_end_player > SCREEN_WIDTH:
                    x_end_player = SCREEN_WIDTH - int(self.image.get_width() / 2) - player_spawn_margin - spawn_margin
                if y_start_player < 0:
                    y_start_player = 0 + int(self.image.get_height() / 2) + player_spawn_margin + spawn_margin
                if y_end_player > SCREEN_HEIGHT:
                    y_end_player = SCREEN_HEIGHT - int(self.image.get_height() / 2) - player_spawn_margin - spawn_margin

                # Check if spawn coordinates are within the spawn avoidance coordinates
                valid_spawn = False # Create spawn validity flag
                # Check for highscore and countdown text
                if (x_pos in range(x_start_highscore, x_end_highscore) or y_pos in range(y_start_highscore, y_end_highscore)) or (x_pos in range(x_start_countdown, x_end_countdown) or y_pos in range(y_start_countdown, y_end_countdown)):
                    # Create new random spawn coordinates
                    x_pos = random.randint(x_min_pos, x_max_pos)
                    y_pos = random.randint(y_min_pos, y_max_pos)
                
                # Check for player
                elif (x_pos in range(x_start_player, x_end_player) or y_pos in range(y_start_player, y_end_player)):
                    # Create new random spawn coordinates
                    x_pos = random.randint(x_min_pos, x_max_pos)
                    y_pos = random.randint(y_min_pos, y_max_pos)

                # Valid spawn coordinates
                else:
                    valid_spawn = True # Set spawn validity flag
                
                # Check if spawn is valid
                if valid_spawn == True:
                    valid_spawn = False # Reset spawn validity flag
                    break # Exit loop

            # Move apple to new x- & y-pos
            self.rect.center = (x_pos, y_pos)

    # Update function
    def update(self):
        pass