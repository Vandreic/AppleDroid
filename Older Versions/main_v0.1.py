"""
AppleDroid v0.1
A small python game where you control an Android with the objective of collecting as many apples as possible.

TO-DO:
- Fix apple spawn so it do not spawn inside highscore text
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


# Main function to run the game loop and initialization
def main():
    pygame.init() # Initialize pygame

    # Create the screen surface and set the window caption
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(game_title)
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate

    # Create a background surface and fill it with grey color
    background_surface = pygame.Surface((screen_width, screen_height))
    background_surface.fill(pygame.color.Color("Grey"))

    #    LOAD ASSETS    #
    # Highscore:
    global highscore_num # Highscore count
    font_highscore = pygame.font.Font("assets\\font\\Boba Cups.ttf", 40) # Set font and size for highscore
    text_highscore = font_highscore.render(f"Score: {highscore_num}", True, pygame.color.Color("White")) # Render highscore in white
    text_highscore_rect = text_highscore.get_rect(center=(screen_width / 2, screen_height / 15)) # Position highscore text

    # Player:
    global player_move_speed_x # X-axis player move speed
    global player_move_speed_y # Y-axis player move speed
    player_surf = pygame.image.load("assets\\player.png").convert_alpha() # Load player.png with transparency (Used for pygame performance)
    player_scale_num = 0.7 # Player scaling factor
    player_surf = pygame.transform.scale(player_surf, (player_surf.get_width() * player_scale_num, player_surf.get_height() * player_scale_num,))  # Apply scaling to player (Use transform.rotozoom instead)
    player_rect = player_surf.get_rect(center=(100, 100)) # Set initial player position

    # Apple:
    apple_surf = pygame.image.load("assets\\apple.png").convert_alpha()
    apple_scale_num = 0.5
    apple_surf = pygame.transform.scale(apple_surf, (apple_surf.get_width() * apple_scale_num, apple_surf.get_height() * apple_scale_num,))
    apple_rect = apple_surf.get_rect(center=(600, 400))

    # Main game loop
    running = True # Game running state (Flag to keep game running)
    while running: # While game is running

        # Draw assets to screen
        screen.blit(background_surface, (0, 0))
        screen.blit(text_highscore, text_highscore_rect)
        screen.blit(player_surf, player_rect)
        screen.blit(apple_surf, apple_rect)

        # Handle events
        for event in pygame.event.get():
            # If the user clicks the 'X' button, exit the game
            if event.type == pygame.QUIT: # If "EXIT" is pressed
                running = False # Stop game

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