# config/debug.py

"""
Debug Class

This class draws some text on screen, that can be used for debugging purposes

Note: Text is positioned from top left corner, not center-based
"""

import pygame

# Draw debug text
def debug(text="", font_size=30, color="White", x_pos=10, y_pos=10, enable_bg=False, bg_color="Black"):
    screen = pygame.display.get_surface() # Get current display surface

    font = pygame.font.SysFont("Arial", font_size) # Create font
    display_text = font.render(str(text), True, color) # Create text
    display_text_rect = display_text.get_rect(topleft=(x_pos, y_pos)) # Position text

    # Check if background is enabled
    if enable_bg == True:
        pygame.draw.rect(screen, bg_color, display_text_rect) # Draw background
    
    screen.blit(display_text, display_text_rect) # Draw text

        


    