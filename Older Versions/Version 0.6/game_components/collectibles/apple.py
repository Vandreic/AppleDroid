# game_components/collectibles/apple.py

"""
Apple Class

This class represents the apple collectible in the game, handling the loading of the apple image,
determining initial positioning, and respawn functionality when collected by the player. 
The apple can respawn at a default or random location.
"""

import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, APPLE_IMAGE_PATH, PURPLE_APPLE_COLLISION_SOUND_PATH

class Apple(pygame.sprite.Sprite):

    # Apple scale factor (Picture is too big, so scale it down)
    APPLE_SCLAE_NUM = 0.1

    # Default x- & y-pos
    DEFAULT_X_POS = 200
    DEFAULT_Y_POS = 200

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(APPLE_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, self.APPLE_SCLAE_NUM) # Resize apple image
        self.rect = self.image.get_rect(center=(self.DEFAULT_X_POS, self.DEFAULT_Y_POS))
        self.type = "apple" # Set apple type (To differentiate between apples)
        self.collision_sound = pygame.mixer.Sound(PURPLE_APPLE_COLLISION_SOUND_PATH) # Load collision sound
        self.spawn_restrictions = {} # Create spawn restrictions dictionary

    def update_spawn_restrictions(self, get_spawn_restrictions={}):
        """Update spawn restrictions dictionary with cached text information
        Gets text positions and dimensions within a dictionary, which is used to create
        boundaries around text, in order to create spawn restrictions for apple.
        If we do not create spawn restrictions, then apple(s) can spawn on top of texts
         
        Parameters:
            get_spawn_restrictions (dict): Dictionary with cached text position and size
        Returns:
            None
        """
        self.spawn_restrictions = get_spawn_restrictions

    # Respawn apple to new location
    def respawn(self, default_spawn_location=False):
        """Respawn apple to random or default location
        
        Parameters:
            default_spawn_location (bool): Flag to determine if apple should spawn to default location
        Returns:
            None
        """
        # If default_spawn_location is True, move apple to default location (Apple never despawns, only changes position)
        if default_spawn_location == True:
            self.rect.center = (self.DEFAULT_X_POS, self.DEFAULT_Y_POS)
        
        # Else, move apple to random location
        else:

            spawn_margin = 4 # Minimum spawn distance from screen edge (in pixels)

            # Define screen boundaries for spawn (Spawn within screen)
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
                x_start_highscore = int(self.spawn_restrictions["highscore"]["x_pos"] - self.spawn_restrictions["highscore"]["width"] / 2) - int(self.image.get_width() / 2) - spawn_margin
                x_end_highscore = int(self.spawn_restrictions["highscore"]["x_pos"] + self.spawn_restrictions["highscore"]["width"] / 2) + int(self.image.get_width() / 2) + spawn_margin
                y_start_highscore = spawn_margin # Calculated value equals -1, so set to value of spawn_margin instead
                y_end_highscore = int(self.spawn_restrictions["highscore"]["y_pos"] + self.spawn_restrictions["highscore"]["height"] / 2) + int(self.image.get_height() / 2) + spawn_margin

                # Countdown text
                x_start_countdown = int(self.spawn_restrictions["countdown_timer"]["x_pos"] - self.spawn_restrictions["countdown_timer"]["width"] / 2) - int(self.image.get_width() / 2) - spawn_margin
                x_end_countdown = int(self.spawn_restrictions["countdown_timer"]["x_pos"] + self.spawn_restrictions["countdown_timer"]["width"] / 2) + int(self.image.get_width() / 2) + spawn_margin
                y_start_countdown = int(self.spawn_restrictions["countdown_timer"]["y_pos"] - self.spawn_restrictions["countdown_timer"]["height"] / 2) - int(self.image.get_height() / 2) - spawn_margin
                y_end_countdown = int(self.spawn_restrictions["countdown_timer"]["y_pos"] + self.spawn_restrictions["countdown_timer"]["height"] / 2) + int(self.image.get_height() / 2) + spawn_margin

                # Player
                x_start_player = int(self.spawn_restrictions["player"]["x_pos"] - self.spawn_restrictions["player"]["width"] / 2) - int(self.image.get_width() / 2) - player_spawn_margin
                x_end_player = int(self.spawn_restrictions["player"]["x_pos"] + self.spawn_restrictions["player"]["width"] / 2) + int(self.image.get_width() / 2) + player_spawn_margin
                y_start_player = int(self.spawn_restrictions["player"]["y_pos"] - self.spawn_restrictions["player"]["height"] / 2) - int(self.image.get_height() / 2) - player_spawn_margin
                y_end_player = int(self.spawn_restrictions["player"]["y_pos"] + self.spawn_restrictions["player"]["height"] / 2) + int(self.image.get_height() / 2) + player_spawn_margin

                # Check player coordinates ranges: Make sure values does not exceed screen boundaries, as player moves
                if x_start_player < 0: 
                    x_start_player = 0 + int(self.image.get_width() / 2) + player_spawn_margin + spawn_margin
                if x_end_player > SCREEN_WIDTH:
                    x_end_player = SCREEN_WIDTH - int(self.image.get_width() / 2) - player_spawn_margin - spawn_margin
                if y_start_player < 0:
                    y_start_player = 0 + int(self.image.get_height() / 2) + player_spawn_margin + spawn_margin
                if y_end_player > SCREEN_HEIGHT:
                    y_end_player = SCREEN_HEIGHT - int(self.image.get_height() / 2) - player_spawn_margin - spawn_margin

                # Check if spawn coordinates are within the spawn avoidance coordinates. If not, create new random spawn coordinates
                # Check for highscore and countdown text
                if (x_pos in range(x_start_highscore, x_end_highscore) or y_pos in range(y_start_highscore, y_end_highscore)) or (x_pos in range(x_start_countdown, x_end_countdown) or y_pos in range(y_start_countdown, y_end_countdown)):
                    x_pos = random.randint(x_min_pos, x_max_pos)
                    y_pos = random.randint(y_min_pos, y_max_pos)
                
                # Check for player
                elif (x_pos in range(x_start_player, x_end_player) or y_pos in range(y_start_player, y_end_player)):
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