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

# F8: Static Obstacles
LEVEL_SCORE_STEP = 100  # Points per level
OBSTACLE_COLOR = (200, 55, 55)  # Bright brick-red, visible on dark bg
OBSTACLE_SHADOW_COLOR = (100, 30, 30, 150) # Semi-transparent dark red
OBSTACLE_X_COLOR = (255, 255, 255)  # White X pattern for contrast
OBSTACLE_COUNT_MIN = 1
OBSTACLE_COUNT_MAX = 3
OBSTACLE_UNLOCK_LEVEL = 3
OBSTACLE_MIN_CELLS = 2  # Minimum obstacle width/height in grid cells
OBSTACLE_SHADOW_DURATION = 3.0 # seconds
OBSTACLE_LIFETIME = 7.0 # seconds (how long it stays materialized)
OBSTACLE_SPAWN_CHANCE = 0.4 # 40% chance after eating food

# F4: Screen Shake & Particles
SHAKE_INTENSITY_DEATH = 10
SHAKE_DURATION_DEATH = 6.0 # restored
SHAKE_INTENSITY_BONUS = 12 
SHAKE_DURATION_BONUS = 0.15 # decreased more than half (was 0.4)
PARTICLE_COUNT_FOOD = 15
PARTICLE_COUNT_BONUS = 60 # Increased for impact
PARTICLE_COUNT_DEATH = 25
PARTICLE_MAX_TOTAL = 200
PARTICLE_MAX_LIFE = 0.6
PARTICLE_MIN_SPEED = 30
PARTICLE_MAX_SPEED = 120

COLOR_BUTTON = (50, 50, 50)
COLOR_BUTTON_HOVER = (70, 70, 70)
COLOR_BONUS_FOOD = (255, 215, 0) # Gold
COLOR_TIMER = (255, 100, 100) # Red-ish

# F9: Power-ups
POWERUP_TYPE_GHOST = "Ghost"
POWERUP_TYPE_SNAIL = "Snail"
COLOR_POWERUP_GHOST = (0, 191, 255) # Deep Sky Blue
COLOR_POWERUP_SNAIL = (50, 205, 50)  # Lime Green
POWERUP_DURATION_GHOST = 5.0 # seconds
POWERUP_DURATION_SNAIL = 10.0 # seconds
POWERUP_EXPIRE_TIME = 10.0 # seconds (how long it stays on board)
POWERUP_SPAWN_CHANCE = 0.15 # 15% chance to spawn after level 2
SNAIL_SPEED_MULTIPLIER = 0.6 # 60% of current speed

# F12: Bonus Food Visual Enhancements
BONUS_PULSE_SPEED = 4.0
BONUS_PULSE_AMPLITUDE = 0.15
BONUS_GLOW_LAYERS = 3
BONUS_GLOW_ALPHA_STEP = 60
BONUS_URGENT_THRESHOLD = 2.0
BONUS_SHAKE_INTENSITY = 3
COLOR_TIMER_URGENT = (255, 50, 50)

# F10: Cosmetic Themes
THEMES = {
    "Classic": {
        "background": (30, 30, 30),
        "snake_head": (0, 255, 100),
        "snake_body": (0, 200, 80),
        "food": (255, 50, 50),
        "bonus_food": (255, 215, 0),
        "text": (255, 255, 255),
        "button": (50, 50, 50),
        "button_hover": (70, 70, 70),
        "board_bg": (40, 40, 40),
        "board_border": (100, 100, 100),
        "ui_header": (50, 50, 50),
        "timer": (255, 100, 100),
        "has_grid": False,
        "grid_color": None
    },
    "Cyberpunk": {
        "background": (10, 5, 25),
        "snake_head": (0, 255, 255),
        "snake_body": (255, 0, 255),
        "food": (255, 255, 0),
        "bonus_food": (0, 255, 255),
        "text": (0, 255, 200),
        "button": (20, 10, 40),
        "button_hover": (40, 20, 80),
        "board_bg": (15, 8, 35),
        "board_border": (0, 255, 255),
        "ui_header": (15, 5, 30),
        "timer": (255, 50, 255),
        "has_grid": True,
        "grid_color": (0, 255, 255, 30)
    },
    "Forest": {
        "background": (20, 40, 20),
        "snake_head": (100, 200, 50),
        "snake_body": (60, 150, 30),
        "food": (200, 100, 50),
        "bonus_food": (255, 200, 100),
        "text": (200, 220, 180),
        "button": (30, 50, 30),
        "button_hover": (50, 70, 50),
        "board_bg": (25, 45, 25),
        "board_border": (80, 120, 60),
        "ui_header": (25, 35, 25),
        "timer": (255, 150, 100),
        "has_grid": False,
        "grid_color": None
    }
}

_current_theme_name = "Classic"
_current_theme = THEMES["Classic"]


def set_theme(name):
    global _current_theme_name, _current_theme
    _current_theme_name = name
    _current_theme = THEMES.get(name, THEMES["Classic"])


def get_theme():
    return _current_theme

# Save Data
SAVE_DATA_PATH = "save_data.json"
DEFAULT_SAVE_DATA = {
    "high_score": 0,
    "total_games": 0,
    "total_golden_food": 0,
    "last_mode": None,
    "last_level": None
}
