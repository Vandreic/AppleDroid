# game_components/ui/game_screen.py

"""
Game Screen Class

This class manages the game's user interface, handling the rendering and updating of various game screens,
including the start-, main-, and end-screen. It displays game elements such as score, timer, and sprites
(player and collectibles) and manages user input for navigating between screens.
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FONT_PATH, PLAYER_IMAGE_PATH

class GameScreen():

    # Create a background surface
    background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def __init__(self, screen):
        self.screen = screen # Store game screen 

    # Start screen
    def start_screen(self):
        # Fill screen with grey color
        self.background_surface.fill(pygame.color.Color("gray70"))
        # Draw background
        self.screen.blit(self.background_surface, (0, 0)) 
            
        # Draw game title
        start_screen_game_title = create_text(text=GAME_TITLE, font_size=70, x_pos=2, y_pos=4, screen=self.screen)
        # Draw game creator
        start_screen_game_creator = create_text(text="Created by Victor", font_size=30, x_pos=2, y_pos=2.8, screen=self.screen)
        # Draw info text
        start_screen_info = create_text(text="Press \"SPACE\" to play...", font_size=44, x_pos=2, y_pos=1.3, screen=self.screen)

    # Main screen
    def main_screen(self):
        # Fill screen with grey color
        self.background_surface.fill(pygame.color.Color("gray60"))
        #  Draw background
        self.screen.blit(self.background_surface, (0, 0)) 
        
        # Draw highscore text and store text size
        self.highscore_display = create_text(text=f"Score: {self.highscore_num}", font_size=40, x_pos=2, y_pos=15, screen=self.screen, return_text_info=True) # Draw highscore text
        self.cache_text_info(get_text_info=self.highscore_display) # Cache highscore text position and size
        # Draw countdown timer text and store text size
        self.countdown_timer_display = create_text(text=f"Timer: {self.countdown_timer_value}", font_size=25, x_pos=2, y_pos=7.7, screen=self.screen, return_text_info=True) # Draw countdown timer text
        self.cache_text_info(get_text_info=self.countdown_timer_display) # Cache countdown timer text position and size
        
        # Draw player
        self.player_group.draw(self.screen)
        # Draw apple
        self.sprite_group.draw(self.screen) 
    
    # End screen
    def end_screen(self):
        # Fill screen with green color
        self.background_surface.fill(pygame.color.Color("gray70")) 
        # Draw background
        self.screen.blit(self.background_surface, (0, 0))
        # Draw highscore
        end_screen_highscore_display = create_text(text=f"Score: {self.highscore_num}", font_size=70, x_pos=2, y_pos=4.3, screen=self.screen)
        # Draw info text
        end_screen_info = create_text(text="Press \"SPACE\" to play again...", font_size=44, x_pos=2, y_pos=1.25, screen=self.screen)

        # Load and draw player image (Image used for display)
        end_screen_player_surf = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha() # Load player.png with transparency (Used for pygame performance)
        end_screen_player_surf = pygame.transform.rotozoom(end_screen_player_surf, 0, 2) # Apply scaling to player image
        end_screen_player_rect = end_screen_player_surf.get_rect(center=((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))) # Set player image position
        self.screen.blit(end_screen_player_surf, end_screen_player_rect) # Draw player image to screen

    # Screen manager (Switch between screens)
    def screen_manager(self, active_screen="start_screen"):
        self.active_game_screen = active_screen

        # Change to start screen
        if self.active_game_screen == "start_screen":
            self.start_screen()
        # Change to main screen
        elif self.active_game_screen == "main_screen":
            self.main_screen()
        # Change to end screen
        elif self.active_game_screen == "end_screen":
            self.end_screen()
    
    # Update function: Check for keyboard input
    def key_input(self, key_is_pressed=False):
        self.key_is_pressed = key_is_pressed # Flag for key press
        # If key pressed
        if self.key_is_pressed == True:
            
            # Start screen --> Main screen
            if self.active_game_screen == "start_screen":
                self.screen_manager("main_screen")

            # End screen --> Main screen
            elif self.active_game_screen == "end_screen":
                self.screen_manager("main_screen")
    
    # Render sprites (Get sprites to draw)
    def render_sprites(self, player_group="", sprite_group=""):
        self.player_group = player_group
        self.sprite_group = sprite_group

    # Get highscore value
    def render_highscore(self, highscore_num=0):
        self.highscore_num = highscore_num

    # Get countdown timer text
    def render_countdown_timer(self, countdown_timer_value=""):
        self.countdown_timer_value = countdown_timer_value
    
    # Cache the position and size of text elements for later use and return values (Used for highscore and countdown timer)
    def cache_text_info(self, get_text_info=None, return_text_info=""):
        # Cache text position and size
        if get_text_info == self.highscore_display: # Highscore text
            self.highscore_text_info = get_text_info
        elif get_text_info == self.countdown_timer_display: # Countdown timer text
            self.countdown_timer_text_info = get_text_info
            
        # Return cached text position and size
        if return_text_info == "highscore": # Highscore text
            return self.highscore_text_info
        elif return_text_info == "countdown_timer": # Countdown timer text
            return self.countdown_timer_text_info
            
    # Update frame (Needed to be updated constantly)
    def update_frame(self):
        
        # Main screen: if active, update frame
        if self.active_game_screen == "main_screen":
            self.main_screen()

# Function for drawing text on screen
def create_text(text="", font_size=10, x_pos=0, y_pos=0, screen="", return_text_info=False):
    """
    Auguments:

    text               Set text
    font_size          Set font size (Default: 10)
    x_pos              X-position for text (Center-based positioning)
    y_pos              Y-position for text (Center-based positioning)
    screen             Set screen to draw text on
    return_text_info   Return text position and size (Default: False)
    """

    text_font = pygame.font.Font(FONT_PATH, font_size) # Set font and size
    text_display = text_font.render(text, True, pygame.color.Color("White")) # Draw text
    text_display_rect = text_display.get_rect(center=((SCREEN_WIDTH / x_pos, SCREEN_HEIGHT / y_pos))) # Position text

    screen.blit(text_display, text_display_rect) # Draw text to screen

    # If return_text_info is True, return text position and size
    if return_text_info == True:
        # Create dictionary with text position and size
        values_dict = {"x_pos": text_display_rect.centerx, "y_pos": text_display_rect.centery, "width": text_display_rect.width, "height": text_display_rect.height}
        return values_dict # Return dictionary
    