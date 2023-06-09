# game_components/ui/game_screen.py

"""
Game Screen Class

This class manages the game's user interface, handling the rendering and updating of various game screens,
including the start-, main-, and end-screen. It displays game elements such as score, timer, and sprites
(player and apples) and manages user input for navigating between screens.
"""


import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FONT_PATH, PLAYER_IMAGE_PATH

class GameScreen():

    # Create a background surface
    background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def __init__(self, screen):
        """Initialize Game Screen
        
        Parameters:
            screen (pygame.Surface):    Game screen
        """
        self.screen = screen # Store game screen
        self.selected_btn = 0 # Store selected button (Default: 0)
        self.key_input_update_delay = 0.1  # Set update delay for key input (in seconds) 

        # Store variables values from Main Screen
        self.highscore = 0 # Highscore
        self.countdown_timer = 0 # Countdown timer

        self.clock = pygame.time.Clock()  # Initialize a Clock object
        self.game_start_time = pygame.time.get_ticks()  # Get current time since game / screen start

       # Start screen
    def start_screen(self):
        """Create and draw start screen"""

        # Fill screen with grey color
        self.background_surface.fill(pygame.color.Color("gray70"))
        # Draw background
        self.screen.blit(self.background_surface, (0, 0)) 
            
        # Draw texts
        game_title = self.draw_text(text=GAME_TITLE[:10], font_size=94, x_pos=50, y_pos=11) # Game title
        game_creator = self.draw_text(text="Created by Victor", font_size=25, x_pos=50, y_pos=22) # Game creator
        game_controls_info = self.draw_text(text="Use arrow keys to navigate. Press \"SPACE\" to enter", font_size=25, x_pos=50, y_pos=86) # Controls text
        game_version = self.draw_text(text=GAME_TITLE[-4:], font_size=20, x_pos=96, y_pos=97) # Game version
        
        # Draw buttons (Just text functioning as buttons)
        btn_play = self.draw_text(text="Play", font_size=40, x_pos=50, y_pos=39) # Play
        btn_controls = self.draw_text(text="Controls", font_size=40, x_pos=50, y_pos=50) # Controls
        btn_about = self.draw_text(text="About", font_size=40, x_pos=50, y_pos=61) # About
        btn_quit = self.draw_text(text="Quit", font_size=40, x_pos=50, y_pos=72) # Quit

        # Update selected button and check if space key is pressed
        key_input = self.update_selected_btn(active_screen="start_screen", total_btns=3) # Total buttons: 0, 1, 2, 3...

        # Highlight selected button and manage key input
        # Play
        if self.selected_btn == 0:
            self.draw_text_highlight(text_info=btn_play)
            if key_input == True:
                self.screen_manager("main_screen")

        # Controls [W.I.P]
        if self.selected_btn == 1:
            self.draw_text_highlight(text_info=btn_controls)
            if key_input == True:
                #self.screen_manager("")
                pass # To be implemented..
        
        # About [W.I.P]
        if self.selected_btn == 2:
            self.draw_text_highlight(text_info=btn_about)
            if key_input == True:
                #self.screen_manager("")
                pass # To be implemented..
        
        # Quit
        if self.selected_btn == 3:
            self.draw_text_highlight(text_info=btn_quit)
            if key_input == True:
                pygame.quit()
                sys.exit()

    # Main screen
    def main_screen(self):
        """Create and draw main screen"""

        # Fill screen with grey color
        self.background_surface.fill(pygame.color.Color("gray60"))
        #  Draw background
        self.screen.blit(self.background_surface, (0, 0)) 

        # Draw highscore text and store text size
        self.highscore_text = self.draw_text(text=f"Score: {self.highscore}", font_size=40, x_pos=50, y_pos=6, return_text_info=True) # Draw highscore text
        self.cache_text_info(get_text_info=self.highscore_text) # Cache highscore text position and size
        # Draw countdown timer text and store text size
        self.countdown_timer_text = self.draw_text(text=f"Timer: {self.countdown_timer}", font_size=25, x_pos=50, y_pos=11.5, return_text_info=True) # Draw countdown timer text
        self.cache_text_info(get_text_info=self.countdown_timer_text) # Cache countdown timer text position and size
        
        # Draw player
        self.player_group.draw(self.screen)
        # Draw apple
        self.sprite_group.draw(self.screen) 
    
    # End screen
    def end_screen(self):
        """Create and draw end screen"""

        # Fill screen with green color
        self.background_surface.fill(pygame.color.Color("gray70")) 
        # Draw background
        self.screen.blit(self.background_surface, (0, 0))
        # Draw highscore
        highscore = self.draw_text(text=f"Score: {self.highscore}", font_size=70, x_pos=50, y_pos=8)

        # Load and draw player image (Image used for display)
        end_screen_player_surf = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha() # Load player.png with transparency (Used for pygame performance)
        end_screen_player_surf = pygame.transform.rotozoom(end_screen_player_surf, 0, 3) # Apply scaling to player image
        end_screen_player_rect = end_screen_player_surf.get_rect(center=((SCREEN_WIDTH * (50 / 100), SCREEN_HEIGHT * (50 / 100)))) # Set player image position
        self.screen.blit(end_screen_player_surf, end_screen_player_rect) # Draw player image to screen

        # Draw buttons (Just text functioning as buttons)
        btn_restart = self.draw_text(text="Restart", font_size=40, x_pos=50, y_pos=39) # Restart
        btn_main_menu = self.draw_text(text="Main Menu", font_size=40, x_pos=50, y_pos=50) # Main menu
        btn_quit = self.draw_text(text="Quit", font_size=40, x_pos=50, y_pos=61) # Quit

        # Update selected button and check if space key is pressed
        key_input = self.update_selected_btn(active_screen="end_screen", total_btns=2)

        # Highlight selected button and manage key input
        # Restart
        if self.selected_btn == 0:
            self.draw_text_highlight(text_info=btn_restart)
            if key_input == True:
                self.screen_manager("main_screen")

        # Main Menu / Start screen
        if self.selected_btn == 1:
            self.draw_text_highlight(text_info=btn_main_menu)
            if key_input == True:
                self.screen_manager("start_screen")
        
        # Quit
        if self.selected_btn == 2:
            self.draw_text_highlight(text_info=btn_quit)
            if key_input == True:
                pygame.quit()
                sys.exit()

    # Screen manager
    def screen_manager(self, active_screen="start_screen"):
        """Manages the game screens by switching between them

        Parameters:
            active_screen (str): Screen to switch to (Default: Start screen)
        Returns:
            None
        """
        self.active_game_screen = active_screen # Get active screen

        # Change to start screen
        if self.active_game_screen == "start_screen":
            self.start_screen()
            self.selected_btn = 0 # Reset selected button
        # Change to main screen
        elif self.active_game_screen == "main_screen":
            self.main_screen()
        # Change to end screen
        elif self.active_game_screen == "end_screen":
            self.end_screen()
            self.selected_btn = 0 # Reset selected button

    def update_frame(self):
        """Update frames on active screen
        Used to constantly update graphics on active screen
        Note: This function needs to be updated constantly
        """
        # Update frame of active screen
        if self.active_game_screen == "start_screen": # Start screen
            self.start_screen()
        elif self.active_game_screen == "main_screen": # Main screen
            self.main_screen()
        elif self.active_game_screen == "end_screen": # End screen
            self.end_screen()
    
    def keyboard_input(self):
        """Get keyboard input

        Returns:
            If arrow keys or space key is pressed, return key input (str)

        """
        current_time = pygame.time.get_ticks()  # Get the current time

        # Check for key input after a delay
        if current_time - self.game_start_time > self.key_input_update_delay*1000:
            self.game_start_time = current_time  # Update game start time
            keys = pygame.key.get_pressed()  # Get key input

            if keys[pygame.K_UP]: # Up arrow
                return "up_arrow"
            elif keys[pygame.K_DOWN]: # Down arrow
                return "down_arrow"
            elif keys[pygame.K_SPACE]: # Space
                return "space"

    # Create and draw text
    def draw_text(self, text="", font_size=10, color="White", x_pos=0, y_pos=0, return_text_info=False):
        """Create and draw text on screen

        Parameters:
            text (str):                 Text to be displayed
            font_size (int):            Font size (Default: 10)
            color (str):                Text color (Default: White) (See: https://www.pygame.org/docs/ref/color_list.html)
            x_pos (float):              X-coordinate for the text position (percentage of screen width) (default is 0)
            y_pos (float):              Y-coordinate for the text position (percentage of screen height) (default is 0)
            return_text_info (bool):    Flag to determine if text information should be returned (default is False)
        Returns:
            If return_text_info is True, a dictionary with text position and size
                Otherwise, a dictionary with text font, text string, and text rectangle object
        """

        text_font = pygame.font.Font(FONT_PATH, font_size) # Set font and size
        text_surface = text_font.render(str(text), True, pygame.color.Color(color)).convert_alpha() # Render text surface
        text_rect = text_surface.get_rect(center=((SCREEN_WIDTH * (x_pos / 100), SCREEN_HEIGHT * (y_pos / 100)))) # Position text
        self.screen.blit(text_surface, text_rect) # Draw text on screen

        # If return_text_info is True, return text position and size
        if return_text_info == True:
            # Create dictionary with text position and size
            values_dict = {"x_pos": text_rect.centerx, "y_pos": text_rect.centery, "width": text_rect.width, "height": text_rect.height}
            return values_dict # Return dictionary
        else:
            # Create dictionary with text surface and rect
            values_dict = {"text_font": text_font, "text": str(text), "text_rect": text_rect}
            return values_dict # Return dictionary

    def draw_text_highlight(self, text_info=None, highlight_color="Purple"):
        """Highlight selected text

        Parameters:
            text_info (dict):           Dictionary with text font, text string, and text rectangle object of text to highlight)
            highlight_color (str):      Text highlight color (Default: Purple) (See: https://www.pygame.org/docs/ref/color_list.html)
        Returns:
            None
        """

        text_font = text_info["text_font"] # Get text size and font
        text_surface = text_font.render(text_info["text"], True, pygame.color.Color(highlight_color)).convert_alpha() # Render highlighted text surface (Changes text color)
        self.screen.blit(text_surface, text_info["text_rect"]) # Draw highlighted text on screen

    def update_text(self, text_to_update=None, new_text_value=None):
        """Update text on the screen
        This function is used to update dynamic text elements (e.g., score, timer)

        Parameters:
            text_to_update (str):   Text to update
        Returns:
            None
        """
        # Check which text to update
        if text_to_update == "highscore": # Update highscore text
            self.highscore = new_text_value
        elif text_to_update == "countdown_timer": # Update countdown timer text
            self.countdown_timer = new_text_value

    def cache_text_info(self, get_text_info=None, return_text_info=""):
        """Cache position and size of text element for later use and return values 
        (Used for highscore and countdown timer)
        
        Parameters:
            get_text_info (dict):      Dictionary with text position and size to cache
            return_text_info (str):    Text to return
        Returns:
            A dictionary with the cached information (dict)
        """
        # Cache text position and size
        if get_text_info == self.highscore_text: # Highscore text
            self.highscore_text_info = get_text_info
        elif get_text_info == self.countdown_timer_text: # Countdown timer text
            self.countdown_timer_text_info = get_text_info
            
        # Return cached text position and size
        if return_text_info == "highscore": # Highscore text
            return self.highscore_text_info
        elif return_text_info == "countdown_timer": # Countdown timer text
            return self.countdown_timer_text_info
          
    def update_selected_btn(self, active_screen="", total_btns=0):
        """Updates value of selected button based on key input
        Creates a loop for the selected button, so it can go from the last button to the first button and vice versa

        Parameters:
            active_screen (str): Screen to update selected button on
            total_btns (int): Total number of buttons on the screen
        Returns:
            If space key is pressed, return True (bool)
        """
        # Update selected button (Loop)
        if active_screen == "start_screen":
            if self.selected_btn < 0:
                self.selected_btn = total_btns
            elif self.selected_btn > total_btns:
                self.selected_btn = 0
        elif active_screen == "end_screen":
            if self.selected_btn < 0:
                self.selected_btn = total_btns
            elif self.selected_btn > total_btns:
                self.selected_btn = 0

        key_input = self.keyboard_input() # Get key input     

        # Update selected button based on key input
        if key_input == "up_arrow":
            self.selected_btn -= 1
        elif key_input == "down_arrow":
            self.selected_btn += 1
        elif key_input == "space":
            return True
    
    def retrieve_sprites(self, player_group="", sprite_group=""):
        """Retrieve sprite groups for drawing

        Parameters:
            player_group (pygame.sprite.Group): Group containing player sprite
            sprite_group (pygame.sprite.Group): Group containing other game sprites (e.g., apples)
        Returns:
            None
        """
        self.player_group = player_group
        self.sprite_group = sprite_group
            
            