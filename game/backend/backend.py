from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt

import param as p
from game.backend import backend_functions as b_utils


class GameLogic(QObject):
    mazes_list = pyqtSignal(list)
    selected_maze = pyqtSignal(list)
    new_position = pyqtSignal(str, list)
    status_bar = pyqtSignal(str)
    go_back = pyqtSignal()
    exit_reached = pyqtSignal()


    def __init__(self) -> None:
        super().__init__()
        self.maze = []
        self.player_position = [0, 0]
        self.special_positions = {
            "entrance": None,
            "exit": None
        }

    def start(self):
        mazes = b_utils.get_mazes()
        self.mazes_list.emit(mazes)

    def load_maze(self, file_name: str):
        self.maze = b_utils.read_maze(file_name)
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
            case Qt.Key.Key_Q:
                self.go_back.emit()
                self.start()

        if direction != "":
            self.move_player(direction)

    def move_player(self, direction: str):
        # all in one function, so that all directions have the same behaviour
        axis, i = b_utils.get_axis(direction)
        new_position = self.player_position.copy()
        new_position[axis] += i

        if b_utils.is_valid_position(new_position, self.maze):
            self.player_position = new_position
            self.new_position.emit(direction, new_position)

            if new_position == self.special_positions["exit"]:
                self.exit_reached.emit()

    def get_special_positions(self) -> None:
        positions = b_utils.get_all_positions(self.maze)
        for position in positions:
            i, j = position
            if self.maze[i][j] == "E":
                self.special_positions["entrance"] = [i, j]
                self.player_position = [i, j]
            if self.maze[i][j] == "S":
                self.special_positions["exit"] = [i, j]


class EditorLogic(QObject):
    mazes_list = pyqtSignal(list)
    selected_maze = pyqtSignal(list)
    status_bar = pyqtSignal(str)
    change_tile = pyqtSignal(tuple)

    def __init__(self) -> None:
        super().__init__()
        self.maze = []
    
    def start(self):
        mazes = b_utils.get_mazes()
        mazes.append("new maze")
        self.mazes_list.emit(mazes)

    def load_maze(self, file_name: str, width: int, height: int):
        if file_name == "new maze":
            self.maze = [["P" for i in range(width)] for j in range(height)]
        else:
            self.maze = b_utils.read_maze(file_name)
        
        self.selected_maze.emit(self.maze)

    def press_tile(self, position: tuple):
        if b_utils.on_border(position, self.maze):
            self.status_bar.emit("You can't edit border tiles!")
            return
        
        self.change_tile.emit(position)
            