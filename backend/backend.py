from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt

import param as p
from backend import bunny_backend_functions as bbf


# TODO
# load list of mazes
# send mazes info
# end level
# move bunny


class GameLogic(QObject):
    mazes_list = pyqtSignal(list)
    selected_maze = pyqtSignal(list)
    new_position = pyqtSignal(str, list)
    status_bat = pyqtSignal(str)


    def __init__(self) -> None:
        super().__init__()
        self.maze = []
        self.player_position = [0, 0]
        self.special_positions = {
            "entrance": None,
            "exit": None
        }

    def start(self):
        mazes = bbf.get_mazes()
        self.mazes_list.emit(mazes)

    def load_maze(self, file_name: str):
        self.maze = bbf.read_maze(file_name)
        self.get_special_positions()
        self.selected_maze.emit(self.maze)

    def keypress_router(self, event: QKeyEvent):
        direction = ""
        match event.key():
            case Qt.Key.Key_W:
                direction = "up"
            case Qt.Key.Key_A:
                direction = "left"
            case Qt.Key.Key_S:
                direction = "down"
            case Qt.Key.Key_D:
                direction = "right"

        if direction != "":
            self.move_player(direction)

    def move_player(self, direction: str):
        # all in one function, so that all directions have the same behaviour
        axis, i = bbf.get_axis(direction)
        new_position = self.player_position.copy()
        new_position[axis] += i

        if bbf.is_valid_position(new_position, self.maze):
            self.player_position = new_position
            self.new_position.emit(direction, new_position)

    def get_special_positions(self) -> None:
        positions = bbf.get_all_positions(self.maze)
        for position in positions:
            i, j = position
            if self.maze[i][j] == "E":
                self.special_positions["entrance"] = [i, j]
            if self.maze[i][j] == "S":
                self.special_positions["exit"] = [i, j]
            if self.maze[i][j] == "C":
                self.player_position = [i, j]
            