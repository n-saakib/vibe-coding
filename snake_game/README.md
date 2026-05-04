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

# Run the game
python main.py
```

### 3. Controls
- **Arrow Keys**: Change direction (Up, Down, Left, Right).
- **R Key**: Restart the game when in the Game Over state.

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
