# game_components/core/game_logic.py

"""
Game Logic Class

This class handles the core game logic, managing the main game loop and event handling.
It initializes and updates game components like the game screen, player, apples, and gold apples,
manages the countdown timer, highscore, and gold apple spawn/despawn logic, and processes user input.
"""

import pygame
import random
import sys
# Game settings
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_RATE, GAME_TITLE, COUNTDOWN_DEFAULT_START_TIMER_VALUE, APPLE_TIME_BONUS, GOLD_APPLE_TIME_BONUS, GOLD_APPLE_CHECK_INTERVAL, GOLD_APPLE_SPAWN_CHANCE
# Sound paths + Game icon image path
from config import PURPLE_APPLE_COLLISION_SOUND_PATH, GOLD_APPLE_COLLISION_SOUND_PATH, GOLD_APPLE_SPAWN_SOUND_PATH, GAME_ICON_IMAGE_PATH
from game_components.ui import GameScreen
from game_components.character import Player
from game_components.collectibles import Apple, GoldApple


class Game():

    def __init__(self):
        """Initialize game components and variables"""
        pygame.init() # Initialize pygame

        # Create the screen surface and set the window dimensions
        pygame.display.set_caption(GAME_TITLE) # Set window caption
        pygame.display.set_icon(pygame.image.load(GAME_ICON_IMAGE_PATH)) # Set window icon
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        
        # Create a clock object to control the frame rate
        self.clock = pygame.time.Clock()

        # Get current time since game start
        self.game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Convert to seconds with one decimal

        # Set default start value for countdown timer
        self.countdown_start_timer_value = COUNTDOWN_DEFAULT_START_TIMER_VALUE

        # Initialize gold apple spawn timer (Used to check if gold apple should spawn/despawn)
        self.gold_apple_spawn_start_time = self.game_start_time # Same value as game_start_time

        # Create gold apple spawn flag (Used to check whether gold apple should spawn/despawn)
        self.gold_apple_spawned = False

        # Create highscore counter
        self.highscore_num = 0

        # Create game screen object: Used to manage game screens
        self.game_screen = GameScreen(screen) # Needs a screen surface as argument

        # Player setup
        self.player = Player() # Create player
        self.player_group = pygame.sprite.GroupSingle() # Create SingleGroup (Used to store single sprite)
        self.player_group.add(self.player) # Add player to group
        
        # Apple(s) setup
        self.apple = Apple() # Create apple
        self.gold_apple = GoldApple() # Create gold apple
        self.apple_group = pygame.sprite.Group() # Create sprite group (Used to store multiple sprites)
        self.apple_group.add(self.apple) # Add apple to group

        # Send sprites groups to game screen (Used to draw sprites)
        self.game_screen.retrieve_sprites(player_group=self.player_group, sprite_group=self.apple_group)

        # Use 'screen_manager' to change screens
        self.game_screen.screen_manager("start_screen") # Change to start screen (Default screen) 

    # Update function (Game loop = Needs to run constantly)
    def update(self):
        """Run the game loop"""
        
        self.game_screen.update_frame() # Update screen frame on active screen (Used to draw sprites and text)
        self.player_group.update()      # Update player (Updates player)
        self.apple_group.update()       # Update apple(s) (Updates all sprites within group, e.g., apple(s))

        # Check if main screen is active
        if self.game_screen.active_game_screen == "main_screen":

            # Countdown timer: Tracks the remaining time before the game ends
            current_time = round(pygame.time.get_ticks() / 1000, 1) # Get current time
            elapsed_time = round(current_time - self.game_start_time, 1) # Calculate elapsed time since game start
            self.countdown_timer_value = round(self.countdown_start_timer_value - elapsed_time, 1) # Start countdown timer from default value

            # Calculate time passed since last check for gold apple spawn
            gold_apple_spawn_time_passed = round(current_time - self.gold_apple_spawn_start_time, 1) 

            # Send updated text values to game screen
            self.game_screen.update_text(text_to_update="highscore", new_text_value=self.highscore_num) # Highscore
            self.game_screen.update_text(text_to_update="countdown_timer", new_text_value=self.countdown_timer_value) # Countdown timer

            # Cache position and size of texts in game_screen class (Used to create bouandaries arond texts)
            highscore_boundaries = self.game_screen.cache_text_info(return_text_info="highscore") # Cache highscore
            countdown_timer_boundaries = self.game_screen.cache_text_info(return_text_info="countdown_timer") # Cache countdown timer
            # Get player boundaries (Used to create boundaries around player)
            player_boundaries = self.player.get_player_boundaries()
            # Create dictionary to store values (Used to create apple-spawn restrictions)
            self.spawn_restrictions = {"highscore": highscore_boundaries, "countdown_timer": countdown_timer_boundaries, "player": player_boundaries}
            # Send spawn restrictions to apple(s) classes
            self.apple.update_spawn_restrictions(self.spawn_restrictions) # Send to apple class
            self.gold_apple.update_spawn_restrictions(self.spawn_restrictions) # Send to gold apple class

            # If countdown timer reaches 0, end game
            if self.countdown_timer_value <= 0:
                self.game_screen.screen_manager("end_screen") # Change to end screen
                self.countdown_start_timer_value = COUNTDOWN_DEFAULT_START_TIMER_VALUE # Reset countdown timer to default value
                self.highscore_num = 0 # Reset highscore
                self.player.respawn() # Respawn player to default position
                self.apple.respawn(default_spawn_location=True) # Respawn apple to default position
                self.gold_apple.respawn() # Respawn gold apple to random position

            # Perform gold apple spawn/despawn check
            if gold_apple_spawn_time_passed >= GOLD_APPLE_CHECK_INTERVAL: # Add check interval to gold apple spawn timer
                self.gold_apple_spawn_start_time = current_time # Update last check time for gold apple spawn/despawn to current time
            
                # Spawn gold apple
                if self.gold_apple_spawned == False and random.random() < (GOLD_APPLE_SPAWN_CHANCE/100): # Check if gold apple should spawn based on spawn chance
                    self.gold_apple.spawn_sound.play() # Play spawn sound
                    self.apple_group.add(self.gold_apple) # Spawn gold apple
                    self.gold_apple.respawn() # Spawn to random location
                    self.gold_apple_spawned = True # Update the gold apple spawn flag

                # Despawn gold apple
                elif self.gold_apple_spawned == True: # Check if gold apple is spawned
                    self.apple_group.remove(self.gold_apple) # Despawn gold apple
                    self.gold_apple_spawned = False # Update the gold apple spawn flag

            # Store collisions between player and apple(s) in list
            collision_list = pygame.sprite.spritecollide(self.player_group.sprite, self.apple_group, False) # Returns list of collided sprites
            if collision_list != None: # If there is a collision
                for apple in collision_list: # Check which apple was collided with

                    # Collision with regular apple
                    if apple.type == "apple":
                        self.apple.collision_sound.play() # Play collision sound
                        self.apple.respawn() # Respawn regular apple
                        self.highscore_num += 1 # Increase highscore
                        self.countdown_start_timer_value += APPLE_TIME_BONUS # Increase countdown timer by bonus value
                    
                    # Collision with gold apple
                    if apple.type == "gold_apple":
                        self.gold_apple.collision_sound.play() # Play collision sound
                        self.apple_group.remove(self.gold_apple) # Despawn gold apple
                        self.gold_apple_spawned = False # Update the gold apple spawn flag
                        self.highscore_num += 1 # Increase highscore
                        self.countdown_start_timer_value += GOLD_APPLE_TIME_BONUS # Increase countdown timer by bonus value

        # If main screen is not active
        else:
            self.game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Reset current time since game start
            self.countdown_timer_value = 0 # Reset countdown timer value
            self.player.respawn() # Respawn player to default position
            self.apple_group.remove(self.gold_apple) # Despawn gold apple
            self.gold_apple_spawned = False # Update the gold apple spawn flag
        
        # Handle events
        for event in pygame.event.get():
            # If the user clicks the 'X' button, exit the game
            if event.type == pygame.QUIT:
                pygame.quit() # Quit pygame
                sys.exit() # Exit script


        # Update the display to show the new frame
        pygame.display.flip()

        # Control the frame rate
        self.clock.tick(FRAME_RATE)