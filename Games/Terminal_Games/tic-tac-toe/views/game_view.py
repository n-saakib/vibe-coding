import pygame

# Constants for the View
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700  # Increased height for scoreboard
BOARD_HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = SCREEN_WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
SCORE_COLOR = (255, 255, 255)

class GameView:
    """Handles the visual representation of the game using Pygame."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('TIC TAC TOE')
        self.screen.fill(BG_COLOR)
        self.font = pygame.font.SysFont('Arial', 40)
        self.small_font = pygame.font.SysFont('Arial', 24)

    def draw_lines(self):
        """Draws the grid lines for the board."""
        # Horizontal lines
        pygame.draw.line(self.screen, LINE_COLOR, (0, SQUARE_SIZE), (SCREEN_WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (SCREEN_WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
        # Vertical lines
        pygame.draw.line(self.screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, BOARD_HEIGHT), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, BOARD_HEIGHT), LINE_WIDTH)

    def draw_figures(self, board):
        """Draws X and O markers based on the current board state."""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 'O':
                    pygame.draw.circle(self.screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif board[row][col] == 'X':
                    pygame.draw.line(self.screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                    pygame.draw.line(self.screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

    def draw_winning_line(self, win_info):
        """Highlights the winning combination."""
        color = (200, 0, 0)
        for type, index in win_info:
            if type == 'row':
                y = index * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.line(self.screen, color, (15, y), (SCREEN_WIDTH - 15, y), 10)
            elif type == 'col':
                x = index * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.line(self.screen, color, (x, 15), (x, BOARD_HEIGHT - 15), 10)
            elif type == 'diag':
                if index == 0:
                    pygame.draw.line(self.screen, color, (15, 15), (SCREEN_WIDTH - 15, BOARD_HEIGHT - 15), 10)
                else:
                    pygame.draw.line(self.screen, color, (15, BOARD_HEIGHT - 15), (SCREEN_WIDTH - 15, 15), 10)

    def draw_scoreboard(self, scores, current_player, mode_text):
        """Renders the scores and game mode info at the bottom."""
        # Clear scoreboard area
        pygame.draw.rect(self.screen, LINE_COLOR, (0, BOARD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - BOARD_HEIGHT))
        
        x_score = self.small_font.render(f"Player X: {scores['X']}", True, SCORE_COLOR)
        o_score = self.small_font.render(f"Player O: {scores['O']}", True, SCORE_COLOR)
        turn_text = self.small_font.render(f"Turn: {current_player}", True, SCORE_COLOR)
        mode_label = self.small_font.render(f"Mode: {mode_text}", True, SCORE_COLOR)
        controls = self.small_font.render("R: Reset | 1: PvP | 2: Easy | 3: Hard", True, SCORE_COLOR)

        self.screen.blit(x_score, (20, BOARD_HEIGHT + 10))
        self.screen.blit(o_score, (20, BOARD_HEIGHT + 40))
        self.screen.blit(turn_text, (200, BOARD_HEIGHT + 10))
        self.screen.blit(mode_label, (200, BOARD_HEIGHT + 40))
        self.screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, BOARD_HEIGHT + 70))

    def update_display(self):
        """Refreshes the Pygame display."""
        pygame.display.update()

    def show_message(self, text):
        """Displays a message in the center of the screen."""
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, BOARD_HEIGHT // 2))
        
        # Simple overlay
        overlay = pygame.Surface((SCREEN_WIDTH, 100))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, BOARD_HEIGHT // 2 - 50))
        
        self.screen.blit(text_surface, text_rect)
        self.update_display()

    def clear_screen(self):
        """Clears the screen with the background color."""
        self.screen.fill(BG_COLOR)
        self.draw_lines()
        self.update_display()
