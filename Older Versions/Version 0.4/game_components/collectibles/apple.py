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
    def respawn(self, default_spawn_location=False):

        # Check if default spawn location in enabled
        if default_spawn_location == True:
            self.rect.center = (self.x_default_pos, self.y_default_pos) # Spawn to default position
        # Spawn to random position
        else:
            spawn_margin = 4 # Minimum spawn distance from screen edge (in pixels)

            # Set minimum spawn distance from screen edge
            x_min_pos = int(self.image.get_width()/2) + spawn_margin
            x_max_pos = int(SCREEN_WIDTH - self.image.get_width()/2) - spawn_margin

            y_min_pos = int(self.image.get_height()/2) + spawn_margin
            y_max_pos = int(SCREEN_HEIGHT - self.image.get_height()/2) - spawn_margin

            # Create random x- & y-pos
            x_pos = random.randint(x_min_pos, x_max_pos)
            y_pos = random.randint(y_min_pos, y_max_pos)

            # Move apple to new x- & y-pos
            self.rect.center = (x_pos, y_pos)

    # Update function
    def update(self):
        pass