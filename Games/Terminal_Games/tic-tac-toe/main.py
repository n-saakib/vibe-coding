from models.game_model import GameModel
from views.game_view import GameView
from controllers.game_controller import GameController

def main():
    model = GameModel()
    view = GameView()
    controller = GameController(model, view)
    
    controller.run()

if __name__ == "__main__":
    main()
