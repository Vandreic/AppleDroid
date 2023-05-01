"""
AppleDroid v0.2

A small python game where you control an Android with the objective of collecting as many apples as possible.


TO-DO:
- BUG: Fix apple spawn so it do not spawn inside highscore & countdown text
- BUG: Fix player & apple spawn after game restart (Create new x- & y-pos for new spawn)

- Update code:
-- Add collision
--- Increase highscore

--- Update calculations for positioning (Use multiplication instead of division?)
--- Create spawn function for apple

"""


# Import modules
from typing import Any
import pygame
import sys
import random



# Player class
class Player(pygame.sprite.Sprite):

    # Player movement speed
    player_move_speed_x = 4
    player_move_speed_y = 4

    # Constructor: Initialize the object
    def __init__(self):
        super().__init__() # Call the parent class (Sprite) constructor
        self.image = pygame.image.load("assets\\player.png").convert_alpha() # Load player.png with transparency (Used for pygame performance)
        player_scale_num = 0.7 # Player scaling factor
        self.image = pygame.transform.rotozoom(self.image, 0, player_scale_num) # Apply scaling to player
        self.rect = self.image.get_rect(center=(100, 100)) # Set initial player position
    

    # Check keyboard input and update player position
    def keyboard_input(self):
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        # LEFT ARROW
        if keys[pygame.K_LEFT] and self.rect.left >= self.player_move_speed_x: # If player is inside game boundaries and key is pressed
            self.rect.x -= self.player_move_speed_x # Move player
        # RIGHT ARROW
        if keys[pygame.K_RIGHT] and self.rect.right <= (screen_width - self.player_move_speed_x):
            self.rect.x += self.player_move_speed_x
        # UP ARROW
        if keys[pygame.K_UP] and self.rect.top >= self.player_move_speed_y:
            self.rect.y -= self.player_move_speed_y
        # DOWN ARROW
        if keys[pygame.K_DOWN] and self.rect.bottom <= (screen_height - self.player_move_speed_y):
            self.rect.y += self.player_move_speed_y

    # Update function
    def update(self):
        self.keyboard_input() # Keyboard input
    

# Apple class
class Apple(pygame.sprite.Sprite):
    def __init__(self,):
        super().__init__()
        self.image = apple_surf = pygame.image.load("assets\\apple.png").convert_alpha()
        apple_scale_num = 0.5
        self.image = pygame.transform.rotozoom(self.image, 0, apple_scale_num)
        self.rect = self.image.get_rect(center=(250, 200))
        
    # Update function
    def update(self):
        pass


# Function for drawing text on screen
def create_text(font_filepath=None, font_size=10, text="", text_color="White", x_pos=0, y_pos=0, screen=""):
    """
    Auguments:

    font_filepath      Path to font file (Used to load custom font)
    font_size          Set font size (Default: 10)
    text               Set text
    text_color         Set text color (Default: White)
    x_pos              X-position for text (Center-based positioning)
    y_pos              Y-position for text (Center-based positioning)
    """

    # Check if custom font path is provided
    if font_filepath != None:
        text_font = pygame.font.Font(font_filepath, font_size) # Set custom font and size
    else:
        text_font = pygame.font.Font("assets\\font\\Boba Cups.ttf", font_size) # Set default font and size

    text_display = text_font.render(text, True, pygame.color.Color(text_color)) # Draw text
    text_display_rect = text_display.get_rect(center=((screen_width / x_pos, screen_height / y_pos))) # Position text

    screen.blit(text_display, text_display_rect) # Draw text to screen


# Game configuration
game_title = "AppleDroid v0.2"  # Game title (window caption)
screen_width = 800              # Screen width
screen_height = 600             # Screen height
frame_rate = 60                 # Frame rate

# Highscore to keep track of score
highscore_num = 0

# Countdown timer
countdown_default_start_timer_value = 10 # Default start value for countdown timer
countdown_start_timer_value = countdown_default_start_timer_value # Start value for countdown timer [Using default value]
countdown_increase_time = 1 # Increase timer by additional seconds


# Main function to run the game loop and initialization
def main():
    pygame.init() # Initialize pygame

    # Create the screen surface and set the window caption
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(game_title)
    
    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Global variables
    global highscore_num # Highscore count
    global countdown_start_timer_value # Countdown timer start value

    # Get current time since game start
    game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Convert to seconds with one decimal

    # Create a background surface
    background_surface = pygame.Surface((screen_width, screen_height))

    # Player
    player = Player() # Create player
    player_group = pygame.sprite.GroupSingle() # Create SingleGroup (Used to store single sprite)
    player_group.add(player) # Add player to player group

    # Apple
    apple = Apple() # Create apple (object)
    apple_group = pygame.sprite.Group() # Create group (Used to store multiple sprites)
    apple_group.add(apple) # Add apple object to group

    # Main game loop
    running = True # Game-loop running state (Flag to keep game running)
    game_active = True # Game active (Used to reach end-game)
    game_show_start_screen = True # Flag for showing start screen

    while running: # While game-loop is running

        # Handle events
        for event in pygame.event.get():
            # If the user clicks the 'X' button, exit the game
            if event.type == pygame.QUIT: # If "EXIT" is pressed
                running = False # Stop game
            
            # Start screen: If 'SPACE' is pressed, hide start screen
            if game_show_start_screen == True and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("START!")
                game_show_start_screen = False # Hide start screen
                game_active = True # Show game
                game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Reset game start time

            # End screen: If 'SPACE' key is pressed, reset game
            if game_active == False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Reset game start time
                countdown_start_timer_value = countdown_default_start_timer_value # Reset countdown timer to default start value
                highscore_num = 0 # Reset highscore
                game_active = True # Show game

        
        # Start screen: Show
        if game_show_start_screen:
            # Fill screen with grey color
            background_surface.fill(pygame.color.Color("gray70"))
            # Draw background
            screen.blit(background_surface, (0, 0)) 
            
            # Draw game title
            start_screen_game_title = create_text(font_size=70, text=game_title, text_color="White", x_pos=2, y_pos=4, screen=screen)
            # Draw game creator
            start_screen_game_creator = create_text(font_size=30, text="Created by Victor", text_color="White", x_pos=2, y_pos=2.8, screen=screen)
            # Draw info text
            start_screen_info = create_text(font_size=44, text="Press \"SPACE\" to play...", text_color="White", x_pos=2, y_pos=1.3, screen=screen)


        # If game is active = Show game
        if game_active == True and game_show_start_screen == False:  
            # Countdown timer
            current_time = round(pygame.time.get_ticks() / 1000, 1) # Get current time
            elapsed_time = round(current_time - game_start_time, 1) # Calculate elapsed time since game start
            countdown_timer_value = round(countdown_start_timer_value - elapsed_time, 1) # Start countdown timer

            # # Fill screen with grey color
            background_surface.fill(pygame.color.Color("gray60"))
            # Draw background
            screen.blit(background_surface, (0, 0))
            
            # Draw highscore
            highscore_display = create_text(font_size=40, text=f"Score: {highscore_num}", text_color="White", x_pos=2, y_pos=15, screen=screen)
            # Draw countdown timer
            countdown_timer_display = create_text(font_size=25, text=f"Timer: {countdown_timer_value}", text_color="White", x_pos=2, y_pos=7.7, screen=screen)
            
            # Draw player and update
            player_group.draw(screen)
            player_group.update()
            # Draw apple and update
            apple_group.draw(screen)
            apple_group.update()

            # Check if countdown timer reaches 0
            if countdown_timer_value <= 0:
                game_active = False # End game (Show end-screen)

            
        # End screen: Show
        elif game_active == False and game_show_start_screen == False:
            # Fill screen with green color
            background_surface.fill(pygame.color.Color("gray70")) 
            # Draw background
            screen.blit(background_surface, (0, 0))
            # Draw highscore
            end_screen_highscore_display = create_text(font_size=70, text=f"Score: {highscore_num}", text_color="White", x_pos=2, y_pos=4.3, screen=screen)
            # Draw info text
            end_screen_info = create_text(font_size=44, text="Press \"SPACE\" to play...", text_color="White", x_pos=2, y_pos=1.25, screen=screen)

            # Load and draw player image (Image used for display)
            end_screen_player_surf = pygame.image.load("assets\\player.png").convert_alpha() # Load player.png with transparency (Used for pygame performance)
            end_screen_player_surf = pygame.transform.rotozoom(end_screen_player_surf, 0, 2) # Apply scaling to player image
            end_screen_player_rect = end_screen_player_surf.get_rect(center=((screen_width / 2, screen_height / 2))) # Set player image position
            screen.blit(end_screen_player_surf, end_screen_player_rect) # Draw player image to screen
            


        # Update the display to show the new frame
        pygame.display.flip()

        # Control the frame rate
        clock.tick(frame_rate)

    # Quit pygame and exit the script
    pygame.quit()
    sys.exit()


# Run the main function when the script is executed
if __name__ == "__main__":
    main()
