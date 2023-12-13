from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap

from frontend.bunny_frontend_functions import get_sprite_path


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

        for direction in directions:
            sprites = []
            for i in range(1, number_of_sprites+1):
                path = get_sprite_path(f"{sprite_name}_{direction}_{i}.png")
                sprites.append((i, QPixmap(path)))
            

class Wall(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        sprite_name = "bloque_pared"
        path = get_sprite_path(f"{sprite_name}.jpeg")
        self.setPixmap(QPixmap(path))
        self.setScaledContents(True)


class BackGround(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        sprite_name = "bloque_fondo"
        path = get_sprite_path(f"{sprite_name}.jpeg")
        self.setPixmap(QPixmap(path))
        self.setScaledContents(True)