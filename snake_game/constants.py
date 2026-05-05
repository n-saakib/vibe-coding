# Game Configuration Constants

# Window dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Grid settings
GRID_SIZE = 20
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
DIFFICULTY_STEP = 50 # Increase speed every 50 points

# Game Modes
MODE_WALL_COLLISION = "Standard"
MODE_WRAP_AROUND = "Wrap Around"

# Difficulty Levels
DIFFICULTY_LEVELS = {
    "Base": {
        "start_fps": 7,
        "growth_rate": 1,
        "speed_inc": 0.2
    },
    "Pro": {
        "start_fps": 10,
        "growth_rate": 1,
        "speed_inc": 0.5
    },
    "Pro Max": {
        "start_fps": 15,
        "growth_rate": 2,
        "speed_inc": 0.8
    },
    "Ultra Pro Max": {
        "start_fps": 20,
        "growth_rate": 3,
        "speed_inc": 1.2
    },
    "Ultra Pro Max +": {
        "start_fps": 25,
        "growth_rate": 5,
        "speed_inc": 2.0
    }
}

COLOR_BUTTON = (50, 50, 50)
COLOR_BUTTON_HOVER = (70, 70, 70)
