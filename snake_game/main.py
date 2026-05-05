import pygame
import sys
import os
from constants import *
from snake_logic import Snake, Food

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
STATE_MODE_SELECT = "MODE_SELECT"
STATE_LEVEL_SELECT = "LEVEL_SELECT"
STATE_START_SCREEN = "START_SCREEN"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAME_OVER = "GAME_OVER"

def main():
    # Initialize Pygame modules selectively to avoid audio/ALSA errors
    pygame.display.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + UI_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    large_font = pygame.font.SysFont("Arial", 48)

    # Game State Variables
    current_state = STATE_MODE_SELECT
    selected_mode = None
    selected_level = None
    
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
    btn_width = 300
    center_x = SCREEN_WIDTH // 2 - btn_width // 2
    
    mode_buttons = [
        Button(center_x, 200, btn_width, 50, MODE_WALL_COLLISION, font),
        Button(center_x, 270, btn_width, 50, MODE_WRAP_AROUND, font)
    ]
    
    level_buttons = []
    for i, level_name in enumerate(DIFFICULTY_LEVELS.keys()):
        level_buttons.append(Button(center_x, 150 + i * 60, btn_width, 50, level_name, font))
    
    start_btn_width = 400
    start_button = Button(SCREEN_WIDTH // 2 - start_btn_width // 2, 350, start_btn_width, 80, "START GAME", large_font)
    
    pause_buttons = [
        Button(center_x, 300, btn_width, 50, "RESUME", font),
        Button(center_x, 370, btn_width, 50, "QUIT TO MENU", font)
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_up = False

        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
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
                        high_score_saved = False

        # 2. Update Logic
        if current_state == STATE_MODE_SELECT:
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

            # Check bonus food consumption
            if bonus_food.active and snake.body[0] == bonus_food.position:
                snake.grow(amount=level_config["growth_rate"] * 2) # Extra growth for bonus
                bonus_food.active = False
                score += SCORE_PER_FOOD * BONUS_SCORE_MULTIPLIER
                # Speed boost from bonus? Maybe too much. Let's stick to points and growth.

            # Spawn bonus food
            if not bonus_food.active and score_since_last_bonus >= level_config["bonus_threshold"]:
                bonus_food.spawn(snake.body, food.position)
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
        
        if current_state == STATE_MODE_SELECT:
            title = large_font.render("Select Game Mode", True, COLOR_TEXT)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            for btn in mode_buttons:
                btn.draw(screen)

        elif current_state == STATE_LEVEL_SELECT:
            title = large_font.render("Select Difficulty", True, COLOR_TEXT)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
            for btn in level_buttons:
                btn.draw(screen)

        elif current_state == STATE_START_SCREEN:
            title = large_font.render("Ready?", True, COLOR_TEXT)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
            info = font.render(f"Mode: {selected_mode} | Level: {selected_level}", True, COLOR_SNAKE_HEAD)
            screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, 220))
            start_button.draw(screen)

        elif current_state == STATE_PLAYING or current_state == STATE_PAUSED or current_state == STATE_GAME_OVER:
            # Draw Header Background
            pygame.draw.rect(screen, (50, 50, 50), (0, 0, SCREEN_WIDTH, UI_HEIGHT))
            pygame.draw.line(screen, COLOR_TEXT, (0, UI_HEIGHT), (SCREEN_WIDTH, UI_HEIGHT), 2)

            # Draw food
            food_rect = pygame.Rect(food.position[0] * GRID_SIZE, 
                                    food.position[1] * GRID_SIZE + UI_HEIGHT, 
                                    GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, COLOR_FOOD, food_rect)

            # Draw bonus food
            if bonus_food.active:
                # Bonus food is 2x2 grid size (centered on its grid position)
                bonus_rect = pygame.Rect(bonus_food.position[0] * GRID_SIZE - GRID_SIZE // 2, 
                                         bonus_food.position[1] * GRID_SIZE + UI_HEIGHT - GRID_SIZE // 2, 
                                         GRID_SIZE * 2, GRID_SIZE * 2)
                pygame.draw.rect(screen, COLOR_BONUS_FOOD, bonus_rect, border_radius=5)
                # Add a pulsing effect or glow? Simple border for now.
                pygame.draw.rect(screen, COLOR_TEXT, bonus_rect, 1, border_radius=5)
            
            # Draw snake
            for i, segment in enumerate(snake.body):
                color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
                seg_rect = pygame.Rect(segment[0] * GRID_SIZE, 
                                       segment[1] * GRID_SIZE + UI_HEIGHT, 
                                       GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, color, seg_rect)
                pygame.draw.rect(screen, COLOR_BACKGROUND, seg_rect, 1)

            # Draw UI
            score_surface = font.render(f"Score: {score}", True, COLOR_TEXT)
            high_score_surface = font.render(f"High Score: {high_score}", True, COLOR_TEXT)
            level_surface = font.render(f"Level: {selected_level}", True, COLOR_TEXT)
            screen.blit(score_surface, (10, UI_HEIGHT // 2 - score_surface.get_height() // 2))
            screen.blit(high_score_surface, (SCREEN_WIDTH - high_score_surface.get_width() - 10, UI_HEIGHT // 2 - high_score_surface.get_height() // 2))
            screen.blit(level_surface, (SCREEN_WIDTH // 2 - level_surface.get_width() // 2, UI_HEIGHT // 2 - level_surface.get_height() // 2))

            if current_state == STATE_PAUSED:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT + UI_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))

                pause_surface = large_font.render("PAUSED", True, COLOR_TEXT)
                screen.blit(pause_surface, (SCREEN_WIDTH // 2 - pause_surface.get_width() // 2, 200))
                for btn in pause_buttons:
                    btn.draw(screen)

            if current_state == STATE_GAME_OVER:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT + UI_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))

                over_surface = large_font.render("GAME OVER", True, COLOR_FOOD)
                restart_surface = font.render("Press R to Restart", True, COLOR_TEXT)
                final_score_surface = font.render(f"Final Score: {score}", True, COLOR_TEXT)
                
                mid_y = (SCREEN_HEIGHT + UI_HEIGHT) // 2
                over_rect = over_surface.get_rect(center=(SCREEN_WIDTH // 2, mid_y - 40))
                final_rect = final_score_surface.get_rect(center=(SCREEN_WIDTH // 2, mid_y + 10))
                restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, mid_y + 60))
                
                screen.blit(over_surface, over_rect)
                screen.blit(final_score_surface, final_rect)
                screen.blit(restart_surface, restart_rect)

        pygame.display.flip()
        clock.tick(fps if current_state == STATE_PLAYING else 60)

if __name__ == "__main__":
    main()
