import pygame
import sys
import time
from models.game_model import GameModel
from views.game_view import GameView, SQUARE_SIZE
from ai.ai_players import EasyAI, MinimaxAI

class GameController:
    """Coordinates interaction between the Model and the View."""

    def __init__(self, model, view, ai_opponent=None):
        self.model = model
        self.view = view
        self.ai_opponent = ai_opponent
        self.game_over = False

    def get_mode_text(self):
        if self.ai_opponent is None:
            return "PvP"
        elif isinstance(self.ai_opponent, EasyAI):
            return "Easy AI"
        elif isinstance(self.ai_opponent, MinimaxAI):
            return "Hard AI"
        return "Unknown"

    def run(self):
        """Main game loop."""
        self.view.draw_lines()
        self.view.draw_scoreboard(self.model.scores, self.model.current_player, self.get_mode_text())
        
        while True:
            # AI Move
            if self.ai_opponent and self.model.current_player == self.ai_opponent.player and not self.game_over:
                time.sleep(0.5)  # Natural delay
                row, col = self.ai_opponent.get_move(self.model)
                self.process_move(row, col)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    # If it's AI's turn, ignore clicks
                    if self.ai_opponent and self.model.current_player == self.ai_opponent.player:
                        continue

                    mouseX = event.pos[0]
                    mouseY = event.pos[1]

                    clicked_row = int(mouseY // SQUARE_SIZE)
                    clicked_col = int(mouseX // SQUARE_SIZE)

                    if clicked_row < 3: # Ignore clicks in scoreboard area
                        self.process_move(clicked_row, clicked_col)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    if event.key == pygame.K_1:
                        self.set_mode(None)
                    if event.key == pygame.K_2:
                        self.set_mode(EasyAI())
                    if event.key == pygame.K_3:
                        self.set_mode(MinimaxAI())

            self.view.update_display()

    def process_move(self, row, col):
        """Handles a move attempt."""
        if self.model.make_move(row, col):
            self.view.draw_figures(self.model.board)
            self.view.draw_scoreboard(self.model.scores, self.model.current_player, self.get_mode_text())
            
            if self.model.winner:
                self.view.draw_winning_line(self.model.winning_line)
                self.view.show_message(f"Player {self.model.winner} Wins!")
                self.game_over = True
            elif self.model.is_draw:
                self.view.show_message("Draw!")
                self.game_over = True
            
            self.view.update_display()

    def reset_game(self):
        """Resets the game state and view."""
        self.model.reset()
        self.view.clear_screen()
        self.view.draw_scoreboard(self.model.scores, self.model.current_player, self.get_mode_text())
        self.game_over = False

    def set_mode(self, ai_opponent):
        """Changes the game mode and resets."""
        self.ai_opponent = ai_opponent
        self.reset_game()
