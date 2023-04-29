"""
AppleDroid v0.1

A small python game where you control an Android with the objective of collecting as many apples as possible.


TO-DO:
- BUG: apple spawn so it do not spawn inside highscore text
- ADD: Coundown-timer to reach end-game (In order to show end-screen)
- - End-screen is currently showing when highscore 10 is reached
"""


# Import modules
import pygame
import sys
import random


# Game configuration
game_title = "AppleDroid v0.1"  # Game title (window caption)
screen_width = 800              # Screen width
screen_height = 600             # Screen height
frame_rate = 60                 # Frame rate

# Player movement speed
player_move_speed_x = 4
player_move_speed_y = 4

# Highscore to keep track of score
highscore_num = 0

# Timer countdown
countdown_start_time = 10 # Start countdown at 10 seconds
countdown_timer_increase = 1 # Increase timer by 1 second


# Main function to run the game loop and initialization
def main():
    pygame.init() # Initialize pygame

    # Create the screen surface and set the window caption
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(game_title)
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate

    # Create a background surface and fill it with grey color
    background_surface = pygame.Surface((screen_width, screen_height))

    #    LOAD ASSETS    #
    # Highscore:
    global highscore_num # Highscore count
    font_highscore = pygame.font.Font("assets\\font\\Boba Cups.ttf", 40) # Set font and size for highscore
    text_highscore = font_highscore.render(f"Score: {highscore_num}", True, pygame.color.Color("White")) # Render highscore in white
    text_highscore_rect = text_highscore.get_rect(center=( (screen_width / 2, screen_height / 15))) # Position highscore text
    # End-screen: Highscore
    end_font_highscore = pygame.font.Font("assets\\font\\Boba Cups.ttf", 80)
    end_text_highscore = end_font_highscore.render(f"Highscore: {highscore_num}", True, pygame.color.Color("White"))
    end_text_highscore_rect = end_text_highscore.get_rect(center=(screen_width / 2, screen_height / 1.4))

    # Countdown timer:
    global countdown_start_time # Countdown timer start
    global countdown_timer_increase # Increase countdown timer 
    font_countdown_timer = pygame.font.Font("assets\\font\\Boba Cups.ttf", 25)
    text_countdown_timer = font_countdown_timer.render(f"Timer: {00.0}", True, pygame.color.Color("White"))
    text_countdown_timer_rect = text_countdown_timer.get_rect(center=((screen_width / 2, screen_height / 7.7)))

    # Player:
    global player_move_speed_x # X-axis player move speed
    global player_move_speed_y # Y-axis player move speed
    player_surf = pygame.image.load("assets\\player.png").convert_alpha() # Load player.png with transparency (Used for pygame performance)
    player_scale_num = 0.7 # Player scaling factor
    player_surf = pygame.transform.scale(player_surf, (player_surf.get_width() * player_scale_num, player_surf.get_height() * player_scale_num,))  # Apply scaling to player (Use transform.rotozoom instead)
    player_rect = player_surf.get_rect(center=(100, 100)) # Set initial player position
    # End-screen: Player
    end_player_scale_num = 2.5
    end_player_surf = pygame.transform.scale(player_surf, (player_surf.get_width() * end_player_scale_num, player_surf.get_height() * end_player_scale_num,))
    end_player_rect = player_surf.get_rect(center=((screen_width - end_player_surf.get_width()/2) / 2, screen_height / 3))

    # Apple:
    apple_surf = pygame.image.load("assets\\apple.png").convert_alpha()
    apple_scale_num = 0.5
    apple_surf = pygame.transform.scale(apple_surf, (apple_surf.get_width() * apple_scale_num, apple_surf.get_height() * apple_scale_num,))
    apple_rect = apple_surf.get_rect(center=(250, 200))

    # Main game loop
    running = True # Game-loop running state (Flag to keep game running)
    game_active = True # Game active (Used for end-screen)

    while running: # While game-loop is running

        # Handle events
        for event in pygame.event.get():
            # If the user clicks the 'X' button, exit the game
            if event.type == pygame.QUIT: # If "EXIT" is pressed
                running = False # Stop game

        
        # If game is active (Show game)
        if game_active:  
            # Fill screen with grey color
            background_surface.fill(pygame.color.Color("gray60"))
            
            # Countdown timer
            countdown_timer = round(pygame.time.get_ticks() / 1000, 1) # Countdown timer in seconds with 1 decimal
            countdown_timer_text = round(countdown_start_time - countdown_timer, 1) # Initial countdown text
            text_countdown_timer = font_countdown_timer.render(f"Timer: {countdown_timer_text}", True, pygame.color.Color("White")) # Update countdown text

            # Draw assets to screen
            screen.blit(background_surface, (0, 0))                         # Background surface
            screen.blit(text_highscore, text_highscore_rect)                # Highscore text
            screen.blit(text_countdown_timer, text_countdown_timer_rect)    # Countdown timer
            screen.blit(player_surf, player_rect)                           # Player
            screen.blit(apple_surf, apple_rect)                             # Apple

            # Check if countdown timer reaches 0
            if countdown_timer_text <= 0:
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
                countdown_start_time += countdown_timer_increase # Increase countdown timer
        
        # If game is not active (Show end-screen)
        else:
            # Fill screen with green color
            background_surface.fill(pygame.color.Color("gray80")) 
            
            # Update score text
            end_text_highscore = end_font_highscore.render(f"Highscore: {highscore_num}", True, pygame.color.Color("White"))
            
            # Draw assets to screen
            screen.blit(background_surface, (0, 0))                     # Background surface
            screen.blit(end_text_highscore, end_text_highscore_rect)    # Highscore text
            screen.blit(end_player_surf, end_player_rect)               # Player image
    

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
