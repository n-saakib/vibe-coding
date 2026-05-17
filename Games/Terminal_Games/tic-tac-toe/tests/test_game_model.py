import pytest
from models.game_model import GameModel

def test_initial_state():
    model = GameModel()
    assert model.current_player == 'X'
    assert model.winner is None
    assert model.is_draw is False
    for row in model.board:
        for cell in row:
            assert cell is None

def test_make_valid_move():
    model = GameModel()
    success = model.make_move(0, 0)
    assert success is True
    assert model.board[0][0] == 'X'
    assert model.current_player == 'O'

def test_make_invalid_move_occupied():
    model = GameModel()
    model.make_move(0, 0)
    success = model.make_move(0, 0)
    assert success is False
    assert model.board[0][0] == 'X'
    assert model.current_player == 'O'  # Player should not switch

def test_make_invalid_move_out_of_bounds():
    model = GameModel()
    assert model.make_move(3, 0) is False
    assert model.make_move(-1, 0) is False

def test_win_horizontal():
    model = GameModel()
    # X wins on top row
    model.make_move(0, 0) # X
    model.make_move(1, 0) # O
    model.make_move(0, 1) # X
    model.make_move(1, 1) # O
    model.make_move(0, 2) # X
    assert model.winner == 'X'
    assert model.is_draw is False

def test_win_vertical():
    model = GameModel()
    # O wins on first column
    model.make_move(0, 1) # X
    model.make_move(0, 0) # O
    model.make_move(1, 1) # X
    model.make_move(1, 0) # O
    model.make_move(2, 2) # X
    model.make_move(2, 0) # O
    assert model.winner == 'O'

def test_win_diagonal():
    model = GameModel()
    # X wins on main diagonal
    model.make_move(0, 0) # X
    model.make_move(0, 1) # O
    model.make_move(1, 1) # X
    model.make_move(0, 2) # O
    model.make_move(2, 2) # X
    assert model.winner == 'X'

def test_draw():
    model = GameModel()
    # X O X
    # X X O
    # O X O
    moves = [
        (0, 0), (0, 1), (0, 2),
        (1, 1), (1, 0), (1, 2),
        (2, 1), (2, 0), (2, 2)
    ]
    for r, c in moves:
        model.make_move(r, c)
    
    assert model.winner is None
    assert model.is_draw is True

def test_reset():
    model = GameModel()
    model.make_move(0, 0)
    model.reset()
    assert model.board[0][0] is None
    assert model.current_player == 'X'
