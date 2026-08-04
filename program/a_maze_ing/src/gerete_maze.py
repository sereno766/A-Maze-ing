from a_maze_ing.parser.parser import Settings


class MazeGenerator:
    N = 1
    E = 2
    S = 4
    W = 8

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.width = settings.width
        self.height = settings.height

        self.grid = [[15 for x in range(self.width)] for y in range(self.height)]
        self.visited = [[False for x in range(self.width)] for y in range(self.height)]

    def debug_print(self) -> None:
        for linha in self.grid:
            print([f"{celula:2}" for celula in linha])

    def gerete(self) -> None:
        print("start maze gerete")