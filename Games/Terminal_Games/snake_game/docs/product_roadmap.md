# Snake Game - Product Roadmap & Feature Specifications

This document outlines the planned enhancements to transition the Snake Game from a functional prototype to a polished, high-juice gaming experience.

---

## 1. Technical & Core Gameplay Improvements

### F1: Input Buffering & Command Queue
*   **Description**: Prevents "missed" inputs during high-speed play by queuing directional commands.
*   **Requirement**: Implement a queue (max size 2) that stores key presses. The game loop will process one command from the queue per tick, ensuring rapid "U-turns" (e.g., Up then Right) are registered even if pressed within the same frame.

### F2: Dynamic Pacing & Scaling
*   **Description**: Replaces the linear speed increase with a curved progression.
*   **Requirement**: Speed should increase aggressively in the early game to reach a "flow state" quickly, then plateau slightly at higher scores to test endurance rather than just raw reaction time.

### F3: Local JSON Profile & Analytics
*   **Description**: Replaces `highscore.txt` with a robust `save_data.json`.
*   **Requirement**: Track and save:
    *   Lifetime high score.
    *   Total games played.
    *   Total "Golden Food" consumed.
    *   Last selected difficulty and mode.

---

## 2. "Game Juice" (Visual & Audio Polish)

### F4: Screen Shake & Particle Bursts
*   **Description**: Adds physical feedback to game events.
*   **Requirement**: 
    *   Trigger a brief "Screen Shake" on collision (death) or when eating Bonus Food.
    *   Spawn a burst of color-matched particles at the food's location upon consumption.

### F5: Smoothed Movement (Interpolation)
*   **Description**: Moves the snake body smoothly between grid cells instead of "teleporting."
*   **Requirement**: Use a sub-pixel movement system where the snake's visual position is interpolated based on the time elapsed between frames.

### F6: Audio Engine Integration
*   **Description**: Adds immersive soundscapes and feedback.
*   **Requirement**:
    *   Implement a looping background track that subtly increases in pitch/tempo as speed increases.
    *   Add SFX for: Turn, Eat, Bonus Spawn, Bonus Eat, and Death.

---

## 3. New Content & Systems

### F7: In-Game Leveling System
*   **Description**: A progression system that unlocks new challenges during a single run.
*   **Requirement**: 
    *   Every X points, the player "Levels Up."
    *   Level Up effects: Visual board color shift, spawn of a temporary "Golden Food," or a short-lived power-up choice.

### F8: Shadow Obstacles (Level Hazards)
*   **Description**: Introduces environmental hazards with a warning phase and limited lifetime.
*   **Requirement**: After Level 3, there's a 40% chance to spawn 1-3 "Shadow" blocks. Shadows materialize after 3 seconds, flickering rapidly in the final 1 second. Once materialized, they last for 7 seconds before disappearing, flickering again in the final 1.5 seconds. Snakes can pass through shadows; if still inside during materialization, the snake remains "safe" until it exits. Re-entering a materialized wall is fatal.

### F9: Power-up System
*   **Description**: Temporary buffs that change gameplay dynamics.
*   **Requirement**: Occasionally spawn a "Blue Food" (Ghost) that allows tail-clipping for 5s, or a "Green Food" (Snail) that slows the game speed for 10s.

### F10: Cosmetic "Vibe" Themes
*   **Description**: Thematic skins for the snake and board.
*   **Requirement**: Allow the player to toggle between "Classic," "Cyberpunk (Neon)," and "Forest" themes in the menu, affecting colors and background styles.

---

## 4. UI/UX Refinement

### F11: Adaptive Board (Menu Streamlining)
*   **Description**: Automatically adjusts board size based on the chosen difficulty.
*   **Requirement**: Remove the standalone board size menu. 
    *   Base/Pro -> Small Board.
    *   Pro Max -> Medium Board.
    *   Ultra+ -> Large Board.

### F12: Visual Bonus Timer & Glow
*   **Description**: Enhances the feedback for Golden Bonus Food.
*   **Requirement**: The bonus food should pulsate (scale up/down) and have a glowing "halo" effect. The UI timer should turn red and shake when less than 2 seconds remain.
