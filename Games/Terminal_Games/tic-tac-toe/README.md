# Tic Tac Toe (Python + Pygame)

A modern, polished Tic Tac Toe game built with Python and Pygame, following the MVC (Model-View-Controller) architecture.

## Features
- **Local Multiplayer:** Play against a friend on the same computer.
- **Easy AI:** Play against a random-move AI.
- **Hard AI:** Challenge yourself against an unbeatable Minimax AI.
- **Scoreboard:** Tracks wins for Player X and Player O across sessions.
- **Winning Highlights:** Clearly shows the winning line.
- **Responsive Controls:** Switch modes or reset the game instantly.

## Architecture
- **Model:** Manages game state, logic, and scoring.
- **View:** Handles rendering with Pygame, including the grid, figures, and UI.
- **Controller:** Orchestrates user inputs and AI turns.

## Setup
1. Ensure you have Python 3.12+ installed.
2. The project uses a virtual environment (`venv`).
3. Install dependencies:
   ```bash
   ./venv/bin/pip install pygame pytest
   ```
4. Run the game:
   ```bash
   ./venv/bin/python main.py
   ```

## Controls
- **Mouse Click:** Place a marker (X or O).
- **R:** Reset the current board.
- **1:** Switch to Local Multiplayer (PvP).
- **2:** Switch to Single Player vs Easy AI.
- **3:** Switch to Single Player vs Hard AI (Minimax).

## Testing
Unit tests for the core logic are located in the `tests/` folder. Run them using:
```bash
PYTHONPATH=. ./venv/bin/pytest tests/
```
