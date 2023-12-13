from PyQt6.QtCore import QObject
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QKeyEvent

from frontend.windows import LevelSelector, GameWindow


class GraphicsLogic(QObject):
    pressed_key = pyqtSignal(QKeyEvent)
    selected_level = pyqtSignal(str)
    
    def __init__(self) -> None:
        super().__init__()
        self.level_selector = LevelSelector()
        self.level_selector.selected_level.connect(
            self.selected_level.emit)
        
        self.game_window = GameWindow()
        self.game_window.pressed_key.connect(
            self.pressed_key.emit)
    
    def start(self):
        self.level_selector.show()

    def add_level_options(self, options: list[str]):
        self.level_selector.add_options(options)

    def show_maze(self, maze: list):
        self.level_selector.hide()
        self.game_window.show()
        self.game_window.load_maze(maze)

    def move_player(self, direction: str, new_position: list):
        self.game_window.move_player(direction, new_position)
