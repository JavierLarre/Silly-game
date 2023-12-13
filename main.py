from PyQt6.QtWidgets import QApplication
import sys

from game.backend.backend import GameLogic
from game.frontend.frontend import GraphicsLogic


class Game:
    def __init__(self) -> None:
        self.backend = GameLogic()
        self.frontend = GraphicsLogic()
        self.connect_backend_signals()
        self.connect_frontend_signals()

    def connect_backend_signals(self):
        self.backend.mazes_list.connect(
            self.frontend.add_level_options)
        
        self.backend.selected_maze.connect(
            self.frontend.show_maze)
        
        self.backend.new_position.connect(
            self.frontend.move_player)
        
        self.backend.go_back.connect(
            self.frontend.show_level_selector)
        
        self.backend.exit_reached.connect(
            self.frontend.exit_reached)

    def connect_frontend_signals(self):
        self.frontend.selected_level.connect(
            self.backend.load_maze)
        
        self.frontend.pressed_key.connect(
            self.backend.keypress_router)
        

    def start(self):
        self.backend.start()
        self.frontend.start()


if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    game = Game()
    game.start()
    sys.exit(app.exec())