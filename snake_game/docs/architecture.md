# Snake Game Architecture

## Overview
A classic Snake game built with Python and Pygame. The game follows a simple grid-based movement system with dynamic difficulty and persistence.

## Components

### 1. `constants.py`
Contains all configuration values such as screen dimensions, grid size, colors, and initial game settings. Centralizing these allows for easy balancing and UI adjustments.

### 2. `snake_logic.py`
Encapsulates the core game entities:
- **`Snake` Class**: 
    - Maintains a list of coordinates representing its body.
    - Handles movement logic (appending new head, popping tail).
    - Checks for self-collision and boundary collision.
    - Manages growth state.
- **`Food` Class**:
    - Manages its random position on the grid.
    - Ensures it doesn't spawn on the snake's body.

### 3. `main.py`
The entry point and orchestrator:
- **Initialization**: Sets up Pygame, the screen, and clock.
- **Game Loop**:
    - **Input Handling**: Translates key presses into direction changes.
    - **Update Logic**: Moves the snake, checks collisions, handles food consumption.
    - **Rendering**: Draws the background, snake, food, and UI elements (score).
- **State Management**: Handles the transition between "Playing", "Game Over", and "Restarting".

## Data Flow
1. **Input**: User presses an arrow key.
2. **Direction Update**: `main.py` updates the snake's direction.
3. **Movement**: `Snake.move()` updates coordinates.
4. **Collision Check**: `main.py` checks if the head hit a wall, self, or food.
5. **Score & Difficulty**: If food is eaten, score increases, and FPS may increase.
6. **Render**: The new state is drawn to the screen.

## Persistence
- High score is stored in `highscore.txt` as a single integer.
- Read on startup, updated on Game Over if the current score exceeds it.
