# config/__init__.py

# Game setup configuration
from .configuration import SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_RATE, GAME_TITLE

# Image paths + font path
from .configuration import GAME_ICON_IMAGE_PATH, FONT_PATH, PLAYER_IMAGE_PATH, APPLE_IMAGE_PATH, GOLD_APPLE_IMAGE_PATH, BG_IMAGE_FOLDER_PATH, ARROW_KEYS_IMAGE_PATH, ENTER_KEY_IMAGE_PATH, SPACE_KEY_IMAGE_PATH
# Sound paths
from .configuration import MENU_SELECTION_SOUND_PATH, GOLD_APPLE_SPAWN_SOUND_PATH, PURPLE_APPLE_COLLISION_SOUND_PATH, GOLD_APPLE_COLLISION_SOUND_PATH

# Player movement speed
from .configuration import PLAYER_MOVE_SPEED_X, PLAYER_MOVE_SPEED_Y

# Gameplay behavior variables
from .configuration import COUNTDOWN_DEFAULT_START_TIMER_VALUE, APPLE_TIME_BONUS, GOLD_APPLE_TIME_BONUS, GOLD_APPLE_SPAWN_CHANCE, GOLD_APPLE_CHECK_INTERVAL

# Custom debug function
from .debug import debug