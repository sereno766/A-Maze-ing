from a_maze_ing.src.parser import Settings
from a_maze_ing.src.cell import Cell
import random

from a_maze_ing import is_even
from random import sample

BINARY = {
    "0001": "1",
    "0010": "2",
    "0100": "4",
    "1000": "8",
    "0011": "3",
    "0101": "5",
    "1001": "9",
    "0111": "7",
    "1011": "k",
    "1111": "o",
    "1110": "n",
    "1101": "m",
    "0110": "6",
    "1010": "z",
    "1100": "l",
    "0000": "p"
}
#BINARY = {
#    "0001": "AQaq1!",
#    "0010": "BRbr2",
#    "0100": "DTdt4",
#    "1000": "HXhx8",
#    "0011": "CScs3#",
#    "0101": "EUeu5",
#    "1001": "IYiy9",
#    "0111": "GWgw7",
#    "1011": "Kk",
#    "1111": "Oo?",
#    "1110": "Nn",
#    "1101": "Mm",
#    "0110": "Vv6#",
#    "1010": "JZjz",
#    "1100": "Ll",
#    "0000": "Vp0"
#}
# BINARY = {
#     "0001": "⬛⬛⬛",
#     "0010": "⬛⬛⬛",
#     "0100": "⬛⬛⬛",
#     "1000": "⬛⬛⬛",
#     "0011": "⬛⬛⬛",
#     "0101": "⬛⬛⬛",
#     "1001": "⬛⬛⬛",
#     "0111": "⬛⬛⬛",
#     "1011": "⬛⬛⬛",
#     "1111": "⬛⬛⬛",
#     "1110": "⬛⬛⬛",
#     "1101": "⬛⬛⬛",
#     "0110": "⬛⬛⬛",
#     "1010": "⬛⬛⬛",
#     "1100": "⬛⬛⬛",
#     "0000": "⬛⬛⬛"
# }

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

        binary_list_placeholder = ["0001", "0010", "0100", "1000", "0011",
                                   "0101", "1001", "0111", "1011", "1111",
                                   "1110", "1101", "0110", "1010", "1100",
                                   "0000"]

        def __init__(self, setting: Settings):
            self.settings = setting
            self.width = self.settings.width
            self.height = self.settings.height
            self.grid = [
                [Cell(x, y) for x in range(self.width)]
                for y in range(self.height)
            ]
            self.make_pattern()

        def debug_print(self) -> None:
            for linha in self.grid:
                print([f"{celula.walls:2}" for celula in linha])
            print("-" * 42, end="\n\n\n")
            print(self.represent())

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

        def look_for_neighbors(
            self, x: int, y: int
        ) -> list[tuple[int, int] | None]:
            n = None if not self.is_valid_pos(x, y - 1) else (y - 1, x)
            s = None if not self.is_valid_pos(x, y + 1) else (y + 1, x)
            e = None if not self.is_valid_pos(x + 1, y) else (y, x + 1)
            w = None if not self.is_valid_pos(x - 1, y) else (y, x - 1)
            return [n, s, e, w]


        #  y
        # x+x
        #  y

        # (y,x)
        # (0,0)(0,1)(0,2)
        # (1,0)(1,1)(1,2)
        # (2,0)(2,1)(2,2)

        #  f   fff
        #  f     f
        #  fff fff
        #    f f
        #    f fff

        @staticmethod
        def get_coords(init_x: int, init_y: int) -> list[tuple]:
            mapped = [
                    (0, 0), (0, 4), (0, 5), (0, 6),
                    (1, 0), (1, 6),
                    (2, 0), (2, 1), (2, 2), (2, 4), (2, 5), (2,6),
                    (3, 2), (3, 4),
                    (4, 2), (4, 4), (4, 5), (4, 6)
                    ]
            coords = list()
            for y, x in mapped:
                tup = (init_y + y, init_x + x)
                coords.append(tup)
            return coords

        def make_pattern(self) -> None:
            if self.width <= 12:
                return
            init_ft_x = int((self.width / 2 - 4) if is_even(self.width)
                            else ((self.width - 1) / 2 - 3))
            init_ft_y = int((self.height / 2 - 3) if is_even(self.height)
                            else ((self.height - 1) / 2 - 2))
            ft_coords = self.get_coords(init_ft_x, init_ft_y)
            for y, x in ft_coords:
                if self.is_valid_pos(x, y):
                    self.get_cell(x, y).is_42 = True


        def wall_to_binary(self, walls: int) -> str:
            return "".join([
                "1" if walls & self.N else "0",
                "1" if walls & self.E else "0",
                "1" if walls & self.S else "0",
                "1" if walls & self.W else "0",
                ])

        def get_hexbit(self, cell: Cell) -> str:
            binary_built = self.wall_to_binary(cell.walls)
            to_choose = BINARY[binary_built]
            #return sample(to_choose, 1)[0]
            return to_choose

        def represent(self) -> str:
            build_representation = []
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.get_cell(x, y)
                    if cell.is_42:
                        to_append = "F"
                    else:
                        to_append = self.get_hexbit(cell)
                    build_representation.append(to_append)
                build_representation.append("\n")
            return "".join(build_representation)

        def is_valid_pos(self, x: int, y: int) -> bool:
            return (0 <= x < self.width and 0 <= y < self.height)

    class MazeGenerator:
        def __init__(self, representation):
            self.representation = representation

        def generate(self) -> None:
            rep = self.representation
            for row in rep.grid:
                for cell in row:
                    cell.visited = False
            self._carve_perfect_maze(rep)
            if not rep.settings.perfect:
                self._add_loops(rep, min_loops=2)

        def _carve_perfect_maze(self, rep) -> None:
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
                    neighbor_cell = rep.get_cell(nx, ny)
                    if not neighbor_cell.visited and not neighbor_cell.is_42:
                        candidates.append(neighbor_cell)
                if candidates:
                    chosen = random.choice(candidates)
                    rep.remove_wall(current.x, current.y, chosen.x, chosen.y)
                    chosen.visited = True
                    stack.append(chosen)
                else:
                    stack.pop()

        def _add_loops(self, rep, min_loops: int) -> None:
            dead_ends = [
                cell
                for row in rep.grid
                for cell in row
                if not cell.is_42 and self._open_wall_count(cell.walls) == 1
            ]
            random.shuffle(dead_ends)

            loops_created = 0
            for cell in dead_ends:
                if loops_created >= min_loops:
                    break

                neighbors = rep.look_for_neighbors(cell.x, cell.y)
                candidates = []
                for n in neighbors:
                    if n is None:
                        continue
                    ny, nx = n
                    neighbor = rep.get_cell(nx, ny)
                    if neighbor.is_42:
                        continue
                    if not self._already_connected(rep, cell, neighbor):
                        candidates.append(neighbor)

                if candidates:
                    chosen = random.choice(candidates)
                    rep.remove_wall(cell.x, cell.y, chosen.x, chosen.y)
                    loops_created += 1

        @staticmethod
        def _open_wall_count(walls: int) -> int:
            return 4 - bin(walls).count("1")

        @staticmethod
        def _already_connected(rep, cell_a, cell_b) -> bool:
            if cell_b.y == cell_a.y - 1:
                return cell_a.walls & rep.N == 0
            if cell_b.y == cell_a.y + 1:
                return cell_a.walls & rep.S == 0
            if cell_b.x == cell_a.x + 1:
                return cell_a.walls & rep.E == 0
            if cell_b.x == cell_a.x - 1:
                return cell_a.walls & rep.W == 0
            return False
