# mypy: ignore-errors
from .includes.clear import clear
from .checker.checker import checker
from .includes.colors import (DEFAULT, RED, GREEN, YLOW, PINK,
                              CYAN, INVERT, BOLD)

__all__ = [
    "clear", "checker",
    "DEFAULT", "RED", "GREEN", "YLOW",
    "PINK", "CYAN", "INVERT", "BOLD",
]
