import random
from a_maze_ing.parser.parser import parser_file, Settings
from pathlib import Path


def runner(fpath: Path = None) -> Settings:
    settings = parser_file(fpath)
    random.seed(settings.seed)
    return settings
