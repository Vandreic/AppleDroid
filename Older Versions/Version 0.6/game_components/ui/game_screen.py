# game_components/ui/game_screen.py

"""
Game Screen Class

This class manages the game's user interface, handling the rendering and updating of various game screens,
including the start-, main-, and end-screen. It displays game elements such as score, timer, and sprites
(player and apples) and manages user input for navigating between screens.

When you create a new screen, you create a function that draws the elements onto it, and handles key input
1) Create function for drawing screen & handle key input
2) Add screen to 'screen_manager' function
3) Add screen to 'update_frame' function (Screen must be drawn constantly)
"""


import pygame
import sys
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FONT_PATH, PLAYER_IMAGE_PATH, MENU_SELECTION_SOUND_PATH
from config import BG_IMAGE_FOLDER_PATH, ARROW_KEYS_IMAGE_PATH, ENTER_KEY_IMAGE_PATH, SPACE_KEY_IMAGE_PATH


class GameScreen():

    def __init__(self, screen):
        """Initialize Game Screen
        
        Parameters:
            screen (pygame.Surface):    Game screen
        """

        self.screen = screen # Store game screen
        self.selected_btn = 0 # Store selected button (Default: 0)
        self.key_input_update_delay = 0.1  # Set update delay for key input (in seconds) 
        self.menu_selection_sound = pygame.mixer.Sound(MENU_SELECTION_SOUND_PATH) # Create menu selection sound

        # Placeholder to store variables values from Main Screen
        self.highscore = 0 # Highscore
        self.countdown_timer = 0 # Countdown timer

        self.clock = pygame.time.Clock()  # Initialize a Clock object
        self.game_start_time = pygame.time.get_ticks()  # Get current time since game / screen start

        # Load default background and transform to fit screen size 
        self.bg_default = pygame.image.load(f"{BG_IMAGE_FOLDER_PATH}/bg_default.png").convert_alpha()
        self.bg_default = pygame.transform.scale(self.bg_default, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Store random backgrounds in a list
        self.bg_images = [] # Used to display random backgrounds on main screen
        
        # Loop through all random backgground and add them to list
        for img in range(0, 6): # 6 total random backgrounds
            bg_img = pygame.image.load(f"{BG_IMAGE_FOLDER_PATH}/bg_{img}.png").convert_alpha()
            bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Transform image to screen size
            self.bg_images.append(bg_img)

        self.random_bg_img = self.set_new_background() # Store random background image
        
    #----------------| SCREENS |----------------#
    def start_screen(self):
        """Create and draw start screen"""

        # Draw default background
        self.draw_default_background()

        # Draw texts
        game_title = self.draw_text(text=GAME_TITLE[:10], font_size=94, x_pos=50, y_pos=14) # Game title
        game_creator = self.draw_text(text="Created by Victor", font_size=25, x_pos=50, y_pos=25) # Game creator
        game_version = self.draw_text(text=GAME_TITLE[-4:], font_size=20, x_pos=96, y_pos=97) # Game version
        
        # Draw buttons (Just text functioning as buttons)
        btn_play = self.draw_text(text="Play", font_size=40, x_pos=50, y_pos=43.5) # Play
        btn_controls = self.draw_text(text="Controls", font_size=40, x_pos=50, y_pos=54.5) # Controls
        btn_about = self.draw_text(text="About", font_size=40, x_pos=50, y_pos=65.5) # About
        btn_quit = self.draw_text(text="Quit", font_size=40, x_pos=50, y_pos=76.5) # Quit

        # Update selected button and check if enter/space key is pressed (Returns True if enter/space key is pressed)
        key_input = self.update_selected_btn(active_screen="start_screen", total_btns=3) # Total buttons: 0, 1, 2, 3...

        # Highlight selected button and manage key input
        # Play
        if self.selected_btn == 0:
            self.draw_text_highlight(text_info=btn_play)
            if key_input == True:
                self.screen_manager("main_screen")

        # Controls
        if self.selected_btn == 1:
            self.draw_text_highlight(text_info=btn_controls)
            if key_input == True:
                self.screen_manager("controls_screen")
        
        # About
        if self.selected_btn == 2:
            self.draw_text_highlight(text_info=btn_about)
            if key_input == True:
                self.screen_manager("about_screen")
        
        # Quit
        if self.selected_btn == 3:
            self.draw_text_highlight(text_info=btn_quit)
            if key_input == True:
                pygame.quit()
                sys.exit()
    
    def controls_screen(self):
        """Create and draw controls screen"""

        # Draw default background
        self.draw_default_background()

        # Draw texts
        title = self.draw_text(text="Game Controls", font_size=94, x_pos=50, y_pos=13) # Title
        movement = self.draw_text(text="Movement:", font_size=50, x_pos=24, y_pos=40) # Movement
        confirm = self.draw_text(text="Confirm:", font_size=50, x_pos=78, y_pos=40) # Confirm
        
        # Load and draw keyboard keys images
        # Arrow keys
        arrow_keys_surf = pygame.image.load(ARROW_KEYS_IMAGE_PATH).convert_alpha()
        arrow_keys_rect = arrow_keys_surf.get_rect(center=((SCREEN_WIDTH * (24 / 100), SCREEN_HEIGHT * (59 / 100))))
        self.screen.blit(arrow_keys_surf, arrow_keys_rect)
        # Enter key
        enter_key_surf = pygame.image.load(ENTER_KEY_IMAGE_PATH).convert_alpha()
        enter_key_rect = enter_key_surf.get_rect(center=((SCREEN_WIDTH * (65 / 100), SCREEN_HEIGHT * (59 / 100))))
        self.screen.blit(enter_key_surf, enter_key_rect)
        # Space key
        space_key_surf = pygame.image.load(SPACE_KEY_IMAGE_PATH).convert_alpha()
        space_key_rect = space_key_surf.get_rect(center=((SCREEN_WIDTH * (84.5 / 100), SCREEN_HEIGHT * (59 / 100))))
        self.screen.blit(space_key_surf, space_key_rect)

        # Draw back button (Just text functioning as button)
        btn_back = self.draw_text(text="Back", font_size=40, x_pos=50, y_pos=92) # Back
        
        # Check if enter/space key is pressed (bool)
        key_input = self.update_selected_btn() # Returns True if enter/space key is pressed
        
        # Reset selected button to 0 (We only have 1 button) & manage key input
        self.selected_btn = 0 
        if self.selected_btn == 0:
            self.draw_text_highlight(text_info=btn_back)
            if key_input == True:
                self.screen_manager("start_screen")
    
    def about_screen(self):
        """Create and draw about screen"""
            
        # Draw default background
        self.draw_default_background()

        # Create a surface (Used to create overlay on screen for better readability)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(pygame.color.Color("grey1"))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        # Draw texts
        title = self.draw_text(text="About", font_size=94, x_pos=50, y_pos=13) # Title

        # Create "about" text and split them up into multiple texts (Used to create spacing between paragraphs)
        text_1 = """
        AppleDroid is a small game where you control an Android with 
        the objective of collecting as many apples as possible. 
        It's the first game I've ever developed and also my first
        project using Pygame and Object-Oriented Programming (OOP).
        """
        text_2 = """
        I've tried to document the code as well as possible,
        but please keep in mind that I'm still learning.. :)
        """
        text_3 = """
        While the game is not perfect and can be improved in many ways,
        the primary aim was to learn Pygame and simple game development.
        """
        text_4 = """
        I'm pleased with the overall result and the progress I've made.
        Thank you for taking the time to play my game and read this!
        """

        about_text = [text_1, text_2, text_3, text_4] # Put all texts in list
        # Draw texts [Pygame does not support multiline text]
        y_pos = 25 # Y position of first text
        for text in about_text: # Loop through the texts
            for line in text.splitlines(): # Split up into lines
                if line.strip() == "": # If empty line, create spacing
                    y_pos += 2 # Add spacing between paragraphs
                    continue # Skip to next line
                self.draw_text(text=line, font_size=20, x_pos=50, y_pos=y_pos) # Draw text
                y_pos += 5 # Add spacing for new line

        # Draw back button (Just text functioning as button)
        btn_back = self.draw_text(text="Back", font_size=40, x_pos=50, y_pos=92)
        
        # Check if enter/space key is pressed (bool)
        key_input = self.update_selected_btn()
        
        # Reset selected button to 0 (We only have 1 button) & manage key input
        self.selected_btn = 0
        if self.selected_btn == 0:
            self.draw_text_highlight(text_info=btn_back)
            if key_input == True:
                self.screen_manager("start_screen")

    def main_screen(self):
        """Create and draw main screen"""

        # Draw random background from stored value in set_bg_img
        self.screen.blit(self.random_bg_img, (0, 0))

        # Draw highscore text and cache text size & position
        self.highscore_text = self.draw_text(text=f"Score: {self.highscore}", font_size=40, x_pos=50, y_pos=6, return_text_info=True) # Draw highscore text
        self.cache_text_info(get_text_info=self.highscore_text) # Cache highscore text position and size (Used for spawn restrictions)
        # Draw countdown timer text and cache text size & position
        self.countdown_timer_text = self.draw_text(text=f"Timer: {self.countdown_timer}", font_size=25, x_pos=50, y_pos=11.5, return_text_info=True) # Draw countdown timer text
        self.cache_text_info(get_text_info=self.countdown_timer_text) # Cache countdown timer text position and size
        
        # Draw player & apple(s)
        self.player_group.draw(self.screen)
        self.sprite_group.draw(self.screen) 
    
    def end_screen(self):
        """Create and draw end screen"""

        # Draw default background
        self.draw_default_background()

        # Draw highscore
        highscore = self.draw_text(text=f"Score: {self.highscore}", font_size=70, x_pos=50, y_pos=8)

        # Load and draw player image (Image used for display)
        end_screen_player_surf = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
        end_screen_player_surf.set_alpha(140)
        end_screen_player_rect = end_screen_player_surf.get_rect(center=((SCREEN_WIDTH * (50 / 100), SCREEN_HEIGHT * (50 / 100))))
        self.screen.blit(end_screen_player_surf, end_screen_player_rect)

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


    #----------------| HELPER FUNCTIONS |----------------#
    def screen_manager(self, active_screen="start_screen"):
        """Manages the game screens by switching between them
        Also resets selected button to 0 when switching screens

        Parameters:
            active_screen (str): Screen to switch to (Default: Start screen)
        Returns:
            None
        """
        self.active_game_screen = active_screen # Get active screen

        # Change to start screen
        if self.active_game_screen == "start_screen":
            self.selected_btn = 0
            self.start_screen()
        # Change to controls screen
        elif self.active_game_screen == "controls_screen":
            self.selected_btn = 0
            self.controls_screen()
        # Change to about screen
        elif self.active_game_screen == "about_screen":
            self.about_screen()
            self.selected_btn = 0
        # Change to main screen
        elif self.active_game_screen == "main_screen":
            self.main_screen()
            self.random_bg_img = self.set_new_background() # Set new random background
        # Change to end screen
        elif self.active_game_screen == "end_screen":
            self.selected_btn = 0
            self.end_screen()

    def update_frame(self):
        """Update frames on active screen
        Used to constantly update graphics on active screen
        Note: This function needs to be updated constantly
        """
        # Update frame of active screen
        if self.active_game_screen == "start_screen": # Start screen
            self.start_screen()
        elif self.active_game_screen == "controls_screen": # Controls screen
            self.controls_screen()
        elif self.active_game_screen == "about_screen": # About screen
            self.about_screen()
        elif self.active_game_screen == "main_screen": # Main screen
            self.main_screen()
        elif self.active_game_screen == "end_screen": # End screen
            self.end_screen()
    
    def draw_default_background(self):
        """Draw default background on screen"""
        self.screen.blit(self.bg_default, (0, 0))

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

        text_font = pygame.font.Font(FONT_PATH, font_size)
        text_surface = text_font.render(str(text), True, pygame.color.Color(color)).convert_alpha()
        text_rect = text_surface.get_rect(center=((SCREEN_WIDTH * (x_pos / 100), SCREEN_HEIGHT * (y_pos / 100))))
        self.screen.blit(text_surface, text_rect)

        # If return_text_info is True, return text position and size
        if return_text_info == True:
            # Create dictionary with text position and size, and return it
            values_dict = {"x_pos": text_rect.centerx, "y_pos": text_rect.centery, "width": text_rect.width, "height": text_rect.height}
            return values_dict
        else:
            # Create dictionary with text surface and rect, and return it
            values_dict = {"text_font": text_font, "text": str(text), "text_rect": text_rect}
            return values_dict

    def draw_text_highlight(self, text_info=None, highlight_color="purple3"):
        """Highlight selected text
        Takes a given text and changes its color to create a highlight effect, and draws it to screen

        Parameters:
            text_info (dict):           Dictionary with text font, text string, and text rectangle object of text to highlight)
            highlight_color (str):      Text highlight color (Default: purple3) (See: https://www.pygame.org/docs/ref/color_list.html)
        Returns:
            None
        """
        text_font = text_info["text_font"] # Get text font
        text_surface = text_font.render(text_info["text"], True, pygame.color.Color(highlight_color)).convert_alpha() # Highlight text (Changes text color)
        
        self.screen.blit(text_surface, text_info["text_rect"]) # Draw highlighted text on screen

    def update_text(self, text_to_update=None, new_text_value=None):
        """Update dynamic texts on screen
        This function is used to update dynamic text elements (Highscore & Countdown timer)
        Takes the new text value from main screen, and stores it in a variable, which is then used to update the text

        Parameters:
            text_to_update (str):   Text to update
        Returns:
            None
        """
        # Store new text value in variable
        if text_to_update == "highscore": # Update highscore text
            self.highscore = new_text_value
        elif text_to_update == "countdown_timer": # Update countdown timer text
            self.countdown_timer = new_text_value

    def cache_text_info(self, get_text_info=None, return_text_info=""):
        """Cache position and size of text 
        Gets text position and size in dictionary (Size is not constant as text changes). 
        Returns dictionary with cached information to main screen
        The cached information is used to create boudariens around text, which is used for spawn restrictions 
        
        Needed for highscore and countdown timer
        
        Parameters:
            get_text_info (dict):      Dictionary with text position and size to cache
            return_text_info (str):    Which dictionary with cached information to return
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

    def keyboard_input(self):
        """Get keyboard input

        Returns:
            If arrow keys or enter/space key is pressed, return key input (str)

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
            elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]: # Enter & Space key
                return "enter"

    def update_selected_btn(self, active_screen="", total_btns=0):
        """Updates value of selected button based on key input & plays menu selection sound
        Creates a loop for the selected button, so it can go from the last button to the first button and vice versa

        Parameters:
            active_screen (str):    Screen to update selected button on
            total_btns (int):       Total number of buttons on the screen
        Returns:
            If space key is pressed, return True (bool)
        """
        # Create loop for selected button
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

        # Update selected button based on key input & play menu selection sound
        if key_input == "up_arrow":
            self.menu_selection_sound.play()
            self.selected_btn -= 1
        elif key_input == "down_arrow":
            self.menu_selection_sound.play()
            self.selected_btn += 1
        elif key_input == "enter":
            return True
        
    def set_new_background(self):
        """Change background image
        
        Returns:
            A random background image (pygame.image)
        """
        return random.choice(self.bg_images)
        
    def retrieve_sprites(self, player_group="", sprite_group=""):
        """Retrieve sprite groups for drawing
        Retrieves sprite groups from main screen, so they can be drawn on the screen

        Parameters:
            player_group (pygame.sprite.Group): Group containing player sprite
            sprite_group (pygame.sprite.Group): Group containing other game sprites (e.g., apples)
        Returns:
            None
        """
        self.player_group = player_group
        self.sprite_group = sprite_group
