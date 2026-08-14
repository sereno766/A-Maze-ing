import random
from a_maze_ing.src.parser import parser_file
from a_maze_ing.src.maze import Maze
from pathlib import Path

class Runner:
    def __init__(self):
        pass

    def run(self, fpath: Path = None) -> dict:
        settings = parser_file(fpath)
        random.seed(settings.seed)
        print(f"settings: {settings}\n")
        maze = Maze(settings)
        maze.generator.generate()
        maze.representation.represent()
        maze.representation.write_output_file()
        ret = {
            "maze_grid": maze.representation.return_maze_grid(),
            "maze_path": maze.representation.path_out
        }
        return ret
