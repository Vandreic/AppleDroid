# config/configuration.py

"""
Configuration Class

This class contains the game's configuration settings and asset paths, defining various parameters 
such as screen dimensions, frame rate, game title, and gameplay behavior variables. It also sets 
player settings, font paths, and image paths for game elements like the player, apple, and gold apple.
"""

# ---- Game setup configuration ---- #
SCREEN_WIDTH = 800  # Screen width (in pixels)
SCREEN_HEIGHT = 600 # Screen height (in pixels)
FRAME_RATE = 60 # Game frame rate (in frames per second)
GAME_TITLE = "AppleDroid v0.4" # Game title

# ---- Gameplay behavior variables ---- #
COUNTDOWN_DEFAULT_START_TIMER_VALUE = 10 # Default start value for countdown timer (in seconds)

APPLE_TIME_BONUS = 1 # Time bonus for collecting apple (in seconds)
GOLD_APPLE_TIME_BONUS = 2 # Time bonus for collecting gold apple (in seconds)

GOLD_APPLE_SPAWN_CHANCE = 60 # Gold apple spawn chance (in percent)
GOLD_APPLE_CHECK_INTERVAL = 2.5 # Gold apple spawn check interval (in seconds)

# ---- Player settings ---- #
PLAYER_MOVE_SPEED_X = 4 # Player movement speed x-axis (in pixels)
PLAYER_MOVE_SPEED_Y = 4 # Player movement speed y-axis (in pixels)

# ---- Font paths ---- #
FONT_PATH = "assets\\font\\boba_cups.ttf" # Default font path

# ---- Images paths ---- #
PLAYER_IMAGE_PATH = "assets\\images\\player.png" # Player image path
APPLE_IMAGE_PATH = "assets\\images\\apple.png" # Apple image path
GOLD_APPLE_IMAGE_PATH ="assets\\images\\gold_apple.png" # Gold apple image path