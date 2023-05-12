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
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_RATE, GAME_TITLE, COUNTDOWN_DEFAULT_START_TIMER_VALUE, APPLE_TIME_BONUS, GOLD_APPLE_TIME_BONUS, GOLD_APPLE_CHECK_INTERVAL, GOLD_APPLE_SPAWN_CHANCE
from game_components.ui import GameScreen
from game_components.character import Player
from game_components.collectibles import Apple, GoldApple


class Game():

    def __init__(self):
        pygame.init() # Initialize pygame

        # Create the screen surface and set the window caption
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        # Create a clock object to control the frame rate
        self.clock = pygame.time.Clock()

        # Get current time since game start
        self.game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Convert to seconds with one decimal

        # Set default start value for countdown timer
        self.countdown_start_timer_value = COUNTDOWN_DEFAULT_START_TIMER_VALUE

        # Initialize gold apple timer with game start time
        self.gold_apple_last_check_time = self.game_start_time # Same value as game_start_time

        # Create spawn flag for gold apple
        self.gold_apple_spawned = False

        # Create highscore counter
        self.highscore_num = 0

        # Handle game screens
        self.game_screen = GameScreen(screen)

        # Player setup
        self.player = Player() # Create player
        self.player_group = pygame.sprite.GroupSingle() # Create SingleGroup (Used to store single sprite)
        self.player_group.add(self.player) # Add player to player group
        
        # Apple(s) setup
        self.apple = Apple() # Create apple (object)
        self.gold_apple = GoldApple() # Create gold apple (object)
        self.apple_group = pygame.sprite.Group() # Create group (Used to store multiple sprites)
        self.apple_group.add(self.apple) # Add apple object to group

        # Send sprites groups to game screen
        self.game_screen.retrieve_sprites(player_group=self.player_group, sprite_group=self.apple_group)

        # Show start screen
        self.game_screen.screen_manager("start_screen")

    # Update function (Game loop = Needed run constantly)
    def update(self):
        
        self.game_screen.update_frame() # Update screen frame
        self.player_group.update()      # Update player
        self.apple_group.update()       # Update apple

        # Check if main screen is active
        if self.game_screen.active_game_screen == "main_screen":

            # Countdown timer
            current_time = round(pygame.time.get_ticks() / 1000, 1) # Get current time
            elapsed_time = round(current_time - self.game_start_time, 1) # Calculate elapsed time since game start
            self.countdown_timer_value = round(self.countdown_start_timer_value - elapsed_time, 1) # Start countdown timer

            # Gold apple spawn timer
            gold_apple_time_passed = round(current_time - self.gold_apple_last_check_time, 1) # Calculate time passed since last check for gold apple spawn

            # Send updated values of highscore and countdown timer to game screen
            self.game_screen.update_text(text_to_update="highscore", new_text_value=self.highscore_num) # Highscore
            self.game_screen.update_text(text_to_update="countdown_timer", new_text_value=self.countdown_timer_value) # Countdown timer

            # Get position and text size from texts (Used for apple-spawn restrictions)
            highscore_boundaries = self.game_screen.cache_text_info(return_text_info="highscore") # Cache position and text size for highscore
            countdown_timer_boundaries = self.game_screen.cache_text_info(return_text_info="countdown_timer") # Cache position and text size for countdown timer
            # Get player boundaries (Used for apple-spawn restrictions)
            player_boundaries = self.player.get_player_boundaries()
            # Create dictionary to store apple-spawn restrictions
            self.spawn_restrictions = {"highscore": highscore_boundaries, "countdown_timer": countdown_timer_boundaries, "player": player_boundaries}
            # Send spawn restrictions to apple(s) classes
            self.apple.update_spawn_restrictions(self.spawn_restrictions)
            self.gold_apple.update_spawn_restrictions(self.spawn_restrictions)

            # Check if countdown timer reaches 0
            if self.countdown_timer_value <= 0:
                self.game_screen.screen_manager("end_screen") # Change to end screen
                self.countdown_start_timer_value = COUNTDOWN_DEFAULT_START_TIMER_VALUE # Reset countdown timer to default value
                self.highscore_num = 0 # Reset highscore
                self.player.respawn() # Respawn player to default position
                self.apple.respawn(default_spawn_location=True) # Respawn apple to default position
                self.gold_apple.respawn() # Respawn gold apple to random position

            # Perform gold apple spawn/despawn check
            if gold_apple_time_passed >= GOLD_APPLE_CHECK_INTERVAL:
                self.gold_apple_last_check_time = current_time # Update last check time for gold apple spawn/despawn
            
                # Gold apple spawn
                if self.gold_apple_spawned == False and random.random() < (GOLD_APPLE_SPAWN_CHANCE/100): # Check if gold apple should spawn based on spawn chance
                    self.apple_group.add(self.gold_apple) # Spawn gold apple
                    self.gold_apple.respawn() # Spawn to random location
                    self.gold_apple_spawned = True # Update the gold apple spawn flag

                # Gold apple despawn
                elif self.gold_apple_spawned == True:
                    self.apple_group.remove(self.gold_apple) # Despawn gold apple
                    self.gold_apple_spawned = False # Update the gold apple spawn flag

            # Store collisions inside a list
            collision_list = pygame.sprite.spritecollide(self.player_group.sprite, self.apple_group, False)
            # Check for stored collision
            if collision_list != None:
                for apple in collision_list: # Check which apple was collided with

                    # Collision with regular apple
                    if apple.type == "apple":
                        self.apple.respawn() # Respawn regular apple
                        self.highscore_num += 1 # Increase highscore
                        self.countdown_start_timer_value += APPLE_TIME_BONUS # Increase countdown timer
                    
                    # Collision with gold apple
                    if apple.type == "gold_apple":
                        self.apple_group.remove(self.gold_apple) # Remove gold apple
                        self.gold_apple_spawned = False # Update the gold apple spawn flag
                        self.highscore_num += 1 # Increase highscore
                        self.countdown_start_timer_value += GOLD_APPLE_TIME_BONUS # Increase countdown timer (2x default value)

        # If main screen is not active
        else:
            self.game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Reset current time since game start
            self.countdown_timer_value = 0 # Reset countdown timer value
            self.player.respawn() # Respawn player to default position
            self.apple_group.remove(self.gold_apple) # Remove gold apple
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