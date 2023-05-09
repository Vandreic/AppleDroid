# config/__init__.py

# Game setup configuration
from .configuration import SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_RATE, GAME_TITLE

# File paths
from .configuration import FONT_PATH, PLAYER_IMAGE_PATH, APPLE_IMAGE_PATH, GOLD_APPLE_IMAGE_PATH

# Player movement speed
from .configuration import PLAYER_MOVE_SPEED_X, PLAYER_MOVE_SPEED_Y

# Gameplay behavior variables
from .configuration import COUNTDOWN_DEFAULT_START_TIMER_VALUE, APPLE_TIME_BONUS, GOLD_APPLE_TIME_BONUS, GOLD_APPLE_SPAWN_CHANCE, GOLD_APPLE_CHECK_INTERVAL

# Custom debug function
from .debug import debug