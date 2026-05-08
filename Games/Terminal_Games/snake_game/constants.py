# Game Configuration Constants

# Window dimensions
INITIAL_WINDOW_WIDTH = 800
INITIAL_WINDOW_HEIGHT = 800
WINDOW_MIN_BUFFER = 40
MIN_UI_WIDTH = 500

SCREEN_SIZES = {
    "Small": 400,
    "Medium": 600,
    "Large": 800
}
# Default values (will be updated at runtime)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
UI_HEIGHT = 80 # Increased for more spacing

# Grid settings
GRID_SIZE = 10
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors (R, G, B)
COLOR_BACKGROUND = (30, 30, 30)
COLOR_SNAKE_HEAD = (0, 255, 100)
COLOR_SNAKE_BODY = (0, 200, 80)
COLOR_FOOD = (255, 50, 50)
COLOR_TEXT = (255, 255, 255)

# Game settings
INITIAL_FPS = 10
SPEED_INCREMENT = 0.5
SCORE_PER_FOOD = 10
BONUS_SCORE_MULTIPLIER = 5
DIFFICULTY_STEP = 50 # Increase speed every 50 points

# Game Modes
MODE_WALL_COLLISION = "Standard"
MODE_WRAP_AROUND = "Wrap Around"

# Difficulty Levels
DIFFICULTY_LEVELS = {
    "Base": {
        "start_fps": 7,
        "growth_rate": 1,
        "speed_inc": 0.2,
        "bonus_threshold": 50,
        "bonus_duration": 10 # seconds
    },
    "Pro": {
        "start_fps": 10,
        "growth_rate": 1,
        "speed_inc": 0.5,
        "bonus_threshold": 80,
        "bonus_duration": 8
    },
    "Pro Max": {
        "start_fps": 15,
        "growth_rate": 2,
        "speed_inc": 0.8,
        "bonus_threshold": 120,
        "bonus_duration": 7
    },
    "Ultra Pro Max": {
        "start_fps": 20,
        "growth_rate": 3,
        "speed_inc": 1.2,
        "bonus_threshold": 200,
        "bonus_duration": 6
    },
    "Ultra Pro Max +": {
        "start_fps": 25,
        "growth_rate": 5,
        "speed_inc": 2.0,
        "bonus_threshold": 300,
        "bonus_duration": 5
    }
}

# Adaptive Board: difficulty → board size mapping (F11)
DIFFICULTY_SIZE_MAP = {
    "Base": "Small",
    "Pro": "Small",
    "Pro Max": "Medium",
    "Ultra Pro Max": "Large",
    "Ultra Pro Max +": "Large"
}

COLOR_BUTTON = (50, 50, 50)
COLOR_BUTTON_HOVER = (70, 70, 70)
COLOR_BONUS_FOOD = (255, 215, 0) # Gold
COLOR_TIMER = (255, 100, 100) # Red-ish

# Save Data
SAVE_DATA_PATH = "save_data.json"
DEFAULT_SAVE_DATA = {
    "high_score": 0,
    "total_games": 0,
    "total_golden_food": 0,
    "last_mode": None,
    "last_level": None
}
