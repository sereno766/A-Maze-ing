import random
from a_maze_ing.parser.parser import parser_file, Settings
from a_maze_ing.checker.validate_config_values import validate_dimensions
from pathlib import Path


def runner(fpath: Path = None) -> Settings:
    settings = parser_file(fpath)
    validate_dimensions(settings)
    random.seed(settings.seed)
    return settings
