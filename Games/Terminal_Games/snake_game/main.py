import pygame
import sys
import os
import json
import random
import math
from constants import *
from snake_logic import Snake, Food, BonusFood, PowerUp, set_grid_dimensions

def load_save_data():
    """Load save data from JSON file, merging with defaults. Returns a dict."""
    save_data = dict(DEFAULT_SAVE_DATA)
    if os.path.exists(SAVE_DATA_PATH):
        try:
            with open(SAVE_DATA_PATH, "r") as f:
                loaded = json.load(f)
            # Merge loaded data into defaults (in case new fields were added)
            for key in DEFAULT_SAVE_DATA:
                if key in loaded:
                    save_data[key] = loaded[key]
        except (json.JSONDecodeError, ValueError):
            pass  # Corrupted file — use defaults
    
    # Migration: if highscore.txt exists and JSON high_score is 0, import it
    if save_data["high_score"] == 0 and os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                legacy_score = int(f.read().strip())
            save_data["high_score"] = legacy_score
            save_save_data(save_data)
        except (ValueError, OSError):
            pass
    
    return save_data

def save_save_data(save_data):
    """Write save data dict to JSON file."""
    try:
        with open(SAVE_DATA_PATH, "w") as f:
            json.dump(save_data, f, indent=4)
    except OSError:
        pass  # Silently fail if we can't write

class Button:
    def __init__(self, x, y, width, height, text, font, color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 2, border_radius=5)
        
        text_surf = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_up):
        return self.is_hovered and mouse_up

# Game States
STATE_MODE_SELECT = "MODE_SELECT"
STATE_LEVEL_SELECT = "LEVEL_SELECT"
STATE_THEME_SELECT = "THEME_SELECT"  # F10
STATE_START_SCREEN = "START_SCREEN"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAME_OVER = "GAME_OVER"

def main():
    # Global constants that need to be updated
    global SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT

    # Initialize Pygame modules selectively to avoid audio/ALSA errors
    pygame.display.init()
    pygame.font.init()
    
    # Start with initial window size
    window_width = INITIAL_WINDOW_WIDTH
    window_height = INITIAL_WINDOW_HEIGHT + UI_HEIGHT
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    large_font = pygame.font.SysFont("Arial", 48)

    # Load persistent save data
    save_data = load_save_data()

    # Game State Variables
    current_state = STATE_MODE_SELECT
    selected_size_name = "Medium" # Default for initial layout
    selected_mode = save_data.get("last_mode")
    selected_level = save_data.get("last_level")

    # Board pixel dimensions (SCREEN_WIDTH/HEIGHT renamed conceptually)
    board_width = SCREEN_WIDTH
    board_height = SCREEN_HEIGHT
    offset_x = 0
    offset_y = UI_HEIGHT

    # Initialize game objects
    snake = None
    food = None
    bonus_food = None
    power_up = None # F9
    obstacles = []  # F8: Static obstacle positions
    score = 0
    score_since_last_bonus = 0
    high_score = save_data["high_score"]
    fps = INITIAL_FPS
    game_over_processed = False  # Tracks if game-over logic ran
    level = 1  # F8: Track level for obstacle unlock gate
    # F4: Screen shake & particle state
    shake_timer = 0.0
    shake_intensity = 0
    particles = []
    # F5: Tick timing for interpolation
    last_tick_time = 0.0
    tick_accumulator = 0.0

    # UI Elements
    btn_width = 250
    mode_buttons = []
    level_buttons = []
    theme_buttons = []  # F10
    pause_buttons = []
    start_button = None
    selected_theme = "Classic"  # F10

    def update_layout():
        nonlocal window_width, window_height, board_width, board_height, offset_x, offset_y
        nonlocal mode_buttons, level_buttons, theme_buttons, pause_buttons, start_button

        # 1. Update board dimensions from selected size
        dim = SCREEN_SIZES.get(selected_size_name, 600)
        board_width = dim
        board_height = dim
        
        # 2. Enforce minimum window size
        min_w = max(board_width + WINDOW_MIN_BUFFER, MIN_UI_WIDTH)
        min_h = board_height + UI_HEIGHT + WINDOW_MIN_BUFFER
        
        if window_width < min_w or window_height < min_h:
            window_width = max(window_width, min_w)
            window_height = max(window_height, min_h)
            pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

        # 3. Calculate offsets
        offset_x = (window_width - board_width) // 2
        offset_y = UI_HEIGHT + (window_height - UI_HEIGHT - board_height) // 2

        # 4. Re-calculate button positions
        center_x = window_width // 2 - btn_width // 2
        y_start = window_height // 3

        mode_buttons = [
            Button(center_x, y_start, btn_width, 50, MODE_WALL_COLLISION, font),
            Button(center_x, y_start + 70, btn_width, 50, MODE_WRAP_AROUND, font)
        ]

        level_buttons = []
        for i, level_name in enumerate(DIFFICULTY_LEVELS.keys()):
            level_buttons.append(Button(center_x, window_height // 4 + i * 60, btn_width, 50, level_name, font))
        
        # F10: Theme selection buttons
        theme_buttons = []
        for i, theme_name in enumerate(THEMES.keys()):
            theme_buttons.append(Button(center_x, window_height // 4 + i * 60, btn_width, 50, theme_name, font))
        
        start_btn_w = int(window_width * 0.8)
        start_button = Button(window_width // 2 - start_btn_w // 2, window_height - 100, start_btn_w, 80, "START GAME", large_font)
        
        pause_buttons = [
            Button(center_x, window_height // 2 - 35, btn_width, 50, "RESUME", font),
            Button(center_x, window_height // 2 + 35, btn_width, 50, "QUIT TO MENU", font)
        ]

    # Initial layout call
    update_layout()

    # F4: Particle spawn helper
    def spawn_particles(screen_x, screen_y, color, count):
        nonlocal particles
        for _ in range(count):
            if len(particles) >= PARTICLE_MAX_TOTAL:
                break
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(PARTICLE_MIN_SPEED, PARTICLE_MAX_SPEED)
            life = random.uniform(0.2, PARTICLE_MAX_LIFE)
            particles.append({
                "x": screen_x, "y": screen_y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "color": color,
                "life": life,
                "max_life": life,
                "size": random.randint(2, 5)
            })

    # F8: Obstacle spawn helper
    def spawn_obstacles():
        nonlocal obstacles
        # 1. When a set of walls are already present, a new set should not appear
        if obstacles:
            return

        # 2. Only spawn sometimes (randomized)
        if random.random() > OBSTACLE_SPAWN_CHANCE:
            return

        # 3. Maximum walls mapping based on difficulty
        difficulty_max_map = {
            "Base": 1,
            "Pro": 2,
            "Pro Max": 3,
            "Ultra Pro Max": 4,
            "Ultra Pro Max +": 5
        }
        abs_max = difficulty_max_map.get(selected_level, 3)
        
        # Obstacle size scales with board (min 2x2 cells)
        obs_cells = max(OBSTACLE_MIN_CELLS, GRID_WIDTH // 20)
        
        # Scaling count based on level, but capped by difficulty-based max
        max_count = min(OBSTACLE_COUNT_MIN + (level // 3), abs_max)
        count = random.randint(OBSTACLE_COUNT_MIN, max_count)
        
        for _ in range(count):
            attempts = 0
            while attempts < 200:
                ox = random.randint(0, GRID_WIDTH - obs_cells)
                oy = random.randint(0, GRID_HEIGHT - obs_cells)
                block_cells = [(ox + dx, oy + dy) for dx in range(obs_cells) for dy in range(obs_cells)]
                
                overlap = False
                for cell in block_cells:
                    if cell == food.position:
                        overlap = True
                        break
                    if bonus_food.active and bonus_food.is_hit(cell):
                        overlap = True
                        break
                    # Obstacles can overlap other obstacles during shadow phase? 
                    # Let's keep them separate for now.
                    for obs in obstacles:
                        if cell in obs["cells"]:
                            overlap = True
                            break
                    if overlap: break
                
                if not overlap:
                    obstacles.append({
                        "cells": block_cells,
                        "state": "SHADOW",
                        "timer": OBSTACLE_SHADOW_DURATION,
                        "safe_segments": [] # Body segments currently overlapping
                    })
                    break
                attempts += 1

    while True:
        # F5: Time tracking for interpolation
        current_time = pygame.time.get_ticks() / 1000.0
        tick_duration = 1.0 / max(fps, 1) if fps > 0 else 1.0 / 7
        t = min(1.0, (current_time - last_tick_time) / tick_duration) if last_tick_time > 0 else 0.0
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_up = False

        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.w, event.h
                update_layout()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True
            
            if event.type == pygame.KEYDOWN:
                if current_state == STATE_PLAYING:
                    if event.key == pygame.K_UP:
                        snake.set_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.set_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.set_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.set_direction((1, 0))
                    elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        current_state = STATE_PAUSED
                elif current_state == STATE_PAUSED:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        current_state = STATE_PLAYING
                elif current_state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        current_state = STATE_MODE_SELECT
                        game_over_processed = False

        # 2. Update Logic
        if current_state == STATE_MODE_SELECT:
            for btn in mode_buttons:
                btn.update(mouse_pos)
                if btn.is_clicked(mouse_pos, mouse_up):
                    selected_mode = btn.text
                    save_data["last_mode"] = selected_mode
                    save_save_data(save_data)
                    current_state = STATE_LEVEL_SELECT
        
        elif current_state == STATE_LEVEL_SELECT:
            for btn in level_buttons:
                btn.update(mouse_pos)
                if btn.is_clicked(mouse_pos, mouse_up):
                    selected_level = btn.text
                    save_data["last_level"] = selected_level
                    save_save_data(save_data)
                    # Derive board size from difficulty (F11)
                    selected_size_name = DIFFICULTY_SIZE_MAP.get(selected_level, "Medium")
                    dim = SCREEN_SIZES[selected_size_name]
                    SCREEN_WIDTH = dim
                    SCREEN_HEIGHT = dim
                    GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
                    GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
                    set_grid_dimensions(GRID_WIDTH, GRID_HEIGHT)
                    update_layout()
                    current_state = STATE_THEME_SELECT  # F10
        
        elif current_state == STATE_THEME_SELECT:
            for btn in theme_buttons:
                btn.update(mouse_pos)
                if btn.is_clicked(mouse_pos, mouse_up):
                    selected_theme = btn.text
                    set_theme(selected_theme)
                    current_state = STATE_START_SCREEN
        
        elif current_state == STATE_START_SCREEN:
            start_button.update(mouse_pos)
            if start_button.is_clicked(mouse_pos, mouse_up):
                # Initialize Game
                snake = Snake()
                food = Food(snake.body)
                bonus_food = BonusFood(snake.body)
                bonus_food.active = False
                power_up = PowerUp(snake.body, [food.position, bonus_food])
                power_up.active = False
                score = 0
                score_since_last_bonus = 0
                high_score = save_data["high_score"]
                level_config = DIFFICULTY_LEVELS[selected_level]
                fps = level_config["start_fps"]
                obstacles = []  # F8: Reset obstacles
                level = 1       # F8: Reset level
                shake_timer = 0.0  # F4: Reset shake
                shake_intensity = 0
                particles = []     # F4: Reset particles
                last_tick_time = pygame.time.get_ticks() / 1000.0  # F5: Init tick timer
                current_state = STATE_PLAYING

        elif current_state == STATE_PLAYING:
            wrap_around = (selected_mode == MODE_WRAP_AROUND)
            wall_collision = (selected_mode == MODE_WALL_COLLISION)
            
            snake.process_queue()  # F1: Process one buffered input per tick
            snake.move(wrap_around=wrap_around)
            last_tick_time = current_time  # F5: Record tick time for interpolation
            
            # Check collision
            if snake.check_collision(wall_collision=wall_collision):
                current_state = STATE_GAME_OVER
                # F4: Death shake & particles
                head_screen_x = offset_x + snake.body[0][0] * GRID_SIZE + GRID_SIZE // 2
                head_screen_y = offset_y + snake.body[0][1] * GRID_SIZE + GRID_SIZE // 2
                spawn_particles(head_screen_x, head_screen_y, COLOR_FOOD, PARTICLE_COUNT_DEATH)
                shake_timer = SHAKE_DURATION_DEATH
                shake_intensity = SHAKE_INTENSITY_DEATH
            
            # F8: Update obstacles and check collision
            dt = 1.0 / max(fps, 1)

            # F9: Update power-up timers
            expired_powerups = []
            for pu_type in snake.active_powerups:
                snake.active_powerups[pu_type] -= dt
                if snake.active_powerups[pu_type] <= 0:
                    expired_powerups.append(pu_type)
            for pu_type in expired_powerups:
                del snake.active_powerups[pu_type]
            
            # F9: Power-up board expiration
            if power_up.active:
                power_up.timer -= dt
                if power_up.timer <= 0:
                    power_up.active = False

            for obs in obstacles[:]: # Use slice to allow removal
                obs["timer"] -= dt
                
                if obs["state"] == "SHADOW":
                    if obs["timer"] <= 0:
                        obs["state"] = "MATERIALIZED"
                        obs["timer"] = OBSTACLE_LIFETIME # Reset timer for materialized phase
                        # When it materializes, capture any segments currently in it as "safe"
                        obs["safe_segments"] = [seg for seg in snake.body if seg in obs["cells"]]
                
                elif obs["state"] == "MATERIALIZED":
                    if obs["timer"] <= 0:
                        obstacles.remove(obs)
                        continue
                        
                    # F9: Ghost mode allows passing through materialized obstacles
                    if POWERUP_TYPE_GHOST in snake.active_powerups:
                        continue

                    head = snake.body[0]
                    if head in obs["cells"]:
                        if head not in obs["safe_segments"]:
                            current_state = STATE_GAME_OVER
                            # F4: Death shake & particles
                            head_screen_x = offset_x + head[0] * GRID_SIZE + GRID_SIZE // 2
                            head_screen_y = offset_y + head[1] * GRID_SIZE + GRID_SIZE // 2
                            spawn_particles(head_screen_x, head_screen_y, COLOR_FOOD, PARTICLE_COUNT_DEATH)
                            shake_timer = SHAKE_DURATION_DEATH
                            shake_intensity = SHAKE_INTENSITY_DEATH
                    
                    # Update safe segments: remove any that are no longer in the wall
                    obs["safe_segments"] = [seg for seg in obs["safe_segments"] if seg in obs["cells"] and seg in snake.body]

            # Update timers
            if bonus_food.active:
                bonus_food.timer -= dt
                if bonus_food.timer <= 0:
                    bonus_food.active = False
            
            # Check food consumption
            level_config = DIFFICULTY_LEVELS[selected_level]
            if snake.body[0] == food.position:
                old_food_x, old_food_y = food.position  # F4: save before spawn moves it
                snake.grow(amount=level_config["growth_rate"])
                food.spawn(snake.body, bonus_food)
                score += SCORE_PER_FOOD
                score_since_last_bonus += SCORE_PER_FOOD
                
                # F4: Food eat particles at old position
                food_screen_x = offset_x + old_food_x * GRID_SIZE + GRID_SIZE // 2
                food_screen_y = offset_y + old_food_y * GRID_SIZE + GRID_SIZE // 2
                spawn_particles(food_screen_x, food_screen_y, COLOR_FOOD, PARTICLE_COUNT_FOOD)
                
                # F8: Update level and spawn/move obstacles
                level = score // LEVEL_SCORE_STEP + 1
                if level >= OBSTACLE_UNLOCK_LEVEL:
                    spawn_obstacles()
                
                # F9: Spawn power-up
                if not power_up.active and level >= 2: # Gate by level 2
                    if random.random() < POWERUP_SPAWN_CHANCE:
                        power_up.spawn(snake.body, [food.position, bonus_food])
                        power_up.timer = POWERUP_EXPIRE_TIME

                # Dynamic difficulty — curved progression (F2)
                fps = calculate_fps(score, level_config)

            # F9: Check power-up consumption
            if power_up.active and snake.body[0] == power_up.position:
                power_up.active = False
                pu_duration = POWERUP_DURATION_GHOST if power_up.type == POWERUP_TYPE_GHOST else POWERUP_DURATION_SNAIL
                snake.active_powerups[power_up.type] = pu_duration
                # Particles
                pu_color = COLOR_POWERUP_GHOST if power_up.type == POWERUP_TYPE_GHOST else COLOR_POWERUP_SNAIL
                pu_screen_x = offset_x + power_up.position[0] * GRID_SIZE + GRID_SIZE // 2
                pu_screen_y = offset_y + power_up.position[1] * GRID_SIZE + GRID_SIZE // 2
                spawn_particles(pu_screen_x, pu_screen_y, pu_color, PARTICLE_COUNT_FOOD)
                # Reset power_up type for next spawn
                power_up.type = random.choice([POWERUP_TYPE_GHOST, POWERUP_TYPE_SNAIL])

            # Check bonus food consumption (area collision)
            if bonus_food.active and bonus_food.is_hit(snake.body[0]):
                snake.grow(amount=level_config["growth_rate"] * 2) # Extra growth for bonus
                bonus_food.active = False
                score += SCORE_PER_FOOD * BONUS_SCORE_MULTIPLIER
                save_data["total_golden_food"] = save_data.get("total_golden_food", 0) + 1
                # F4: Bonus food particles & shake
                bonus_screen_x = offset_x + bonus_food.position[0] * GRID_SIZE + GRID_SIZE // 2
                bonus_screen_y = offset_y + bonus_food.position[1] * GRID_SIZE + GRID_SIZE // 2
                spawn_particles(bonus_screen_x, bonus_screen_y, COLOR_BONUS_FOOD, PARTICLE_COUNT_BONUS)
                shake_timer = max(shake_timer, SHAKE_DURATION_BONUS)
                shake_intensity = max(shake_intensity, SHAKE_INTENSITY_BONUS)

            # Spawn bonus food
            if not bonus_food.active and score_since_last_bonus >= level_config["bonus_threshold"]:
                bonus_food.spawn(snake.body, food.position)
                bonus_food.timer = level_config["bonus_duration"]
                score_since_last_bonus = 0
        
        elif current_state == STATE_PAUSED:
            for btn in pause_buttons:
                btn.update(mouse_pos)
                if btn.is_clicked(mouse_pos, mouse_up):
                    if btn.text == "RESUME":
                        current_state = STATE_PLAYING
                    elif btn.text == "QUIT TO MENU":
                        current_state = STATE_MODE_SELECT
                        game_over_processed = False
        
        elif current_state == STATE_GAME_OVER:
            if not game_over_processed:
                save_data["total_games"] = save_data.get("total_games", 0) + 1
                if score > save_data["high_score"]:
                    save_data["high_score"] = score
                    high_score = score
                save_save_data(save_data)
                game_over_processed = True

        # F4: Shake timer and particle updates (runs for all game-active states)
        if current_state in (STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER):
            # Use real delta time for visual effects
            frame_dt = 1.0 / 60.0 # Standard refresh rate
            if shake_timer > 0:
                shake_timer -= frame_dt
                if shake_timer <= 0:
                    shake_timer = 0.0
                    shake_intensity = 0
            
            for p in particles[:]:
                p["x"] += p["vx"] * frame_dt
                p["y"] += p["vy"] * frame_dt
                p["life"] -= frame_dt
                if p["life"] <= 0:
                    particles.remove(p)

        # 3. Rendering
        tm = get_theme()  # F10
        screen.fill(tm["background"])
        
        if current_state == STATE_MODE_SELECT:
            title = large_font.render("Select Game Mode", True, COLOR_TEXT)
            screen.blit(title, (window_width // 2 - title.get_width() // 2, window_height // 6))
            for btn in mode_buttons:
                btn.draw(screen)

        elif current_state == STATE_LEVEL_SELECT:
            title = large_font.render("Select Difficulty", True, COLOR_TEXT)
            screen.blit(title, (window_width // 2 - title.get_width() // 2, window_height // 10))
            for btn in level_buttons:
                btn.draw(screen)

        elif current_state == STATE_THEME_SELECT:
            title = large_font.render("Select Theme", True, COLOR_TEXT)
            screen.blit(title, (window_width // 2 - title.get_width() // 2, window_height // 10))
            for btn in theme_buttons:
                btn.draw(screen)

        elif current_state == STATE_START_SCREEN:
            title = large_font.render("Ready?", True, COLOR_TEXT)
            screen.blit(title, (window_width // 2 - title.get_width() // 2, window_height // 6))
            
            info_lines = [
                f"Size: {selected_size_name}",
                f"Mode: {selected_mode}",
                f"Level: {selected_level}"
            ]
            y_base = window_height // 3
            for i, line in enumerate(info_lines):
                info_surf = font.render(line, True, COLOR_SNAKE_HEAD)
                screen.blit(info_surf, (window_width // 2 - info_surf.get_width() // 2, y_base + i * 35))
            
            start_button.draw(screen)

        elif current_state == STATE_PLAYING or current_state == STATE_PAUSED or current_state == STATE_GAME_OVER:
            # F4: Compute shake offset
            shake_dx = 0
            shake_dy = 0
            if shake_timer > 0:
                intensity = shake_intensity * (shake_timer / max(SHAKE_DURATION_DEATH, SHAKE_DURATION_BONUS))
                shake_dx = random.randint(-int(intensity), int(intensity))
                shake_dy = random.randint(-int(intensity), int(intensity))
            render_ox = offset_x + shake_dx
            render_oy = offset_y + shake_dy

            # Draw Header Background
            pygame.draw.rect(screen, tm["ui_header"], (0, 0, window_width, UI_HEIGHT))
            pygame.draw.line(screen, tm["text"], (0, UI_HEIGHT), (window_width, UI_HEIGHT), 2)

            # Draw Playable Area Border
            pygame.draw.rect(screen, tm["board_bg"], (render_ox, render_oy, board_width, board_height))
            pygame.draw.rect(screen, tm["board_border"], (render_ox, render_oy, board_width, board_height), 1)

            # F10: Cyberpunk grid lines
            if tm["has_grid"] and tm["grid_color"] is not None:
                grid_surf = pygame.Surface((board_width, board_height), pygame.SRCALPHA)
                gc = tm["grid_color"]
                for gx in range(0, board_width, GRID_SIZE):
                    pygame.draw.line(grid_surf, gc, (gx, 0), (gx, board_height), 1)
                for gy in range(0, board_height, GRID_SIZE):
                    pygame.draw.line(grid_surf, gc, (0, gy), (board_width, gy), 1)
                screen.blit(grid_surf, (render_ox, render_oy))

            # F8: Draw obstacles
            for obs in obstacles:
                if obs["state"] == "SHADOW":
                    # Flickering effect: "Flicker twice" means 2 off-cycles
                    # Warn for 1.0s. 0.8-1.0 (OFF), 0.5-0.7 (OFF), others ON
                    if (0.75 < obs["timer"] <= 1.0) or (0.25 < obs["timer"] <= 0.5):
                        continue # OFF phase
                    color = OBSTACLE_SHADOW_COLOR
                else:
                    # Flickering effect when close to disappearing (< 1.5s)
                    # 1.1-1.4 (OFF), 0.4-0.7 (OFF)
                    if (1.1 < obs["timer"] <= 1.4) or (0.4 < obs["timer"] <= 0.7):
                        continue # OFF phase
                    color = OBSTACLE_COLOR

                for ox, oy in obs["cells"]:
                    obs_rect = pygame.Rect(render_ox + ox * GRID_SIZE,
                                           render_oy + oy * GRID_SIZE,
                                           GRID_SIZE, GRID_SIZE)
                    if obs["state"] == "MATERIALIZED":
                        pygame.draw.rect(screen, color, obs_rect)
                        # Draw X pattern for visibility
                        inset = 3
                        pygame.draw.line(screen, OBSTACLE_X_COLOR, 
                                         (obs_rect.left + inset, obs_rect.top + inset),
                                         (obs_rect.right - inset, obs_rect.bottom - inset), 2)
                        pygame.draw.line(screen, OBSTACLE_X_COLOR,
                                         (obs_rect.right - inset, obs_rect.top + inset),
                                         (obs_rect.left + inset, obs_rect.bottom - inset), 2)
                    else:
                        # Draw shadow (outline or semi-transparent)
                        # Note: SHADOW_COLOR has alpha, so we need a surface or use it directly if supported
                        if len(color) > 3: # Has alpha
                            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                            s.fill(color)
                            screen.blit(s, obs_rect)
                        else:
                            pygame.draw.rect(screen, color, obs_rect, 2)

            # Draw food
            food_rect = pygame.Rect(render_ox + food.position[0] * GRID_SIZE, 
                                    render_oy + food.position[1] * GRID_SIZE, 
                                    GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, tm["food"], food_rect)

            # F9: Draw power-up
            if power_up.active:
                # Flickering effect when < 3s remaining
                if power_up.timer < 3.0:
                    # OFF every 0.2s in the last 3s
                    if int(power_up.timer * 10) % 2 == 0:
                        pass 
                    else:
                        pu_rect = pygame.Rect(render_ox + power_up.position[0] * GRID_SIZE,
                                              render_oy + power_up.position[1] * GRID_SIZE,
                                              GRID_SIZE, GRID_SIZE)
                        pu_color = COLOR_POWERUP_GHOST if power_up.type == POWERUP_TYPE_GHOST else COLOR_POWERUP_SNAIL
                        pygame.draw.rect(screen, pu_color, pu_rect)
                        pygame.draw.rect(screen, tm["text"], pu_rect, 1)
                else:
                    pu_rect = pygame.Rect(render_ox + power_up.position[0] * GRID_SIZE,
                                          render_oy + power_up.position[1] * GRID_SIZE,
                                          GRID_SIZE, GRID_SIZE)
                    pu_color = COLOR_POWERUP_GHOST if power_up.type == POWERUP_TYPE_GHOST else COLOR_POWERUP_SNAIL
                    pygame.draw.rect(screen, pu_color, pu_rect)
                    pygame.draw.rect(screen, tm["text"], pu_rect, 1)

            # Draw bonus food (F12: pulse + glow)
            if bonus_food.active:
                base_size = GRID_SIZE * 3
                pulse = 1.0 + BONUS_PULSE_AMPLITUDE * math.sin(pygame.time.get_ticks() / 1000.0 * BONUS_PULSE_SPEED * 2 * math.pi)
                pulse_size = int(base_size * pulse)
                cx = render_ox + bonus_food.position[0] * GRID_SIZE + GRID_SIZE // 2
                cy = render_oy + bonus_food.position[1] * GRID_SIZE + GRID_SIZE // 2
                
                # Glow layers
                for layer in range(BONUS_GLOW_LAYERS, 0, -1):
                    alpha = max(0, 255 - BONUS_GLOW_ALPHA_STEP * layer)
                    glow_size = int(pulse_size + layer * 6)
                    glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                    glow_color = (*tm["bonus_food"], alpha)
                    glow_surf.fill(glow_color)
                    screen.blit(glow_surf, (cx - glow_size // 2, cy - glow_size // 2))
                
                bonus_rect = pygame.Rect(cx - pulse_size // 2, cy - pulse_size // 2,
                                         pulse_size, pulse_size)
                pygame.draw.rect(screen, tm["bonus_food"], bonus_rect, border_radius=5)
                pygame.draw.rect(screen, tm["text"], bonus_rect, 1, border_radius=5)
            
            # Draw snake (F5: interpolated positions)
            prev = snake.prev_body
            curr = snake.body
            wrap = (selected_mode == MODE_WRAP_AROUND) if selected_mode else False

            # F9: Visual feedback for active power-ups
            is_ghost = POWERUP_TYPE_GHOST in snake.active_powerups
            is_snail = POWERUP_TYPE_SNAIL in snake.active_powerups

            for i, segment in enumerate(curr):
                base_color = tm["snake_head"] if i == 0 else tm["snake_body"]
                # Apply power-up visual shifts
                if is_ghost:
                    color = (*COLOR_POWERUP_GHOST, 160) # RGBA
                elif is_snail:
                    color = (*COLOR_POWERUP_SNAIL, 255)
                else:
                    color = base_color

                # Get prev position (handle length mismatch)
                if i < len(prev):
                    px, py = prev[i]
                else:
                    px, py = segment  # New segment, no interpolation
                cx, cy = segment
                # Wrap-aware lerp
                dx = cx - px
                dy = cy - py
                if wrap:
                    if dx > GRID_WIDTH // 2:
                        px += GRID_WIDTH
                    elif dx < -GRID_WIDTH // 2:
                        px -= GRID_WIDTH
                    if dy > GRID_HEIGHT // 2:
                        py += GRID_HEIGHT
                    elif dy < -GRID_HEIGHT // 2:
                        py -= GRID_HEIGHT
                rx = (px + (cx - px) * t) * GRID_SIZE
                ry = (py + (cy - py) * t) * GRID_SIZE
                seg_rect = pygame.Rect(int(render_ox + rx), int(render_oy + ry),
                                       GRID_SIZE, GRID_SIZE)
                
                if len(color) > 3: # Has alpha
                    s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                    s.fill(color)
                    screen.blit(s, seg_rect)
                else:
                    pygame.draw.rect(screen, color, seg_rect)
                
                pygame.draw.rect(screen, tm["background"], seg_rect, 1)

            # F4: Draw particles
            for p in particles:
                alpha = int(255 * (p["life"] / p["max_life"]))
                if alpha <= 0:
                    continue
                pcolor = (*p["color"], alpha)
                psurf = pygame.Surface((p["size"], p["size"]), pygame.SRCALPHA)
                psurf.fill(pcolor)
                px = int(p["x"] + shake_dx - p["size"] // 2)
                py = int(p["y"] + shake_dy - p["size"] // 2)
                screen.blit(psurf, (px, py))

            # Draw UI
            score_surface = font.render(f"Score: {score}", True, tm["text"])
            high_score_surface = font.render(f"High Score: {high_score}", True, tm["text"])
            level_surface = font.render(f"Level: {selected_level}", True, tm["text"])
            
            screen.blit(score_surface, (10, 10))
            screen.blit(high_score_surface, (window_width - high_score_surface.get_width() - 10, 10))
            screen.blit(level_surface, (window_width // 2 - level_surface.get_width() // 2, 10))

            # Draw Bonus Timer (F12: urgent color + shake)
            if bonus_food.active:
                remaining = max(0, int(bonus_food.timer + 1))
                timer_text = f"BONUS: {remaining}s"
                is_urgent = bonus_food.timer <= BONUS_URGENT_THRESHOLD
                timer_color = COLOR_TIMER_URGENT if is_urgent else tm["timer"]
                timer_surf = font.render(timer_text, True, timer_color)
                tx = window_width // 2 - timer_surf.get_width() // 2
                ty = UI_HEIGHT - 35
                if is_urgent:
                    tx += random.randint(-BONUS_SHAKE_INTENSITY, BONUS_SHAKE_INTENSITY)
                    ty += random.randint(-BONUS_SHAKE_INTENSITY // 2, BONUS_SHAKE_INTENSITY // 2)
                screen.blit(timer_surf, (tx, ty))

            # F9: Draw active power-up timers
            pu_y = 10
            for pu_type, time_left in snake.active_powerups.items():
                pu_text = f"{pu_type.upper()}: {int(time_left + 1)}s"
                pu_color = COLOR_POWERUP_GHOST if pu_type == POWERUP_TYPE_GHOST else COLOR_POWERUP_SNAIL
                pu_surf = font.render(pu_text, True, pu_color)
                # Position them vertically below the level/bonus text or to the side
                screen.blit(pu_surf, (window_width // 2 - pu_surf.get_width() // 2, 40 + pu_y))
                pu_y += 25

            if current_state == STATE_PAUSED:
                overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))

                pause_surface = large_font.render("PAUSED", True, COLOR_TEXT)
                screen.blit(pause_surface, (window_width // 2 - pause_surface.get_width() // 2, window_height // 4))
                for btn in pause_buttons:
                    btn.draw(screen)

            if current_state == STATE_GAME_OVER:
                overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))

                over_surface = large_font.render("GAME OVER", True, tm["food"])
                restart_surface = font.render("Press R to Restart", True, tm["text"])
                final_score_surface = font.render(f"Final Score: {score}", True, tm["text"])
                
                mid_y = window_height // 2
                over_rect = over_surface.get_rect(center=(window_width // 2, mid_y - 40))
                final_rect = final_score_surface.get_rect(center=(window_width // 2, mid_y + 10))
                restart_rect = restart_surface.get_rect(center=(window_width // 2, mid_y + 60))
                
                screen.blit(over_surface, over_rect)
                screen.blit(final_score_surface, final_rect)
                screen.blit(restart_surface, restart_rect)

        pygame.display.flip()
        
        # F9: Apply snail speed reduction
        current_fps = fps
        if snake and POWERUP_TYPE_SNAIL in snake.active_powerups:
            current_fps *= SNAIL_SPEED_MULTIPLIER
        
        clock.tick(current_fps if current_state == STATE_PLAYING else 60)

if __name__ == "__main__":
    main()
