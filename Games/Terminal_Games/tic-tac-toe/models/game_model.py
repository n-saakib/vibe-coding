import random

class GameModel:
    """Manages the state and logic of the Tic-Tac-Toe game."""

    def __init__(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.player_names = {'X': 'Player X', 'O': 'Player O'}
        self.current_player = random.choice(['X', 'O'])
        self.winner = None
        self.is_draw = False
        self.scores = {'X': 0, 'O': 0}
        self.winning_line = None

    def make_move(self, row, col):
        """Places a marker at the specified row and column if valid."""
        if self.winner or self.is_draw:
            return False  # Game is already over

        if not (0 <= row < 3 and 0 <= col < 3):
            return False  # Out of bounds

        if self.board[row][col] is not None:
            return False  # Cell already occupied

        self.board[row][col] = self.current_player
        
        win_info = self.check_winner(row, col)
        if win_info:
            self.winner = self.current_player
            self.winning_line = win_info
            self.scores[self.current_player] += 1
        elif self.check_draw():
            self.is_draw = True
        else:
            self.switch_player()
            
        return True

    def switch_player(self):
        """Switches the current player between 'X' and 'O'."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self, last_row, last_col):
        """Checks if the last move resulted in a win. Returns winning line if any."""
        player = self.board[last_row][last_col]

        # Check row
        if all(self.board[last_row][c] == player for c in range(3)):
            return [('row', last_row)]

        # Check column
        if all(self.board[r][last_col] == player for r in range(3)):
            return [('col', last_col)]

        # Check diagonals
        winning_lines = []
        if last_row == last_col:
            if all(self.board[i][i] == player for i in range(3)):
                winning_lines.append(('diag', 0))
        
        if last_row + last_col == 2:
            if all(self.board[i][2 - i] == player for i in range(3)):
                winning_lines.append(('diag', 1))

        return winning_lines if winning_lines else None

    def check_draw(self):
        """Checks if the board is full and there is no winner."""
        return all(cell is not None for row in self.board for cell in row)

    def reset(self):
        """Resets the game state (but keeps scores and names)."""
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = random.choice(['X', 'O'])
        self.winner = None
        self.is_draw = False
        self.winning_line = None

    def reset_scores(self):
        """Resets the scores."""
        self.scores = {'X': 0, 'O': 0}

    def set_player_names(self, name_x, name_o):
        """Sets custom names for players."""
        if name_x: self.player_names['X'] = name_x[:8]
        if name_o: self.player_names['O'] = name_o[:8]

    def get_available_moves(self):
        """Returns a list of (row, col) tuples for empty cells."""
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] is None]
