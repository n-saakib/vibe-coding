import pygame

# Constants for the View
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
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
BUTTON_COLOR = (66, 66, 66)
BUTTON_TEXT_COLOR = (255, 255, 255)
INPUT_BOX_COLOR = (255, 255, 255)

class GameView:
    """Handles the visual representation of the game using Pygame."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('TIC TAC TOE')
        self.screen.fill(BG_COLOR)
        self.font = pygame.font.SysFont('Arial', 40)
        self.small_font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 60, bold=True)

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

    def draw_scoreboard(self, scores, current_player, player_names, mode_text):
        """Renders the scores and game mode info at the bottom."""
        pygame.draw.rect(self.screen, LINE_COLOR, (0, BOARD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - BOARD_HEIGHT))
        
        x_name = player_names['X']
        o_name = player_names['O']
        current_name = player_names[current_player]

        x_score = self.small_font.render(f"{x_name}: {scores['X']}", True, SCORE_COLOR)
        o_score = self.small_font.render(f"{o_name}: {scores['O']}", True, SCORE_COLOR)
        turn_text = self.small_font.render(f"Turn: {current_name}", True, SCORE_COLOR)
        mode_label = self.small_font.render(f"Mode: {mode_text}", True, SCORE_COLOR)
        controls = self.small_font.render("R: Reset | ESC: Menu", True, SCORE_COLOR)

        self.screen.blit(x_score, (20, BOARD_HEIGHT + 10))
        self.screen.blit(o_score, (20, BOARD_HEIGHT + 40))
        self.screen.blit(turn_text, (200, BOARD_HEIGHT + 10))
        self.screen.blit(mode_label, (200, BOARD_HEIGHT + 40))
        self.screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, BOARD_HEIGHT + 70))

    def draw_button(self, text, y_pos, active=False):
        """Draws a styled button."""
        color = (100, 100, 100) if active else BUTTON_COLOR
        rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, y_pos, 300, 50)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        text_surf = self.small_font.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        return rect

    def draw_input_box(self, label, text, y_pos, active=False):
        """Draws an input box with a label."""
        label_surf = self.small_font.render(label, True, SCORE_COLOR)
        self.screen.blit(label_surf, (SCREEN_WIDTH // 2 - 150, y_pos - 30))
        
        rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, y_pos, 300, 40)
        color = (200, 200, 200) if active else (255, 255, 255)
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2, border_radius=5)
        
        text_surf = self.small_font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surf, (rect.x + 10, rect.y + 5))
        return rect

    def show_main_menu(self):
        """Renders the main menu screen."""
        self.screen.fill(BG_COLOR)
        title = self.title_font.render("TIC TAC TOE", True, SCORE_COLOR)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        btn_pvp = self.draw_button("Player vs Player", 250)
        btn_ai = self.draw_button("Player vs AI", 350)
        btn_quit = self.draw_button("Quit", 450)
        
        self.update_display()
        return btn_pvp, btn_ai, btn_quit

    def show_pvp_menu(self, name_x, name_o, active_input):
        """Renders the PvP name entry screen."""
        self.screen.fill(BG_COLOR)
        title = self.font.render("Enter Player Names", True, SCORE_COLOR)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        box_x = self.draw_input_box("Player X Name:", name_x, 250, active_input == 'X')
        box_o = self.draw_input_box("Player O Name:", name_o, 350, active_input == 'O')
        
        btn_start = self.draw_button("Start Game", 450)
        btn_back = self.draw_button("Back", 530)
        
        self.update_display()
        return box_x, box_o, btn_start, btn_back

    def show_ai_menu(self, difficulty):
        """Renders the AI difficulty selection screen."""
        self.screen.fill(BG_COLOR)
        title = self.font.render("Select AI Difficulty", True, SCORE_COLOR)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        btn_easy = self.draw_button("Easy (Random)", 250, difficulty == 'easy')
        btn_hard = self.draw_button("Hard (Minimax)", 350, difficulty == 'hard')
        
        btn_start = self.draw_button("Start Game", 450)
        btn_back = self.draw_button("Back", 530)
        
        self.update_display()
        return btn_easy, btn_hard, btn_start, btn_back

    def update_display(self):
        """Refreshes the Pygame display."""
        pygame.display.update()

    def show_message(self, text):
        """Displays a message in the center of the screen."""
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, BOARD_HEIGHT // 2))
        
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
