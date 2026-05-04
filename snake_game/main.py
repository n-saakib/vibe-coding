import pygame
import sys
from constants import *
from snake_logic import Snake, Food

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    # Initialize game objects
    snake = Snake()
    food = Food(snake.body)
    score = 0
    fps = INITIAL_FPS
    game_over = False

    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        snake.set_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.set_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.set_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.set_direction((1, 0))
                else:
                    if event.key == pygame.K_r:
                        # Restart game
                        snake = Snake()
                        food = Food(snake.body)
                        score = 0
                        fps = INITIAL_FPS
                        game_over = False

        # 2. Update Logic
        if not game_over:
            snake.move()
            
            # Check collision
            if snake.check_collision():
                game_over = True
            
            # Check food consumption
            if snake.body[0] == food.position:
                snake.grow()
                food.spawn(snake.body)
                score += SCORE_PER_FOOD
                # Dynamic difficulty
                if score % DIFFICULTY_STEP == 0:
                    fps += SPEED_INCREMENT

        # 3. Rendering
        screen.fill(COLOR_BACKGROUND)
        
        # Draw food
        food_rect = pygame.Rect(food.position[0] * GRID_SIZE, 
                                food.position[1] * GRID_SIZE, 
                                GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, COLOR_FOOD, food_rect)
        
        # Draw snake
        for i, segment in enumerate(snake.body):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            seg_rect = pygame.Rect(segment[0] * GRID_SIZE, 
                                   segment[1] * GRID_SIZE, 
                                   GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, seg_rect)
            # Add a small border to segments
            pygame.draw.rect(screen, COLOR_BACKGROUND, seg_rect, 1)

        # Draw score
        score_surface = font.render(f"Score: {score}", True, COLOR_TEXT)
        screen.blit(score_surface, (10, 10))

        if game_over:
            over_surface = font.render("GAME OVER - Press R to Restart", True, COLOR_TEXT)
            over_rect = over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(over_surface, over_rect)

        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()
