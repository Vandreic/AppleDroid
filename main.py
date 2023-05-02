"""
AppleDroid v0.3

A small python game where you control an Android with the objective of collecting as many apples as possible.


TO-DO:
- BUG: Fix apple spawn
       * No spawn inside highscore & countdown text
       * No spawn inside player spawn area

"""


# Import modules
import pygame
import sys
import random


# Game configuration
game_title = "AppleDroid v0.3"  # Game title (window caption)
screen_width = 800              # Screen width
screen_height = 600             # Screen height
frame_rate = 60                 # Frame rate

# Highscore to keep track of score
highscore_num = 0

# Countdown timer
countdown_default_start_timer_value = 10 # Default start value for countdown timer
countdown_start_timer_value = countdown_default_start_timer_value # Start value for countdown timer [Using default value]
countdown_increase_time = 1 # Increase timer by additional seconds


# Player class
class Player(pygame.sprite.Sprite):

    # Player movement speed
    player_move_speed_x = 4
    player_move_speed_y = 4

    # Default x- & y-pos
    x_pos = screen_width / 2
    y_pos = screen_height / 2

    # Player scaling factor
    player_scale_num = 0.7

    # Constructor: Initialize the object
    def __init__(self):
        super().__init__() # Call the parent class (Sprite) constructor
        self.image = pygame.image.load("assets\\player.png").convert_alpha() # Load player.png with transparency (Used for pygame performance)
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

    # Default x- & y-pos
    x_default_pos = 200
    y_default_pos = 200

    # Apple scale factor
    apple_scale_num = 0.5

    def __init__(self):
        super().__init__()
        self.image = apple_surf = pygame.image.load("assets\\apple.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, self.apple_scale_num)
        self.rect = self.image.get_rect(center=(self.x_default_pos, self.y_default_pos))

    # Respawn apple to new location
    def respawn(self, default_spawn_location=False):

        # Check if default spawn location in enabled
        if default_spawn_location == True:
            self.rect.center = (self.x_default_pos, self.y_default_pos) # Spawn to default position
        
        # Spawn to random position
        else:
            spawn_margin = 4 # Minimum spawn distance from screen edge (in pixels)

            # Set minimum spawn distance from screen edge
            x_min_pos = int(self.image.get_width()/2) + spawn_margin
            x_max_pos = int(screen_width - self.image.get_width()/2) - spawn_margin

            y_min_pos = int(self.image.get_height()/2) + spawn_margin
            y_max_pos = int(screen_height - self.image.get_height()/2) - spawn_margin

            # Create random x- & y-pos
            x_pos = random.randint(x_min_pos, x_max_pos)
            y_pos = random.randint(y_min_pos, y_max_pos)

            # Move apple to new x- & y-pos
            self.rect.center = (x_pos, y_pos)

    # Update function
    def update(self):
        pass

# Game screen class (Handles game screens)
class GameScreen():

    # Create a background surface
    background_surface = pygame.Surface((screen_width, screen_height))

    def __init__(self, screen):
        self.screen = screen # Store game screen 

    # Start screen
    def start_screen(self):
        # Fill screen with grey color
        self.background_surface.fill(pygame.color.Color("gray70"))
        # Draw background
        self.screen.blit(self.background_surface, (0, 0)) 
            
        # Draw game title
        start_screen_game_title = create_text(font_size=70, text=game_title, x_pos=2, y_pos=4, screen=self.screen)
        # Draw game creator
        start_screen_game_creator = create_text(font_size=30, text="Created by Victor", x_pos=2, y_pos=2.8, screen=self.screen)
        # Draw info text
        start_screen_info = create_text(font_size=44, text="Press \"SPACE\" to play...", x_pos=2, y_pos=1.3, screen=self.screen)

    # Main screen
    def main_screen(self):
        # Fill screen with grey color
        self.background_surface.fill(pygame.color.Color("gray60"))
        # Draw background
        self.screen.blit(self.background_surface, (0, 0))
        # Draw highscore
        highscore_display = create_text(font_size=40, text=f"Score: {highscore_num}", x_pos=2, y_pos=15, screen=self.screen)
        # Draw countdown timer
        countdown_timer_display = create_text(font_size=25, text=f"Timer: {self.countdown_timer_value}", x_pos=2, y_pos=7.7, screen=self.screen)
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
        end_screen_highscore_display = create_text(font_size=70, text=f"Score: {highscore_num}", x_pos=2, y_pos=4.3, screen=self.screen)
        # Draw info text
        end_screen_info = create_text(font_size=44, text="Press \"SPACE\" to play again...", x_pos=2, y_pos=1.25, screen=self.screen)

        # Load and draw player image (Image used for display)
        end_screen_player_surf = pygame.image.load("assets\\player.png").convert_alpha() # Load player.png with transparency (Used for pygame performance)
        end_screen_player_surf = pygame.transform.rotozoom(end_screen_player_surf, 0, 2) # Apply scaling to player image
        end_screen_player_rect = end_screen_player_surf.get_rect(center=((screen_width / 2, screen_height / 2))) # Set player image position
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

    # Get countdown timer text
    def render_countdown_timer(self, countdown_timer_value=""):
        self.countdown_timer_value = countdown_timer_value

    # Update frame (Needed to be updated constantly)
    def update_frame(self):
        
        # Main screen: if active, update frame
        if self.active_game_screen == "main_screen":
            self.main_screen()


# Game logic class
class Game():

    def __init__(self):
        pygame.init() # Initialize pygame

        # Create the screen surface and set the window caption
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(game_title)
        
        # Create a clock object to control the frame rate
        self.clock = pygame.time.Clock()

        # Get current time since game start
        self.game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Convert to seconds with one decimal

        # Handle game screens
        self.game_screen = GameScreen(screen)

        # Player
        self.player = Player() # Create player
        self.player_group = pygame.sprite.GroupSingle() # Create SingleGroup (Used to store single sprite)
        self.player_group.add(self.player) # Add player to player group
        
        # Apple
        self.apple = Apple() # Create apple (object)
        self.apple_group = pygame.sprite.Group() # Create group (Used to store multiple sprites)
        self.apple_group.add(self.apple) # Add apple object to group
        
        # Draw player & apple to screen
        self.game_screen.render_sprites(player_group=self.player_group, sprite_group=self.apple_group)

        # Show start screen
        self.game_screen.screen_manager("start_screen")

    # Update function (Game loop = Needed run constantly)
    def update(self):
        # Global variables
        global highscore_num # Highscore count
        global countdown_start_timer_value # Countdown timer start value

        # Update screen frame
        self.game_screen.update_frame()
        # Update player
        self.player_group.update()
        # Update apple
        self.apple_group.update()

        # Countdowntimer - Check if main screen is active
        if self.game_screen.active_game_screen == "main_screen":
            # Countdown timer
            current_time = round(pygame.time.get_ticks() / 1000, 1) # Get current time
            elapsed_time = round(current_time - self.game_start_time, 1) # Calculate elapsed time since game start
            countdown_timer_value = round(countdown_start_timer_value - elapsed_time, 1) # Start countdown timer

            # Check if countdown timer reaches 0
            if countdown_timer_value <= 0:
                # Show start screen
                self.game_screen.screen_manager("end_screen") # Change to end screen
                #self.game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Reset current time since game start
                current_time = round(pygame.time.get_ticks() / 1000, 1) # Reset current time
                countdown_start_timer_value = countdown_default_start_timer_value # Reset countdown timer value to default
                highscore_num = 0 # Reset highscore
                self.player.respawn() # Respawn player to default position
                self.apple.respawn(True) # Respawn apple to default position
                print(f"current_time: {current_time} elapsed_time: {elapsed_time} countdown_timer_value: {countdown_timer_value}")

        # If main screen is not active, reset countdown timer value
        else:
            countdown_timer_value = 0 # Reset countdown timer value
            self.game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Reset current time since game start
                

        # Draw countdown timer
        self.game_screen.render_countdown_timer(countdown_timer_value)

        # Check for collision:
        is_collision = pygame.sprite.spritecollide(self.player_group.sprite, self.apple_group, False)
        if is_collision: # If collision = True
            self.apple.respawn() # Respawn apple
            highscore_num += 1 # Increase highscore
            countdown_start_timer_value += countdown_increase_time # Increase countdown timer
            
        # Handle events
        for event in pygame.event.get():
            # If the user clicks the 'X' button, exit the game
            if event.type == pygame.QUIT:
                pygame.quit() # Quit pygame
                sys.exit() # Exit script
            
            # Check if 'SPACE' is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game_screen.key_input(True) # Update game class with key input

        # Update the display to show the new frame
        pygame.display.flip()

        # Control the frame rate
        self.clock.tick(frame_rate)


# Function for drawing text on screen
def create_text(font_size=10, text="", x_pos=0, y_pos=0, screen=""):
    """
    Auguments:

    font_size          Set font size (Default: 10)
    text               Set text
    x_pos              X-position for text (Center-based positioning)
    y_pos              Y-position for text (Center-based positioning)
    """

    text_font = pygame.font.Font("assets\\font\\Boba Cups.ttf", font_size) # Set font and size
    text_display = text_font.render(text, True, pygame.color.Color("White")) # Draw text
    text_display_rect = text_display.get_rect(center=((screen_width / x_pos, screen_height / y_pos))) # Position text

    screen.blit(text_display, text_display_rect) # Draw text to screen



def main():
    game = Game() # Create game
    
    while True: # Needed in order to run game constantly
        game.update() # Run game loop

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
