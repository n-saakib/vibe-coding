import random
import copy

class AI:
    """Base class for AI opponents."""
    
    def __init__(self, player='O'):
        self.player = player  # AI usually plays as 'O'

    def get_move(self, model):
        raise NotImplementedError("AI subclasses must implement get_move")

class EasyAI(AI):
    """AI that makes random moves."""
    
    def get_move(self, model):
        available_moves = model.get_available_moves()
        if available_moves:
            return random.choice(available_moves)
        return None

class MinimaxAI(AI):
    """Unbeatable AI using the Minimax algorithm."""
    
    def get_move(self, model):
        # If board is empty, take a random corner or center to speed things up
        available_moves = model.get_available_moves()
        if len(available_moves) == 9:
            return random.choice([(0,0), (0,2), (2,0), (2,2), (1,1)])
        
        best_score = -float('inf')
        move = None
        
        for r, c in available_moves:
            # Simulate move
            model.board[r][c] = self.player
            score = self.minimax(model, 0, False)
            model.board[r][c] = None  # Undo move
            
            if score > best_score:
                best_score = score
                move = (r, c)
        
        return move

    def minimax(self, model, depth, is_maximizing):
        # Check terminal states
        if self.check_win(model, self.player):
            return 10 - depth
        if self.check_win(model, 'X' if self.player == 'O' else 'O'):
            return depth - 10
        if model.check_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for r, c in model.get_available_moves():
                model.board[r][c] = self.player
                score = self.minimax(model, depth + 1, False)
                model.board[r][c] = None
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            opponent = 'X' if self.player == 'O' else 'O'
            for r, c in model.get_available_moves():
                model.board[r][c] = opponent
                score = self.minimax(model, depth + 1, True)
                model.board[r][c] = None
                best_score = min(score, best_score)
            return best_score

    def check_win(self, model, player):
        """Helper to check win for a specific player during simulation."""
        # Row check
        for row in range(3):
            if all(model.board[row][col] == player for col in range(3)):
                return True
        # Col check
        for col in range(3):
            if all(model.board[row][col] == player for row in range(3)):
                return True
        # Diag check
        if all(model.board[i][i] == player for i in range(3)):
            return True
        if all(model.board[i][2-i] == player for i in range(3)):
            return True
        return False
