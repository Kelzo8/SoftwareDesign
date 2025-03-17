from enum import Enum

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (50, 50, 50)
LIGHT_GRAY = (240, 240, 245)
DARK_GRAY = (50, 50, 50)
GOLD = (255, 215, 0)

# Lane settings
NUM_LANES = 12
LANE_WIDTH = SCREEN_WIDTH // NUM_LANES

# Player car settings
PLAYER_CAR_SPEED = 5

# Enemy car settings
ENEMY_CAR_SPEED = 5
NEW_ENEMY_CAR_PROBABILITY = 20

# Coin settings
NEW_COIN_PROBABILITY = 50

# Road animation settings
ROAD_LINE_HEIGHT = 20
ROAD_LINE_GAP = 20

# Checkpoint settings
CHECKPOINT_COIN_COUNT = 5
CHECKPOINT_IMMUNE_TIME = 5  # 3 seconds

class CarDimensions(Enum):
    PLAYER_CAR_WIDTH = LANE_WIDTH * 0.8
    PLAYER_CAR_HEIGHT = PLAYER_CAR_WIDTH * 2
    ENEMY_CAR_WIDTH = LANE_WIDTH * 0.8
    ENEMY_CAR_HEIGHT = ENEMY_CAR_WIDTH * 2