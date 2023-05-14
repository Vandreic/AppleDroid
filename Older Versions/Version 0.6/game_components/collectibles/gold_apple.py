# game_components\collectibles\gold_apple.py

"""
Gold Apple Class

This class represents the gold apple collectible in the game, which is a more valuable version of the regular apple.
It manages the loading of the gold apple image, determining initial positioning, and respawn functionality when 
collected by the player. The gold apple can respawn at a default or random location.
"""


import pygame
from game_components.collectibles.apple import Apple
from config import GOLD_APPLE_IMAGE_PATH, GOLD_APPLE_COLLISION_SOUND_PATH, GOLD_APPLE_SPAWN_SOUND_PATH


class GoldApple(Apple): # Inherit from Apple class

    # Default x- & y-pos
    DEFAULT_X_POS = 700
    DEFAULT_Y_POS = 500

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(GOLD_APPLE_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, super().APPLE_SCLAE_NUM)
        self.rect = self.image.get_rect(center=(self.DEFAULT_X_POS, self.DEFAULT_Y_POS))
        self.type = "gold_apple" # Set apple type
        self.collision_sound = pygame.mixer.Sound(GOLD_APPLE_COLLISION_SOUND_PATH) # Collision sound
        self.spawn_sound = pygame.mixer.Sound(GOLD_APPLE_SPAWN_SOUND_PATH) # Spawn sound (Played when apple spawns)

    # Update function
    def update(self):
        pass