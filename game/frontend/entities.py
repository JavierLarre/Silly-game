import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap

from game.frontend.frontend_functions import get_sprite_path

WALL_FILE_NAME = "bloque_pared"
BACKGROUND_FILE_NAME = "bloque_fondo"
FILE_EXTENSION = "jpg"


class Player(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        sprite_name = "grace"
        directions = (
            "arriba",
            "abajo",
            "izquierda",
            "derecha"
        )
        number_of_sprites = 3 # the number of sprites for each direction

        default_path = get_sprite_path(f"{sprite_name}.png")
        self.sprites = {}
        self.sprites["default"] = QPixmap(default_path)
        self.setPixmap(self.sprites["default"])
        self.setScaledContents(True)
            

class Wall(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        path = get_sprite_path(f"{WALL_FILE_NAME}.{FILE_EXTENSION}")
        self.setPixmap(QPixmap(path))
        self.setScaledContents(True)


class BackGround(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        path = get_sprite_path(f"{BACKGROUND_FILE_NAME}.{FILE_EXTENSION}")
        self.setPixmap(QPixmap(path))
        self.setScaledContents(True)

class ClickableTile(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent, position):
        super().__init__(parent)
        self.wall_tile = Wall(self)
        self.background_tile = BackGround(self)
        self.position = position

        self.current_sprite = "wall"
        self.setPixmap(self.wall_tile.pixmap())
        self.setScaledContents(True)

    def change_sprite(self):
        if self.current_sprite == "wall":
            self.current_sprite = "background"
            self.setPixmap(self.background_tile.pixmap())
            self.setScaledContents(True)
        elif self.current_sprite == "background":
            self.current_sprite = "wall"
            self.setPixmap(self.wall_tile.pixmap())
            self.setScaledContents(True)
    
    def mousePressEvent(self, ev: QtGui.QMouseEvent | None) -> None:
        self.clicked.emit()