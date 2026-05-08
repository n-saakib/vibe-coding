# Python Snake Game (Pygame)

A classic, polished Snake game built with Python and the Pygame library. Features include dynamic difficulty, persistent high scores, and a clean, modular architecture.

## How to Run the Game

### 1. Prerequisites
Ensure you have Python 3.12+ installed on your system.

### 2. Setup & Execution
The project comes with a pre-configured virtual environment (if you are on the same machine) and a `requirements.txt` file.

```bash
# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### 3. Controls
- **Mouse**: Select game mode and difficulty level in the menus.
- **Arrow Keys**: Change direction (Up, Down, Left, Right).
- **P / ESC Key**: Pause or Resume the game.
- **R Key**: Return to the main menu when in the Game Over state.

## Gameplay & Events

The game follows a structured sequence of events to get you started:

1.  **Size Selection**: Choose your preferred game board size: **Small** (40x40 grid), **Medium** (60x60 grid), or **Large** (80x80 grid). The window is resizable and will automatically center the game board within the playable area.
2.  **Mode Selection**: Choose between **Standard** (wall collision) or **Wrap Around** (no wall deaths).
3.  **Start Screen**: A final confirmation screen displays your chosen settings. Click **START GAME** to begin.
4.  **The Game Loop**:
    - **Movement**: The snake moves constantly in the current direction.
    - **Eating**: Consuming food increases your score and triggers the **Growth Event**. Standard food intelligently avoids spawning on top of active bonus food areas.
    - **Bonus Food**: After reaching a level-specific score threshold, a **3x3 Golden Bonus Food** appears for a limited time. Eating it gives **5x points** and double the normal growth. Hit detection is robust across all 9 cells. A countdown timer will appear at the top when it's active.
    - **Shadow Obstacles**: After Level 3, hazards appear. They start as "Shadows" (semi-transparent) for 3 seconds. The snake can pass through shadows. If the snake is inside a shadow when it materializes, it remains safe until it exits the wall. However, entering a materialized wall from the outside is fatal. Shadows flicker rapidly as they are about to materialize.
    - **Growth**: The snake grows by a specific number of segments based on your chosen difficulty level.
    - **Speeding Up**: Every 50 points, a **Difficulty Event** occurs, increasing the game speed.
5.  **Game Over**: If you collide with yourself (or a wall in Standard mode), the game ends. Your high score is saved locally.

## Game Features

### Game Modes
- **Standard**: The classic experience. Hitting a wall ends the game.
- **Wrap Around**: The snake wraps to the opposite side of the screen when it hits an edge.

### Difficulty Levels
There are 5 levels of difficulty, each affecting starting speed, how fast the snake grows, and how quickly the speed increases:
- **Base**: 7 FPS, 1 segment/food, 0.2 speed increase.
- **Pro**: 10 FPS, 1 segment/food, 0.5 speed increase.
- **Pro Max**: 15 FPS, 2 segments/food, 0.8 speed increase.
- **Ultra Pro Max**: 20 FPS, 3 segments/food, 1.2 speed increase.
- **Ultra Pro Max +**: 25 FPS, 5 segments/food, 2.0 speed increase.

## Documentation Guide
For a deeper dive into the technical details:
- **[docs/architecture.md](docs/architecture.md)**: Explains the class structure, data flow, and how the game loop is orchestrated.
- **constants.py**: Contains all adjustable game parameters (colors, speed, grid size).

## Project Summary (The Prompt)
I was tasked with creating a fully functional Snake game in Python. The requirements evolved from a general feature list to a specific implementation using **Pygame**. Key constraints included:
- Creating a modular architecture.
- Implementing dynamic difficulty (speed increase).
- Adding high score persistence.
- Setting up a Python virtual environment (`venv`).
- Maintaining a clean Git history with specific commit message styles (no prefixes).

## How It Was Built
I followed a structured development lifecycle to ensure a robust and maintainable final product:

1.  **Research & Planning**: I first identified the core mechanics and UI requirements. I then drafted a detailed implementation plan in Plan Mode, which served as our roadmap.
2.  **Architecture Design**: I created a `docs/architecture.md` file early on to map out how the `Snake` and `Food` logic would interact with the main Pygame engine.
3.  **Environment Setup**: I initialized a virtual environment, installed dependencies, and centralized all game settings in `constants.py`.
4.  **Iterative Implementation**:
    - **Logic First**: Implemented the `Snake` and `Food` classes in `snake_logic.py` with rigorous collision and growth logic.
    - **Engine Integration**: Built the main loop in `main.py`, integrating input handling and rendering.
    - **Features & UI**: Added scoring, persistence, and a polished Game Over screen.
5.  **Validation**: Performed final checks on movement accuracy, collision reliability, and data persistence.
6.  **Version Control**: Used Git at each major milestone to provide a clear and traceable development history.
