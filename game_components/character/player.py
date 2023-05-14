# game_components/character/player.py

"""
Player Class

This class represents the player character in the game, managing the loading of the player's image,
determining initial positioning, movement based on keyboard input, and respawn functionality when required.
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_IMAGE_PATH, PLAYER_MOVE_SPEED_X, PLAYER_MOVE_SPEED_Y


class Player(pygame.sprite.Sprite):

    # Player scaling factor (Picture is too big, so scale it down)
    PLAYER_SCALE_NUM = 0.28

    # Default x- & y-pos
    DEFAULT_X_POS = SCREEN_WIDTH / 2
    DEFAULT_Y_POS = SCREEN_HEIGHT / 2

    # Constructor: Initialize the object
    def __init__(self):
        super().__init__() # Call the parent class (Sprite) constructor
        self.image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha() # Load player.png with transparency (Used for pygame performance)
        self.image = pygame.transform.rotozoom(self.image, 0, self.PLAYER_SCALE_NUM) # Apply scaling to player
        self.rect = self.image.get_rect(center=(self.DEFAULT_X_POS, self.DEFAULT_Y_POS)) # Set initial player position
  
    def keyboard_input(self):
        """Handles keyboard input: Sets player velocity based on keyboard input"""
        self.vx, self.vy = 0, 0 # Player velocity
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        # UP ARROW
        if keys[pygame.K_UP] and self.rect.top >= 1:
            self.vy = -PLAYER_MOVE_SPEED_Y
        # DOWN ARROW
        if keys[pygame.K_DOWN] and self.rect.bottom <= SCREEN_HEIGHT:
            self.vy = PLAYER_MOVE_SPEED_Y

        # LEFT ARROW
        if keys[pygame.K_LEFT] and self.rect.left >= -35:
            self.vx = -PLAYER_MOVE_SPEED_X
        # RIGHT ARROW
        if keys[pygame.K_RIGHT] and self.rect.right <= SCREEN_WIDTH + 35:
            self.vx = PLAYER_MOVE_SPEED_X
        
        # Normalize diagonal movement to maintain the same speed in all directions
        if self.vx != 0 and self.vy != 0: # If player is moving diagonally
            self.vx *= 0.7071 # Reduce player x-velocity by 0.7071 (1/sqrt(2)) or /= 1.4142
            self.vy *= 0.7071 # Reduce player y-velocity by 0.7071 (1/sqrt(2)) or /= 1.4142
        
    def move(self):
        """Moves player based on velocity"""
        self.rect.x += self.vx # Update player x-pos
        self.rect.y += self.vy # Update player y-pos
        
    def update(self):
        """Call keyboard_input to respond to player action
        Note: 'update' is a built-in method in pygame's Sprite class. It's called once per frame
        """
        self.keyboard_input() # Keyboard input
        self.move() # Move player
        
    def respawn(self):
        """Handles respawn: Spawns player to default location"""
        # Move player to default x- & y-pos
        self.rect.center = (self.DEFAULT_X_POS, self.DEFAULT_Y_POS)

    # Return player boundaries (Used to restrict apple-spawn)
    def get_player_boundaries(self):
        """Return player boundaries: Used to restrict apple-spawn

        Returns:
            values_dict (dict): Dictionary with player boundaries
        """
        # Create dictionary with the player boundaries
        values_dict = {"x_pos": self.rect.centerx, "y_pos": self.rect.centery, "width": self.rect.width, "height": self.rect.height}
        return values_dict