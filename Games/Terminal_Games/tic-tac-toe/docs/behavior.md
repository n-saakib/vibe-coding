# Behavior Documentation

## User Flows

### 1. Main Menu
- The user is presented with options:
    - **Local Multiplayer:** Play against another person on the same machine.
    - **Single Player (Easy AI):** Play against a random-move AI.
    - **Single Player (Hard AI):** Play against an unbeatable Minimax AI.
    - **Quit:** Exit the game.

### 2. Game Session
- **Turn Order:** X always goes first.
- **Making a Move:** User clicks on an empty cell.
- **Visual Feedback:** 
    - Hovering over a cell might highlight it (Optional/Polish).
    - Placing a marker plays a sound or shows an animation (Optional/Polish).
- **Winning:** When 3 identical markers align (row, col, diag), the winning line is highlighted, and a victory message appears.
- **Draw:** If all cells are filled and no one wins, a "Draw" message appears.

### 3. Post-Game
- Options:
    - **Play Again:** Resets the board but keeps the same mode and scores.
    - **Back to Menu:** Returns to the main menu.

## State Transitions
1. `MENU` -> `PLAYING` (Mode selected)
2. `PLAYING` -> `GAME_OVER` (Win or Draw detected)
3. `GAME_OVER` -> `PLAYING` (Play Again selected)
4. `GAME_OVER` -> `MENU` (Back to Menu selected)

## AI Behavior
- **Easy AI:** 
    - Waits for a small delay (0.5s) to feel natural.
    - Picks a random available spot on the board.
- **Hard AI:**
    - Uses Minimax algorithm to find the optimal move.
    - Prioritizes winning, then blocking player wins, then controlling the center/corners.
