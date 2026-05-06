# Snake Game Architecture

## Overview
A classic Snake game built with Python and Pygame. The game follows a simple grid-based movement system with dynamic difficulty and persistence.

## Components

### 1. `constants.py`
Contains all configuration values such as screen dimensions, grid size, colors, and initial game settings. It also defines:
- **`GAME_MODES`**: Defines the "Standard" and "Wrap Around" logic types.
- **`DIFFICULTY_LEVELS`**: A configuration dictionary that maps level names to their specific `start_fps`, `growth_rate`, and `speed_inc` values.

### 2. `snake_logic.py`
Encapsulates the core game entities:
- **`set_grid_dimensions(width, height)`**: A utility function that updates the global grid dimensions, allowing the game to scale across different screen sizes.
- **`Snake` Class**: 
    - Maintains a list of coordinates representing its body.
    - **`move(wrap_around)`**: Handles movement logic, with optional modulo arithmetic for wrapping around screen boundaries.
    - **`check_collision(wall_collision)`**: Checks for self-collision and, optionally, boundary collision.
    - **`growth_pool`**: An integer-based growth system allowing for multiple segments to be added incrementally over several moves.
- **`Food` Class**:
    - Manages its random position on the grid.
    - Ensures it doesn't spawn on the snake's body.
- **`BonusFood` Class**:
    - Inherits from `Food`.
    - **Area Collision**: Occupies a 3x3 grid area. `is_hit(head_pos)` checks if the snake's head enters any part of this 9-cell block.
    - **Timer**: Managed in the game loop; the bonus food disappears if the timer expires.

### 3. `main.py`
The entry point and orchestrator:
- **Initialization**: Sets up Pygame, the screen, and clock.
- **`Button` Class**: A simple UI helper for drawing interactive menu buttons.
- **State Machine**: Orchestrates the game flow through six distinct states:
    1. `STATE_SIZE_SELECT`: Choose the screen resolution (Small, Medium, Large).
    2. `STATE_MODE_SELECT`: Choose between Standard and Wrap Around.
    3. `STATE_LEVEL_SELECT`: Choose the difficulty level.
    4. `STATE_START_SCREEN`: Confirmation screen showing selected settings.
    5. `STATE_PLAYING`: The active game loop using the chosen configurations.
    6. `STATE_GAME_OVER`: Displays the final score and allows returning to the main menu.
- **Game Loop**:
    - **Input Handling**: Translates key presses and mouse clicks based on the current state.
    - **Update Logic**: Moves the snake, checks collisions, and handles score-based speed scaling.
    - **Rendering**: Draws state-specific UI or the game world.

## Data Flow
1. **Setup**: User selects Mode and Level via the UI buttons.
2. **Configuration**: Level-specific constants are loaded into the game state (initial FPS, growth rate).
3. **Input**: User presses an arrow key.
4. **Direction Update**: `main.py` updates the snake's direction.
5. **Movement**: `Snake.move()` updates coordinates, wrapping if enabled.
6. **Collision Check**: `main.py` checks if the head hit a wall (if enabled), self, or food.
7. **Score & Difficulty**: If food is eaten, snake grows by the level's `growth_rate`, score increases, and FPS scales by the level's `speed_inc`.
8. **Render**: The new state is drawn to the screen.

## Persistence
- High score is stored in `highscore.txt` as a single integer.
- Read on startup, updated on Game Over if the current score exceeds it.
