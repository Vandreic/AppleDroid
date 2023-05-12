# game_components\collectibles\gold_apple.py

"""
Gold Apple Class

This class represents the gold apple collectible in the game, which is a more valuable version of the regular apple.
It manages the loading of the gold apple image, determining initial positioning, and respawn functionality when 
collected by the player. The gold apple can respawn at a default or random location.
"""


import pygame
from game_components.collectibles.apple import Apple
from config import GOLD_APPLE_IMAGE_PATH


class GoldApple(Apple): # Inherit from Apple class

    # Default x- & y-pos
    x_default_pos = 700
    y_default_pos = 550

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(GOLD_APPLE_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, super().apple_scale_num)
        self.rect = self.image.get_rect(center=(self.x_default_pos, self.y_default_pos))
        self.type = "gold_apple" # Set apple type

    # Update function
    def update(self):
        pass