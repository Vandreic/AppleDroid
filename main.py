"""
AppleDroid v0.2

A small python game where you control an Android with the objective of collecting as many apples as possible.


TO-DO:
- BUG: Fix apple spawn so it do not spawn inside highscore & countdown text
- BUG: Fix player & apple spawn after game restart (Create new x- & y-pos for new spawn)
- Update code:
-- Create functions to load images & text
--- Update calculations for positioning (Use multiplication instead of division?)
--- Update scale method to 'transform.rotozoom' (Sligthy better image quality)
-- Create spawn function for apple
-- Update general code structure
"""


# Import modules
import pygame
import sys
import random


# Game configuration
game_title = "AppleDroid v0.2"  # Game title (window caption)
screen_width = 800              # Screen width
screen_height = 600             # Screen height
frame_rate = 60                 # Frame rate

# Player movement speed
player_move_speed_x = 4
player_move_speed_y = 4

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

    # Get current time since game start
    game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Convert to seconds with one decimal

    # Create a background surface
    background_surface = pygame.Surface((screen_width, screen_height))

    #    LOAD ASSETS    #
    # Highscore:
    global highscore_num # Highscore count
    font_highscore = pygame.font.Font("assets\\font\\Boba Cups.ttf", 40) # Set font and size for highscore
    text_highscore = font_highscore.render(f"Score: {highscore_num}", True, pygame.color.Color("White")) # Render highscore in white
    text_highscore_rect = text_highscore.get_rect(center=((screen_width / 2, screen_height / 15))) # Position highscore text

    # Countdown timer:
    font_countdown_timer = pygame.font.Font("assets\\font\\Boba Cups.ttf", 25)
    text_countdown_timer = font_countdown_timer.render(f"Timer: {00.0}", True, pygame.color.Color("White"))
    text_countdown_timer_rect = text_countdown_timer.get_rect(center=((screen_width / 2, screen_height / 7.7)))
    global countdown_start_timer_value # Countdown timer start value

    # Player:
    global player_move_speed_x # X-axis player move speed
    global player_move_speed_y # Y-axis player move speed
    player_surf = pygame.image.load("assets\\player.png").convert_alpha() # Load player.png with transparency (Used for pygame performance)
    player_scale_num = 0.7 # Player scaling factor
    player_surf = pygame.transform.scale(player_surf, (player_surf.get_width() * player_scale_num, player_surf.get_height() * player_scale_num,))  # Apply scaling to player (Use transform.rotozoom instead)
    player_rect = player_surf.get_rect(center=(100, 100)) # Set initial player position

    # Apple
    apple_surf = pygame.image.load("assets\\apple.png").convert_alpha()
    apple_scale_num = 0.5
    apple_surf = pygame.transform.scale(apple_surf, (apple_surf.get_width() * apple_scale_num, apple_surf.get_height() * apple_scale_num,))
    apple_rect = apple_surf.get_rect(center=(250, 200))

    # Start-screen: Game title text
    start_font_game_title = pygame.font.Font("assets\\font\\Boba Cups.ttf", 70)
    start_text_game_title = start_font_game_title.render(game_title, True, pygame.color.Color("White"))
    start_text_game_title_rect = start_text_game_title.get_rect(center=(screen_width / 2, screen_height / 4))

    # Start-screen: Game creator text
    start_font_game_creator = pygame.font.Font("assets\\font\\Boba Cups.ttf", 30)
    start_text_game_creator = start_font_game_creator.render("Created by Victor", True, pygame.color.Color("White"))
    start_text_game_creator_rect = start_text_game_creator.get_rect(center=(screen_width / 2, screen_height / 2.8))

    # Start-screen: Info text
    start_font_info = pygame.font.Font("assets\\font\\Boba Cups.ttf", 44)
    start_text_info = start_font_info.render("Press \"SPACE\" to play...", True, pygame.color.Color("White"))
    start_text_info_rect = start_text_info.get_rect(center=(screen_width / 2, screen_height / 1.3))

    # End-screen: Highscore
    end_font_highscore = pygame.font.Font("assets\\font\\Boba Cups.ttf", 70)
    end_text_highscore = end_font_highscore.render(f"Highscore: {highscore_num}", True, pygame.color.Color("White"))
    end_text_highscore_rect = end_text_highscore.get_rect(center=(screen_width / 2, screen_height / 4))

    # End-screen: Player
    end_player_scale_num = 2.5
    end_player_surf = pygame.transform.scale(player_surf, (player_surf.get_width() * end_player_scale_num, player_surf.get_height() * end_player_scale_num,))
    end_player_rect = player_surf.get_rect(center=((screen_width - end_player_surf.get_width()/2) / 2, screen_height / 2.47))

    # End-screen: Info text
    end_font_info = pygame.font.Font("assets\\font\\Boba Cups.ttf", 44)
    end_text_info = end_font_info.render("Press \"SPACE\" to play again...", True, pygame.color.Color("White"))
    end_text_info_rect = end_text_info.get_rect(center=(screen_width / 2, screen_height / 1.3))


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
            
            if game_show_start_screen == True and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("START!")
                game_show_start_screen = False
                game_active = True
                game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Reset game start time

            # If on end-screen and 'SPACE' key is pressed, reset game
            if game_active == False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_start_time = round(pygame.time.get_ticks() / 1000, 1) # Reset game start time
                countdown_start_timer_value = countdown_default_start_timer_value # Reset countdown timer to default start value
                highscore_num = 0 # Reset highscore
                game_active = True # Show game

        
        # If true, show start screen
        if game_show_start_screen:
            # Fill screen with grey color
            background_surface.fill(pygame.color.Color("gray70"))

            screen.blit(background_surface, (0, 0)) 
            screen.blit(start_text_game_title, start_text_game_title_rect)
            screen.blit(start_text_game_creator, start_text_game_creator_rect)
            screen.blit(start_text_info, start_text_info_rect)              # Info text



        # If game is active (Show game)
        if game_active == True and game_show_start_screen == False:  
            # Fill screen with grey color
            background_surface.fill(pygame.color.Color("gray60"))
            
            # Update score text
            text_highscore = font_highscore.render(f"Score: {highscore_num}", True, pygame.color.Color("White"))

            # Countdown timer
            current_time = round(pygame.time.get_ticks() / 1000, 1) # Get current time
            elapsed_time = round(current_time - game_start_time, 1) # Calculate elapsed time since game start

            countdown_timer_value = round(countdown_start_timer_value - elapsed_time, 1) # Start countdown timer
            text_countdown_timer = font_countdown_timer.render(f"Timer: {countdown_timer_value}", True, pygame.color.Color("White")) # Update text for countdown timer


            # Draw assets to screen
            screen.blit(background_surface, (0, 0))                         # Background surface
            screen.blit(text_highscore, text_highscore_rect)                # Highscore text
            screen.blit(text_countdown_timer, text_countdown_timer_rect)    # Countdown timer
            screen.blit(player_surf, player_rect)                           # Player
            screen.blit(apple_surf, apple_rect)                             # Apple (Regular)


            # Check if countdown timer reaches 0
            if countdown_timer_value <= 0:
                game_active = False # End game (Show end-screen)


            keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
            # Check keyboard input and update player position
            # LEFT ARROW
            if keys[pygame.K_LEFT] and player_rect.left >= player_move_speed_x: # If player is inside game boundaries and key is pressed
                player_rect.x -= player_move_speed_x # Move player
            # RIGHT ARROW
            if keys[pygame.K_RIGHT] and player_rect.right <= (screen_width - player_move_speed_x):
                player_rect.x += player_move_speed_x
            # UP ARROW
            if keys[pygame.K_UP] and player_rect.top >= player_move_speed_y:
                player_rect.y -= player_move_speed_y
            # DOWN ARROW
            if keys[pygame.K_DOWN] and player_rect.bottom <= (screen_height - player_move_speed_y):
                player_rect.y += player_move_speed_y


            # Check if player collides with apple
            if player_rect.colliderect(apple_rect):
                # New x- & y-pos for apple (Used for respawn)
                new_apple_pos_x = random.randint(10, screen_width - apple_surf.get_width())
                new_apple_pos_y = random.randint(10, screen_height - apple_surf.get_height())
                apple_rect.topleft = (new_apple_pos_x, new_apple_pos_y) # Move apple to new pos
                
                highscore_num += 1 # Increase score
                text_highscore = font_highscore.render(f"Score: {highscore_num}", True, pygame.color.Color("White")) # Update score text

                countdown_start_timer_value += countdown_increase_time # Increase countdown timer
                text_countdown_timer = font_countdown_timer.render(f"Timer: {countdown_timer_value}", True, pygame.color.Color("White")) # Update text for countdown timer

                
        # If game is not active (Show end-screen)
        elif game_active == False and game_show_start_screen == False:
            # Fill screen with green color
            background_surface.fill(pygame.color.Color("gray70")) 

            # Update score text
            end_text_highscore = end_font_highscore.render(f"Highscore: {highscore_num}", True, pygame.color.Color("White"))
            
            # Draw assets to screen
            screen.blit(background_surface, (0, 0))                     # Background surface
            screen.blit(end_text_highscore, end_text_highscore_rect)    # Highscore text
            screen.blit(end_player_surf, end_player_rect)               # Player image
            screen.blit(end_text_info, end_text_info_rect)              # Info text


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
