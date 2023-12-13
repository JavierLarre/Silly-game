import param as p
from os.path import join
from itertools import product


def get_sprite_path(file_name: str):
    return join(*p.SPRITES_PATH, file_name)

def get_all_positions(maze: list):
    width = range(len(maze))
    length =range(len(maze[0]))
    return product(width, length)

def get_axis(direction: str) -> tuple:
    axis = (0 if (direction == "up" or direction == "down") else 1)
    i = (-1 if (direction == "up" or direction == "left") else 1)
    return (axis, i)