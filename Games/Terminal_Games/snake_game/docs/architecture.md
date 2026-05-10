# Snake Game Architecture (Combined Build)

## Overview
A classic Snake game built with Python and Pygame, featuring input buffering, dynamic difficulty pacing, JSON persistence, screen shake & particle effects, smoothed movement interpolation, cosmetic themes, adaptive board sizing, static obstacles, and animated bonus food.

## Files

### `constants.py`
All configuration: window/screen sizes, colors, difficulty levels, game modes, theme presets (Classic/Cyberpunk/Forest), obstacle/power-up config, shake/particle config, bonus food animation config, and save data defaults.

### `snake_logic.py`
Core entities:
- **`Snake`**: Body list, direction, `command_queue` (input buffering, max 2), `process_queue()`, `prev_body` (for interpolation), `growth_pool`, collision with optional ghost mode.
- **`Food`**: Random position, spawn avoidance (now explicitly avoids the 3x3 `BonusFood` area).
- **`BonusFood`**: 3x3 area collision (robust absolute-distance check), timer.
- **`PowerUp`**: Inherits from `Food`. Spawns "Ghost" (Blue) or "Snail" (Green) items. Ghost allows self-collision for 5s; Snail slows speed by 40% for 10s.

### `audio.py` (F6 branch only, not in combined)
Procedural sound generation — not included in combined build.

### `main.py`
Entry point and orchestrator:
- **State Machine** (8 states): Mode Select → Level Select → Theme Select → Start Screen → Playing → Paused → Game Over. Board size auto-derived from difficulty (F11).
- **Input Buffering (F1)**: Arrow keys enqueue to `command_queue`; one command processed per tick.
- **Dynamic Pacing (F2)**: `calculate_fps()` — piecewise curved speed progression with per-difficulty max FPS caps.
- **JSON Persistence (F3)**: `save_data.json` for high score, total games, golden food count, last mode/level.
- **Screen Shake & Particles (F4)**: Shake on death/bonus eat; particle bursts on food eat with alpha fading.
- **Smoothed Movement (F5)**: `prev_body` tracking + wrap-aware lerp interpolation for sub-pixel rendering.
- **Shadow Obstacles (F8)**: Multi-cell blocks (2×2 to 4×4) spawn with 40% chance after level 3. Features a 3s "Shadow" phase (safe to enter) with flicker warning, followed by materialization with safety windows for overlapping segments.
- **Cosmetic Themes (F10)**: Classic/Cyberpunk/Forest themes. Cyberpunk has grid lines. Theme select in menu.
- **Bonus Food Animation (F12)**: Pulsating scale + 3-layer glow halo. Timer turns red and shakes when < 2s.

## Data Flow
1. User selects Mode → Level → Theme via buttons.
2. Board size auto-derived from difficulty (`DIFFICULTY_SIZE_MAP`).
3. Game loop: input → process queue → move (prev_body saved) → collision checks (walls, self, obstacles) → food/bonus/power-up consumption → speed curve recalculation → shake/particle updates → render with interpolation + shake offset + theme colors.
4. Game over: save stats to JSON, shake+particle effects decay naturally.

## Persistence
- `save_data.json`: `high_score`, `total_games`, `total_golden_food`, `last_mode`, `last_level`.
- Migration from legacy `highscore.txt` on first run.
