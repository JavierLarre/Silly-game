import param as p
import os
from typing import Iterable
from itertools import product


def get_maze_path(file_name: str | None = None) -> str:
    if file_name is None:
        path = os.path.join(*p.MAZES_PATH)
    else:
        path = os.path.join(*p.MAZES_PATH, file_name)
    
    return path


def get_mazes() -> list[str]:
    '''gets all the file names in /assets/mazes/'''
    
    files = [file for file in os.listdir(get_maze_path())
            if os.path.isfile(get_maze_path(file))]
    return files

def read_maze(file_name: str) -> list[list]:
    with open(get_maze_path(file_name)) as maze_file:

        maze = [[cell for cell in row.strip().split(",") if cell != ""]
                for row in maze_file.read().split("\n") if len(row) != 0]
    
    return maze


def is_valid_position(new_position: Iterable, maze: list) -> bool:
    i, j = new_position
    try:
        cell = maze[i][j]
    except IndexError:
        return False
    else:
        return cell != "P"

def get_all_positions(maze: list):
    width = range(len(maze))
    length = range(len(maze[0]))
    return product(width, length)

def get_axis(direction: str) -> tuple:
    axis = (0 if (direction == "up" or direction == "down") else 1)
    i = (-1 if (direction == "up" or direction == "left") else 1)
    return (axis, i)

def on_border(position: tuple, maze: list) -> bool:
    i, j = position
    width = len(maze)
    length = len(maze[0])
    return (False if 
            (0 < i < (width - 1)
             and 0 < j < (length - 1))
            else True)