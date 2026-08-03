import random
from a_maze_ing import parser_file, Settings
from pathlib import Path


def runner(fpath: Path) -> Settings:
    settings = parser_file(fpath)
    random.seed(settings.seed)
    return settings
