from PyQt6.QtWidgets import QApplication
import sys

from game.backend.backend import EditorLogic
from game.frontend.frontend import GraphicsLogic

class LevelEditor:
    def __init__(self) -> None:
        self.backend = EditorLogic()
        self.frontend = GraphicsLogic()
        self.connect_backend_signals()
        self.connect_frontend_signals()
    
    def connect_backend_signals(self):
        self.backend.mazes_list.connect(
            self.frontend.add_level_options)

    def connect_frontend_signals(self):
        pass

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
    editor = LevelEditor()
    editor.start()
    sys.exit(app.exec())