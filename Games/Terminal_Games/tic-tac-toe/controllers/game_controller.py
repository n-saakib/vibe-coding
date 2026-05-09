import pygame
import sys
import time
from models.game_model import GameModel
from views.game_view import GameView, SQUARE_SIZE
from ai.ai_players import EasyAI, MinimaxAI

class GameController:
    """Coordinates interaction between the Model and the View."""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.ai_opponent = None
        self.game_over = False
        self.state = 'MAIN_MENU'
        
        # Menu state variables
        self.player_x_name = ""
        self.player_o_name = ""
        self.active_input = 'X'
        self.ai_difficulty = 'easy'

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
        while True:
            if self.state == 'MAIN_MENU':
                self.handle_main_menu()
            elif self.state == 'PVP_MENU':
                self.handle_pvp_menu()
            elif self.state == 'AI_MENU':
                self.handle_ai_menu()
            elif self.state == 'PLAYING':
                self.handle_playing()

            self.view.update_display()

    def handle_main_menu(self):
        btn_pvp, btn_ai, btn_quit = self.view.show_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pvp.collidepoint(event.pos):
                    self.state = 'PVP_MENU'
                elif btn_ai.collidepoint(event.pos):
                    self.state = 'AI_MENU'
                elif btn_quit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    def handle_pvp_menu(self):
        box_x, box_o, btn_start, btn_back = self.view.show_pvp_menu(self.player_x_name, self.player_o_name, self.active_input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if box_x.collidepoint(event.pos):
                    self.active_input = 'X'
                elif box_o.collidepoint(event.pos):
                    self.active_input = 'O'
                elif btn_start.collidepoint(event.pos):
                    self.start_game(None)
                elif btn_back.collidepoint(event.pos):
                    self.state = 'MAIN_MENU'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.active_input == 'X': self.player_x_name = self.player_x_name[:-1]
                    else: self.player_o_name = self.player_o_name[:-1]
                elif event.key == pygame.K_RETURN:
                    self.start_game(None)
                elif event.key == pygame.K_TAB:
                    self.active_input = 'O' if self.active_input == 'X' else 'X'
                else:
                    if len(event.unicode) > 0 and event.unicode.isprintable():
                        if self.active_input == 'X' and len(self.player_x_name) < 8:
                            self.player_x_name += event.unicode
                        elif self.active_input == 'O' and len(self.player_o_name) < 8:
                            self.player_o_name += event.unicode

    def handle_ai_menu(self):
        btn_easy, btn_hard, btn_start, btn_back = self.view.show_ai_menu(self.ai_difficulty)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_easy.collidepoint(event.pos):
                    self.ai_difficulty = 'easy'
                elif btn_hard.collidepoint(event.pos):
                    self.ai_difficulty = 'hard'
                elif btn_start.collidepoint(event.pos):
                    ai = EasyAI() if self.ai_difficulty == 'easy' else MinimaxAI()
                    self.start_game(ai)
                elif btn_back.collidepoint(event.pos):
                    self.state = 'MAIN_MENU'

    def handle_playing(self):
        # AI Move
        if self.ai_opponent and self.model.current_player == self.ai_opponent.player and not self.game_over:
            time.sleep(0.5)
            row, col = self.ai_opponent.get_move(self.model)
            self.process_move(row, col)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                if self.ai_opponent and self.model.current_player == self.ai_opponent.player:
                    continue
                mouseX, mouseY = event.pos
                clicked_row, clicked_col = int(mouseY // SQUARE_SIZE), int(mouseX // SQUARE_SIZE)
                if clicked_row < 3:
                    self.process_move(clicked_row, clicked_col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                if event.key == pygame.K_ESCAPE:
                    self.state = 'MAIN_MENU'
                    self.game_over = False

    def start_game(self, ai_opponent):
        """Initializes game settings and starts the match."""
        self.ai_opponent = ai_opponent
        self.model.reset_scores()
        
        name_x = self.player_x_name if self.player_x_name else "Player X"
        name_o = self.player_o_name if self.player_o_name else ("AI" if ai_opponent else "Player O")
        self.model.set_player_names(name_x, name_o)
        
        self.model.reset()
        self.view.clear_screen()
        self.view.draw_scoreboard(self.model.scores, self.model.current_player, self.model.player_names, self.get_mode_text())
        self.state = 'PLAYING'
        self.game_over = False

    def process_move(self, row, col):
        """Handles a move attempt."""
        if self.model.make_move(row, col):
            self.view.draw_figures(self.model.board)
            self.view.draw_scoreboard(self.model.scores, self.model.current_player, self.model.player_names, self.get_mode_text())
            
            if self.model.winner:
                self.view.draw_winning_line(self.model.winning_line)
                winner_name = self.model.player_names[self.model.winner]
                self.view.show_message(f"{winner_name} Wins!")
                self.game_over = True
            elif self.model.is_draw:
                self.view.show_message("Draw!")
                self.game_over = True
            
            self.view.update_display()

    def reset_game(self):
        """Resets the game state and view."""
        self.model.reset()
        self.view.clear_screen()
        self.view.draw_scoreboard(self.model.scores, self.model.current_player, self.model.player_names, self.get_mode_text())
        self.game_over = False
