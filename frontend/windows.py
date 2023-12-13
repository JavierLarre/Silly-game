import typing
from PyQt6.QtWidgets import (
    QLabel, QWidget, QPushButton, QGridLayout, QMainWindow,
    QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QKeyEvent

from frontend import bunny_frontend_functions as bff
from frontend import entities
import param as p

class LevelSelector(QWidget):
    selected_level = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle("Select a level")
        self.setGeometry(p.X_POS,
                         p.Y_POS,
                         p.WIDTH_GAME,
                         p.HEIGHT_GAME)
        
        self.options = QComboBox(self)
        self.button = QPushButton("&Go!", self)
        self.button.clicked.connect(self.send_level)
        
        options_vbox = QVBoxLayout()
        options_vbox.addStretch(1)
        options_vbox.addWidget(self.options)
        options_vbox.addStretch(1)

        button_vbox = QVBoxLayout()
        button_vbox.addStretch(1)
        button_vbox.addWidget(self.button)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(options_vbox)
        hbox.addStretch(1)
        hbox.addLayout(button_vbox)

        self.setLayout(hbox)

    def add_options(self, options: list[str]):
        self.options.addItems(options)

    def send_level(self):
        level = self.options.currentText()
        self.selected_level.emit(level)


class GameWindow(QMainWindow):
    pressed_key = pyqtSignal(QKeyEvent)

    def __init__(self) -> None:
        super().__init__()
        self.player = None
        self.setGeometry(p.X_POS,
                         p.Y_POS,
                         p.WIDTH_GAME,
                         p.HEIGHT_GAME)
        self.setCentralWidget(QLabel(self))
        self.centralWidget().setMaximumSize(p.WIDTH_GAME, p.HEIGHT_GAME)
        
    def load_maze(self, maze: list):
        old_layout = self.centralWidget().layout()
        if old_layout is not None:
            QWidget().setLayout(old_layout)

        layout = QGridLayout()
        layout.setSpacing(0)
        positions = bff.get_all_positions(maze)

        for i, j in positions:
            if maze[i][j] == "P":
                tile = entities.Wall(self)
            else:
                tile = entities.BackGround(self)
            layout.addWidget(tile, i, j)
            
            if maze[i][j] == "E":
                self.player = entities.Player(self)
                layout.addWidget(self.player, i, j)

        self.centralWidget().setLayout(layout)

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        if not a0.isAutoRepeat():
            self.pressed_key.emit(a0)

    def move_player(self, direction: str, new_position: list):
        grid: QGridLayout = self.centralWidget().layout()
        grid.addWidget(self.player, *new_position)
        self.player.raise_()