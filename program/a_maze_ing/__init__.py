# mypy: ignore-errors
from .includes.clear import clear
from .checker.checker import checker
from .includes.colors import (DEFAULT, RED, GREEN, YLOW, PINK,
                              CYAN, INVERT, BOLD)
from .src.a_maze_ing import a_maze_ing

__all__ = [
    "clear", "checker",
    "DEFAULT", "RED", "GREEN", "YLOW", "PINK", "CYAN", "INVERT", "BOLD",
    "a_maze_ing",
]
