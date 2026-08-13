import random
from a_maze_ing.src.parser import parser_file
from a_maze_ing.src.maze import Maze
from pathlib import Path


def runner(fpath: Path = None) -> None:
    settings = parser_file(fpath)
    random.seed(settings.seed)
    print(f"settings: {settings}\n")
    maze = Maze(settings)
    maze.generator.generate()
    maze.representation.represent()
    maze.representation.debug_print()
