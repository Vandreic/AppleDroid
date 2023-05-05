# game_components\collectibles\gold_apple.py

"""
Gold Apple Class

This class represents the gold apple collectible in the game, which is a more valuable version of the regular apple.
It manages the loading of the gold apple image, determining initial positioning, and respawn functionality
when collected by the player. The gold apple always respawns at a random location.
"""

import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GOLD_APPLE_IMAGE_PATH

class GoldApple(pygame.sprite.Sprite):

    # Default x- & y-pos
    x_default_pos = 700
    y_default_pos = 550

    # Apple scale factor
    apple_scale_num = 0.5

    def __init__(self):
        super().__init__()
        self.image = apple_surf = pygame.image.load(GOLD_APPLE_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, self.apple_scale_num)
        self.rect = self.image.get_rect(center=(self.x_default_pos, self.y_default_pos))

    # Respawn apple to new location
    def respawn(self):
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