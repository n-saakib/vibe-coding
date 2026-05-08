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
        "bonus_duration": 10, # seconds
        "max_fps": 30,
        "curve_early_step": 30,   # pts per increment in early phase (0-200)
        "curve_mid_step": 60,     # pts per increment in mid phase (200-500)
        "curve_late_step": 100    # pts per increment in late phase (500+)
    },
    "Pro": {
        "start_fps": 10,
        "growth_rate": 1,
        "speed_inc": 0.5,
        "bonus_threshold": 80,
        "bonus_duration": 8,
        "max_fps": 35,
        "curve_early_step": 30,
        "curve_mid_step": 55,
        "curve_late_step": 90
    },
    "Pro Max": {
        "start_fps": 15,
        "growth_rate": 2,
        "speed_inc": 0.8,
        "bonus_threshold": 120,
        "bonus_duration": 7,
        "max_fps": 40,
        "curve_early_step": 25,
        "curve_mid_step": 50,
        "curve_late_step": 85
    },
    "Ultra Pro Max": {
        "start_fps": 20,
        "growth_rate": 3,
        "speed_inc": 1.2,
        "bonus_threshold": 200,
        "bonus_duration": 6,
        "max_fps": 50,
        "curve_early_step": 25,
        "curve_mid_step": 45,
        "curve_late_step": 80
    },
    "Ultra Pro Max +": {
        "start_fps": 25,
        "growth_rate": 5,
        "speed_inc": 2.0,
        "bonus_threshold": 300,
        "bonus_duration": 5,
        "max_fps": 60,
        "curve_early_step": 20,
        "curve_mid_step": 40,
        "curve_late_step": 70
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

# F2: Dynamic Pacing — phase boundaries
CURVE_EARLY_LIMIT = 200
CURVE_MID_LIMIT = 500


def calculate_fps(score, level_config):
    """Calculate target FPS using piecewise curved progression."""
    base_fps = level_config["start_fps"]
    speed_inc = level_config["speed_inc"]
    max_fps = level_config["max_fps"]
    
    # Determine how many increments the score has earned
    increments = 0
    remaining = score
    
    # Early phase
    early_cap = CURVE_EARLY_LIMIT
    if remaining > 0:
        phase_inc = min(remaining, early_cap) // level_config["curve_early_step"]
        increments += phase_inc
        remaining -= early_cap
    
    # Mid phase
    if remaining > 0:
        mid_range = CURVE_MID_LIMIT - CURVE_EARLY_LIMIT
        phase_inc = min(remaining, mid_range) // level_config["curve_mid_step"]
        increments += phase_inc
        remaining -= mid_range
    
    # Late phase
    if remaining > 0:
        phase_inc = remaining // level_config["curve_late_step"]
        increments += phase_inc
    
    fps = base_fps + increments * speed_inc
    return min(fps, max_fps)

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
