import pygame
import sys
import os
from constants import *
from snake_logic import Snake, Food, BonusFood, set_grid_dimensions

def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

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
STATE_SIZE_SELECT = "SIZE_SELECT"
STATE_MODE_SELECT = "MODE_SELECT"
STATE_LEVEL_SELECT = "LEVEL_SELECT"
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

    # Game State Variables
    current_state = STATE_SIZE_SELECT
    selected_size_name = "Medium" # Default for initial layout
    selected_mode = None
    selected_level = None

    # Board pixel dimensions (SCREEN_WIDTH/HEIGHT renamed conceptually)
    board_width = SCREEN_WIDTH
    board_height = SCREEN_HEIGHT
    offset_x = 0
    offset_y = UI_HEIGHT

    # Initialize game objects
    snake = None
    food = None
    bonus_food = None
    score = 0
    score_since_last_bonus = 0
    high_score = load_high_score()
    fps = INITIAL_FPS
    high_score_saved = False

    # UI Elements
    btn_width = 250
    size_buttons = []
    mode_buttons = []
    level_buttons = []
    pause_buttons = []
    start_button = None

    def update_layout():
        nonlocal window_width, window_height, board_width, board_height, offset_x, offset_y
        nonlocal size_buttons, mode_buttons, level_buttons, pause_buttons, start_button

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
        
        size_buttons = [
            Button(center_x, y_start, btn_width, 50, "Small", font),
            Button(center_x, y_start + 70, btn_width, 50, "Medium", font),
            Button(center_x, y_start + 140, btn_width, 50, "Large", font)
        ]

        mode_buttons = [
            Button(center_x, y_start, btn_width, 50, MODE_WALL_COLLISION, font),
            Button(center_x, y_start + 70, btn_width, 50, MODE_WRAP_AROUND, font)
        ]

        level_buttons = []
        for i, level_name in enumerate(DIFFICULTY_LEVELS.keys()):
            level_buttons.append(Button(center_x, window_height // 4 + i * 60, btn_width, 50, level_name, font))
        
        start_btn_w = int(window_width * 0.8)
        start_button = Button(window_width // 2 - start_btn_w // 2, window_height - 100, start_btn_w, 80, "START GAME", large_font)
        
        pause_buttons = [
            Button(center_x, window_height // 2 - 35, btn_width, 50, "RESUME", font),
            Button(center_x, window_height // 2 + 35, btn_width, 50, "QUIT TO MENU", font)
        ]

    # Initial layout call
    update_layout()

    while True:
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
                        current_state = STATE_SIZE_SELECT
                        high_score_saved = False

        # 2. Update Logic
        if current_state == STATE_SIZE_SELECT:
            for btn in size_buttons:
                btn.update(mouse_pos)
                if btn.is_clicked(mouse_pos, mouse_up):
                    selected_size_name = btn.text
                    dim = SCREEN_SIZES[selected_size_name]
                    SCREEN_WIDTH = dim
                    SCREEN_HEIGHT = dim
                    GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
                    GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
                    
                    # Update snake_logic grid dimensions
                    set_grid_dimensions(GRID_WIDTH, GRID_HEIGHT)
                    update_layout()
                    current_state = STATE_MODE_SELECT

        elif current_state == STATE_MODE_SELECT:
            for btn in mode_buttons:
                btn.update(mouse_pos)
                if btn.is_clicked(mouse_pos, mouse_up):
                    selected_mode = btn.text
                    current_state = STATE_LEVEL_SELECT
        
        elif current_state == STATE_LEVEL_SELECT:
            for btn in level_buttons:
                btn.update(mouse_pos)
                if btn.is_clicked(mouse_pos, mouse_up):
                    selected_level = btn.text
                    current_state = STATE_START_SCREEN
        
        elif current_state == STATE_START_SCREEN:
            start_button.update(mouse_pos)
            if start_button.is_clicked(mouse_pos, mouse_up):
                # Initialize Game
                snake = Snake()
                food = Food(snake.body)
                bonus_food = BonusFood(snake.body)
                bonus_food.active = False
                score = 0
                score_since_last_bonus = 0
                high_score = load_high_score()
                level_config = DIFFICULTY_LEVELS[selected_level]
                fps = level_config["start_fps"]
                current_state = STATE_PLAYING

        elif current_state == STATE_PLAYING:
            wrap_around = (selected_mode == MODE_WRAP_AROUND)
            wall_collision = (selected_mode == MODE_WALL_COLLISION)
            
            snake.move(wrap_around=wrap_around)
            
            # Check collision
            if snake.check_collision(wall_collision=wall_collision):
                current_state = STATE_GAME_OVER
            
            # Update timers
            if bonus_food.active:
                bonus_food.timer -= 1/fps
                if bonus_food.timer <= 0:
                    bonus_food.active = False
            
            # Check food consumption
            level_config = DIFFICULTY_LEVELS[selected_level]
            if snake.body[0] == food.position:
                snake.grow(amount=level_config["growth_rate"])
                food.spawn(snake.body, bonus_food.position if bonus_food.active else None)
                score += SCORE_PER_FOOD
                score_since_last_bonus += SCORE_PER_FOOD
                
                # Dynamic difficulty
                if score % DIFFICULTY_STEP == 0:
                    fps += level_config["speed_inc"]

            # Check bonus food consumption (area collision)
            if bonus_food.active and bonus_food.is_hit(snake.body[0]):
                snake.grow(amount=level_config["growth_rate"] * 2) # Extra growth for bonus
                bonus_food.active = False
                score += SCORE_PER_FOOD * BONUS_SCORE_MULTIPLIER

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
                        high_score_saved = False
        
        elif current_state == STATE_GAME_OVER:
            if not high_score_saved:
                if score > high_score:
                    save_high_score(score)
                    high_score = score
                high_score_saved = True

        # 3. Rendering
        screen.fill(COLOR_BACKGROUND)
        
        if current_state == STATE_SIZE_SELECT:
            title = large_font.render("Select Screen Size", True, COLOR_TEXT)
            screen.blit(title, (window_width // 2 - title.get_width() // 2, window_height // 6))
            for btn in size_buttons:
                btn.draw(screen)

        elif current_state == STATE_MODE_SELECT:
            title = large_font.render("Select Game Mode", True, COLOR_TEXT)
            screen.blit(title, (window_width // 2 - title.get_width() // 2, window_height // 6))
            for btn in mode_buttons:
                btn.draw(screen)

        elif current_state == STATE_LEVEL_SELECT:
            title = large_font.render("Select Difficulty", True, COLOR_TEXT)
            screen.blit(title, (window_width // 2 - title.get_width() // 2, window_height // 10))
            for btn in level_buttons:
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
            # Draw Header Background
            pygame.draw.rect(screen, (50, 50, 50), (0, 0, window_width, UI_HEIGHT))
            pygame.draw.line(screen, COLOR_TEXT, (0, UI_HEIGHT), (window_width, UI_HEIGHT), 2)

            # Draw Playable Area Border
            pygame.draw.rect(screen, (40, 40, 40), (offset_x, offset_y, board_width, board_height))
            pygame.draw.rect(screen, (100, 100, 100), (offset_x, offset_y, board_width, board_height), 1)

            # Draw food
            food_rect = pygame.Rect(offset_x + food.position[0] * GRID_SIZE, 
                                    offset_y + food.position[1] * GRID_SIZE, 
                                    GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, COLOR_FOOD, food_rect)

            # Draw bonus food
            if bonus_food.active:
                bonus_rect = pygame.Rect(offset_x + (bonus_food.position[0] - 1) * GRID_SIZE, 
                                         offset_y + (bonus_food.position[1] - 1) * GRID_SIZE, 
                                         GRID_SIZE * 3, GRID_SIZE * 3)
                pygame.draw.rect(screen, COLOR_BONUS_FOOD, bonus_rect, border_radius=5)
                pygame.draw.rect(screen, COLOR_TEXT, bonus_rect, 1, border_radius=5)
            
            # Draw snake
            for i, segment in enumerate(snake.body):
                color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
                seg_rect = pygame.Rect(offset_x + segment[0] * GRID_SIZE, 
                                       offset_y + segment[1] * GRID_SIZE, 
                                       GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, color, seg_rect)
                pygame.draw.rect(screen, COLOR_BACKGROUND, seg_rect, 1)

            # Draw UI
            score_surface = font.render(f"Score: {score}", True, COLOR_TEXT)
            high_score_surface = font.render(f"High Score: {high_score}", True, COLOR_TEXT)
            level_surface = font.render(f"Level: {selected_level}", True, COLOR_TEXT)
            
            screen.blit(score_surface, (10, 10))
            screen.blit(high_score_surface, (window_width - high_score_surface.get_width() - 10, 10))
            screen.blit(level_surface, (window_width // 2 - level_surface.get_width() // 2, 10))

            # Draw Bonus Timer
            if bonus_food.active:
                timer_text = f"BONUS: {max(0, int(bonus_food.timer + 1))}s"
                timer_surf = font.render(timer_text, True, COLOR_TIMER)
                screen.blit(timer_surf, (window_width // 2 - timer_surf.get_width() // 2, UI_HEIGHT - 35))

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

                over_surface = large_font.render("GAME OVER", True, COLOR_FOOD)
                restart_surface = font.render("Press R to Restart", True, COLOR_TEXT)
                final_score_surface = font.render(f"Final Score: {score}", True, COLOR_TEXT)
                
                mid_y = window_height // 2
                over_rect = over_surface.get_rect(center=(window_width // 2, mid_y - 40))
                final_rect = final_score_surface.get_rect(center=(window_width // 2, mid_y + 10))
                restart_rect = restart_surface.get_rect(center=(window_width // 2, mid_y + 60))
                
                screen.blit(over_surface, over_rect)
                screen.blit(final_score_surface, final_rect)
                screen.blit(restart_surface, restart_rect)

        pygame.display.flip()
        clock.tick(fps if current_state == STATE_PLAYING else 60)

if __name__ == "__main__":
    main()
