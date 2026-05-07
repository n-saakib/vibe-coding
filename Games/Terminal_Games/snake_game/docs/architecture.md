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
- **Initialization**: Sets up Pygame with a resizable window (`pygame.RESIZABLE`).
- **`Button` Class**: A UI helper that is dynamically repositioned when the window is resized.
- **Layout Management**:
    - **`update_layout()`**: A central function that calculates board dimensions, enforces minimum window sizes (with buffers), and centers the board within the window using `offset_x` and `offset_y`.
- **State Machine**: Orchestrates the game flow. Selecting a size now updates the board's grid but keeps the window stable unless it's too small for the new board.
- **Game Loop**:
    - **Input Handling**: Handles `VIDEORESIZE` events to maintain layout integrity.
    - **Rendering**: Uses `offset_x` and `offset_y` to center all game objects (Snake, Food, Bonus Food) within the window. Draws a visual border to define the playable area.

## Sizing and Scaling
- **Window Size**: Decoupled from the game board. The window can be manually resized, but it will always stay larger than the board plus a `WINDOW_MIN_BUFFER`.
- **UI Constraints**: A `MIN_UI_WIDTH` ensures that header text (Score, High Score, Level) never overlaps.
- **Board Centering**: The board is dynamically centered in the space below the fixed-height UI header.

## Persistence
- High score is stored in `highscore.txt` as a single integer.
- Read on startup, updated on Game Over if the current score exceeds it.
