import random
from a_maze_ing.src.parser import parser_file, Settings
from pathlib import Path


def runner(fpath: Path = None) -> Settings:
    """Run the full configuration pipeline for a maze.

    Parses (or auto-generates, if `fpath` is None) the configuration,
    validates it, and initializes the global random number generator
    with the resulting seed so that maze generation stays reproducible.

    Args:
        fpath: Path to the config.txt file. If None, a random valid
            configuration is generated instead.

    Returns:
        The validated Settings ready to be used to build a Maze.
    """
    settings = parser_file(fpath)
    random.seed(settings.seed)
    return settings
