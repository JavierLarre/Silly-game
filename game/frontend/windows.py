import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QLabel, QWidget, QPushButton, QGridLayout, QMainWindow,
    QHBoxLayout, QVBoxLayout, QComboBox, QSpinBox)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QKeyEvent

from game.frontend import frontend_functions as f_utils
from game.frontend import entities
import param as p

from game.frontend.frontend_functions import get_rata_path
from PyQt6.QtGui import QPixmap


class LevelSelector(QWidget):
    selected_level = pyqtSignal(str, int, int)

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
        self.dimensions_label = QLabel("Dimensions: ", self)
        self.width_line = QSpinBox(self)
        self.height_line = QSpinBox(self)
        
        self.options.currentTextChanged.connect(self.show_dimensions)
        self.button.clicked.connect(self.send_level)
        self.width_line.setMinimum(0)
        self.width_line.setMaximum(100)
        self.height_line.setMinimum(0)
        self.height_line.setMaximum(100)
        
        
        options_box = QHBoxLayout()
        options_box.addStretch(1)
        options_box.addWidget(self.options)
        options_box.addStretch(1)

        dimensions_box = QHBoxLayout()
        dimensions_box.addStretch(1)
        dimensions_box.addWidget(self.dimensions_label)
        dimensions_box.addWidget(self.width_line)
        dimensions_box.addWidget(self.height_line)
        dimensions_box.addStretch(1)

        button_box = QHBoxLayout()
        button_box.addStretch(1)
        button_box.addWidget(self.button)

        main_box = QVBoxLayout()
        main_box.addStretch(1)
        main_box.addLayout(options_box)
        main_box.addLayout(dimensions_box)
        main_box.addStretch(1)
        main_box.addLayout(button_box)

        self.setLayout(main_box)

    def add_options(self, options: list[str]):
        self.options.clear()
        self.options.addItems(options)

    def send_level(self):
        level = self.options.currentText()
        width = self.width_line.value()
        height = self.height_line.value()
        self.selected_level.emit(level, width, height)

    def show_dimensions(self, options_text: str):
        if (options_text != "new maze"):
            self.dimensions_label.hide()
            self.width_line.hide()
            self.height_line.hide()
        else:
            self.dimensions_label.show()
            self.width_line.show()
            self.height_line.show()


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
        positions = f_utils.get_all_positions(maze)

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
        self.pressed_key.emit(a0)
        if a0.text() == "r" and False:
            self.rata()
        

    def move_player(self, direction: str, new_position: list):
        grid: QGridLayout = self.centralWidget().layout()
        grid.addWidget(self.player, *new_position)
        self.player.raise_()

    def rata(self):
        print("rata")
        rata_1, rata_2 = QLabel(self), QLabel(self)
        path_1, path_2 = get_rata_path()
        pix_1, pix_2 = QPixmap(path_1), QPixmap(path_2)
        rata_1.setPixmap(pix_1)
        rata_1.setScaledContents(True)
        rata_2.setPixmap(pix_2)
        rata_2.setScaledContents(True)
        rata_1.setGeometry(100, 200, 200, 200)
        rata_2.setGeometry(300, 200, 200, 200)
        rata_1.show()
        rata_2.show()
        
class EditorWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
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

        layout = QGridLayout(self.centralWidget())
        layout.setSpacing(0)
        positions = f_utils.get_all_positions(maze)

        for i, j in positions:
            tile = entities.ClickableTile(self, (i, j))
            # tile = entities.Wall(self)
            layout.addWidget(tile, i, j)
            tile.clicked.connect(self.tile_clicked)
            
            if maze[i][j] != "P":
                tile.change_sprite()
            tile.repaint()

        self.centralWidget().setLayout(layout)

    def tile_clicked(self):
        tile = self.sender()
        print(tile.position)