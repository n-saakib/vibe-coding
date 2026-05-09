# Architecture Documentation

## Overview
The Tic-Tac-Toe game follows the **Model-View-Controller (MVC)** architectural pattern to ensure separation of concerns and maintainability.

## Components

### 1. Model (`models/game_model.py`)
- **Responsibility:** Manages the game state and rules.
- **Key Data:**
    - 3x3 Grid (Board).
    - Current player (X or O).
    - Game status (Ongoing, Win, Draw).
- **Key Methods:**
    - `make_move(row, col)`
    - `check_winner()`
    - `reset_game()`

### 2. View (`views/game_view.py`)
- **Responsibility:** Handles the visual representation of the game using Pygame.
- **Key Data:**
    - Screen dimensions and colors.
    - Assets (X/O icons, fonts).
- **Key Methods:**
    - `draw_board()`
    - `draw_markers()`
    - `show_menu()`
    - `display_message()`

### 3. Controller (`controllers/game_controller.py`)
- **Responsibility:** Acts as the glue between Model and View. Processes user input.
- **Key Methods:**
    - `handle_events()`
    - `update_game_loop()`
    - `process_click(pos)`

## AI Implementation
- AI logic will be decoupled from the Controller to allow for different difficulty levels (Easy/Hard).
- The Controller will invoke the AI when it's the AI's turn.

## Data Flow
1. User interacts with the **View** (mouse click).
2. **Controller** receives the event and translates it to a board position.
3. **Controller** asks the **Model** to update the state.
4. **Model** validates and updates state, then checks for win/draw.
5. **Controller** tells the **View** to re-render based on the new state.
