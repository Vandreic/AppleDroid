# game_components/character/player.py

"""
Player Class

This class represents the player character in the game, managing the loading of the player's image,
determining initial positioning, movement based on keyboard input, and respawn functionality when required.
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_IMAGE_PATH, PLAYER_MOVE_SPEED_X, PLAYER_MOVE_SPEED_Y

class Player(pygame.sprite.Sprite):

    # Default x- & y-pos
    x_pos = SCREEN_WIDTH / 2
    y_pos = SCREEN_HEIGHT / 2

    # Player scaling factor
    player_scale_num = 0.7

    # Constructor: Initialize the object
    def __init__(self):
        super().__init__() # Call the parent class (Sprite) constructor
        self.image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha() # Load player.png with transparency (Used for pygame performance)
        self.image = pygame.transform.rotozoom(self.image, 0, self.player_scale_num) # Apply scaling to player
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) # Set initial player position

    # Respawn player 
    def respawn(self):
        # Move player to default x- & y-pos
        self.rect.center = (self.x_pos, self.y_pos)

    # Check keyboard input and update player position
    def keyboard_input(self):
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        # LEFT ARROW
        if keys[pygame.K_LEFT] and self.rect.left >= PLAYER_MOVE_SPEED_X: # If player is inside game boundaries and key is pressed
            self.rect.x -= PLAYER_MOVE_SPEED_X # Move player
        # RIGHT ARROW
        if keys[pygame.K_RIGHT] and self.rect.right <= (SCREEN_WIDTH - PLAYER_MOVE_SPEED_X):
            self.rect.x += PLAYER_MOVE_SPEED_X
        # UP ARROW
        if keys[pygame.K_UP] and self.rect.top >= PLAYER_MOVE_SPEED_Y:
            self.rect.y -= PLAYER_MOVE_SPEED_Y
        # DOWN ARROW
        if keys[pygame.K_DOWN] and self.rect.bottom <= (SCREEN_HEIGHT - PLAYER_MOVE_SPEED_Y):
            self.rect.y += PLAYER_MOVE_SPEED_Y

    # Update function
    def update(self):
        self.keyboard_input() # Keyboard input