import random
from typing import Any
from a_maze_ing.src.parser import parser_file
from a_maze_ing.src.maze import Maze
from pathlib import Path


class Runner:
    """Runs the full pipeline: parse config, generate, write output."""

    def __init__(self) -> None:
        """Create a Runner -- stateless, every call to `run` is independent."""
        pass

    def run(self, fpath: Path | None = None) -> dict[str, Any]:
        """Parse, generate and write a maze, then return its info.

        Args:
            fpath: Path to the config.txt file. If None, a random
                valid configuration is generated instead.

        Returns:
            A dict with the flattened maze grid ("maze_grid") and
            the shortest solution path ("maze_path").
        """
        settings = parser_file(fpath)
        random.seed(settings.seed)
        maze = Maze(settings)
        maze.generator.generate()
        maze.representation.write_output_file()
        ret = {
            "maze_grid": maze.representation.return_maze_grid(),
            "maze_path": maze.representation.path_out,
            "entry": maze.representation.settings.entry,
            "exit": maze.representation.settings.exit
        }
        return ret
