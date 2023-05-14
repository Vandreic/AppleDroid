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
GAME_TITLE = "AppleDroid v0.6" # Game title

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
FONT_PATH = "assets/font/boba_cups.ttf" # Default font

# ---- Images paths ---- #
GAME_ICON_IMAGE_PATH = "assets/images/game_icon.png" # Game icon image
PLAYER_IMAGE_PATH = "assets/images/player.png" # Player image
APPLE_IMAGE_PATH = "assets/images/apple.png" # Apple image
GOLD_APPLE_IMAGE_PATH ="assets/images/gold_apple.png" # Gold apple image
BG_IMAGE_FOLDER_PATH = "assets/images/backgrounds/" # Background image (folder) path: Files are called bg_1.png, bg_2.png, etc.
ARROW_KEYS_IMAGE_PATH = "assets/images//keyboard_keys/arrow_keys.png" # Arrow keys image
ENTER_KEY_IMAGE_PATH = "assets/images/keyboard_keys/enter_key.png" # Enter key image
SPACE_KEY_IMAGE_PATH = "assets/images/keyboard_keys/space_key.png" # Space key image

# ---- Sounds paths ---- #
MENU_SELECTION_SOUND_PATH = "assets/sounds/menu_selection.wav" # Sound for menu selection
GOLD_APPLE_SPAWN_SOUND_PATH = "assets/sounds/gold_apple_spawn_sound.wav" # Gold apple spawn sound 
PURPLE_APPLE_COLLISION_SOUND_PATH = "assets/sounds/purple_apple_collision.wav" # Purple apple collision sound
GOLD_APPLE_COLLISION_SOUND_PATH = "assets/sounds/gold_apple_collision.wav" # Gold apple collision sound