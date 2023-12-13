from backend.bunny_backend_functions import get_mazes, read_maze
from pprint import pprint

if __name__ == "__main__":
    mazes = get_mazes()
    print(*read_maze(mazes[2]), sep="\n")