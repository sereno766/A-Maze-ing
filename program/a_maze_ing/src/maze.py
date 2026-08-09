from a_maze_ing.src.parser import Settings
from a_maze_ing.src.cell import Cell
import random

class Maze:
    def __init__(self, setting: Settings):
        self.setting = setting
        self.representation = self.MazeRepresentation(setting)
        self.generator = self.MazeGenerator(self.representation)

    class MazeRepresentation:
        N: int = 1
        E: int = 2
        S: int = 4
        W: int = 8

        def __init__(self, setting: Settings):
            self.settings = setting
            self.width = self.settings.width
            self.height = self.settings.height
            self.grid = [
                [Cell(x, y) for x in range(self.width)]
                for y in range(self.height)
            ]

        def debug_print(self) -> None:
            for linha in self.grid:
                print([f"{celula.walls:2}" for celula in linha])

        def get_cell(self, x: int, y: int):
                return self.grid[y][x]

        def remove_wall(self, x1: int, y1: int, x2: int, y2: int,) -> None:
            cell_a = self.get_cell(x1, y1)
            cell_b = self.get_cell(x2, y2)
            if x2 == x1 and y2 == y1 - 1:
                direction_a, direction_b = self.N, self.S
            elif x2 == x1 and y2 == y1 + 1:
                direction_a, direction_b = self.S, self.N
            elif x2 == x1 + 1 and y2 == y1:
                direction_a, direction_b = self.E, self.W
            elif x2 == x1 - 1 and y2 == y1:
                direction_a, direction_b = self.W, self.E
            else:
                raise ValueError(
                    f"cells ({x1},{y1}) and ({x2},{y2}) are not adjacent"
                )
            cell_a.walls &= ~direction_a
            cell_b.walls &= ~direction_b
        #  y
        # x+x
        #  y

        # (x,y)
        # (0,0)(1,0)(2,0)
        # (0,1)(1,1)(2,1)
        # (0,2)(1,2)(2,2)

        def look_for_neighbors(self, x: int,
                            y: int) -> list[tuple[int, int] | None]:
            n = None if not self.is_valid_pos(x, y - 1) else (y - 1, x)
            s = None if not self.is_valid_pos(x, y + 1) else (y + 1, x)
            e = None if not self.is_valid_pos(x + 1, y) else (y, x + 1)
            w = None if not self.is_valid_pos(x - 1, y) else (y, x - 1)
            return [n, s, e, w]

        def represent(self) -> str:
            build_representation: list = []
            return "".join(build_representation)

        def is_valid_pos(self, x: int, y: int) -> bool:
            return (0 <= x < self.width and 0 <= y < self.height)


    class MazeGenerator:
        def __init__(self, representation):
            self.representation = representation

        def generate(self) -> None:
            rep = self.representation

            start_x, start_y = rep.settings.entry
            start = rep.get_cell(start_x, start_y)
            start.visited = True
            stack = [start]

            while stack:
                current = stack[-1]

                neighbors = rep.look_for_neighbors(current.x, current.y)
                candidates = []
                for n in neighbors:
                    if n is None:
                        continue
                    ny, nx = n
                    neighbors_cell = rep.get_cell(nx, ny)
                    if not neighbors_cell.visited and not neighbors_cell.is_42:
                        candidates.append(neighbors_cell)
                if candidates:
                    chosen = random.choice(candidates)
                    rep.remove_wall(current.x, current.y, chosen.x, chosen.y)
                    chosen.visited = True
                    stack.append(chosen)
                else:
                    stack.pop()
