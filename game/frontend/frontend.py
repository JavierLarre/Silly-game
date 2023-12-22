from PyQt6.QtCore import QObject
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QWidget

from game.frontend.windows import LevelSelector, GameWindow, EditorWindow

class GraphicsLogic(QObject):
    pressed_key = pyqtSignal(QKeyEvent)
    selected_level = pyqtSignal(str, int, int)
    pressed_tile = pyqtSignal(tuple)
    
    def __init__(self) -> None:
        super().__init__()
        self.level_selector = LevelSelector()
        self.level_selector.selected_level.connect(
            self.selected_level.emit)
        
        self.game_window = GameWindow()
        self.game_window.pressed_key.connect(
            self.pressed_key.emit)
        
        self.editor_window = EditorWindow()
        self.editor_window.clicked_tile.connect(
            self.pressed_tile.emit)
    
    def start(self):
        self.level_selector.show()

    def add_level_options(self, options: list[str]):
        self.level_selector.add_options(options)

    def show_maze(self, maze: list):
        self.level_selector.hide()
        self.game_window.load_maze(maze)
        self.game_window.show()

    def move_player(self, direction: str, new_position: list):
        self.game_window.move_player(direction, new_position)

    def show_level_selector(self):
        self.level_selector.show()
        self.game_window.hide()

    def exit_reached(self):
        self.game_window.rata()
    
    def show_level_editor(self, maze: list):
        self.level_selector.hide()
        self.editor_window.load_maze(maze)
        self.editor_window.show()

    def change_tile(self, position: tuple):
        self.editor_window.change_tile(position)