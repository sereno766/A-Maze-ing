from a_maze_ing.src.parser import Settings
from a_maze_ing.src.cell import Cell

class MazeRepresentation:
    N: int = 1
    E: int = 2
    S: int = 4
    W: int = 8

    def __init__(self, settings: Settings):
        self.settings = settings
        self.width = settings.width
        self.height = settings.height
        self.grid = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def debug_print(self) -> None:
        for linha in self.grid:
            print([f"{celula.walls:2}" for celula in linha])

    def get_cell(self, x: int, y: int):
            return self.grid[y][x]

    #  y
    # x+x
    #  y

    # (x,y)
    # (0,0)(1,0)(2,0)
    # (0,1)(1,1)(2,1)
    # (0,2)(1,2)(2,2)

    def look_for_neighbors(self, x: int, y: int) -> None:
        n = None if not self.is_valid_pos(x, y - 1) else (y - 1, x)
        s = None if not self.is_valid_pos(x, y + 1) else (y - 1, x)
        e = None if not self.is_valid_pos(x + 1, y) else (y, x + 1)
        w = None if not self.is_valid_pos(x - 1, y) else (y, x - 1)
        return [n, s, e, w]

    def represent(self) -> str: #MINE
        build_representation: list = []
        return "".join(build_representation)

    def is_valid_pos(self, x: int, y: int) -> bool:
        return (0 <= x < self.width and 0 <= y < self.height)


class MazeGenerator:
    def __init__(self):
        pass

    def generate(self) -> None:
        print("starting to generate maze")

