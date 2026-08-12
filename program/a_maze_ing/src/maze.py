from a_maze_ing.src.parser import Settings
from a_maze_ing.src.cell import Cell
from collections import deque
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

        def look_for_neighbors(
            self, x: int, y: int
        ) -> list[tuple[int, int] | None]:
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

        def find_shortest_path(self) -> list[str]:
            start_x, start_y = self.settings.entry
            end_x, end_y = self.settings.exit
            start = self.get_cell(start_x, start_y)
            end = self.get_cell(end_x, end_y)

            visited = {start}
            predecessors = {}
            queue = deque([start])

            while queue:
                current = queue.popleft()

                if current is end:
                    break

                neighbors = self.look_for_neighbors(current.x, current.y)
                for n in neighbors:
                    if n is None:
                        continue
                    ny, nx = n
                    neighbor = self.get_cell(nx, ny)

                    if neighbor in visited:
                        continue

                    if not self._is_open(current, neighbor):
                        continue

                    visited.add(neighbor)
                    predecessors[neighbor] = current
                    queue.append(neighbor)

            path_cells = [end]
            current = end
            while current is not start:
                current = predecessors[current]
                path_cells.append(current)
            path_cells.reverse()

            return self._cells_to_directions(path_cells)

        def _is_open(self, cell_a, cell_b) -> bool:
            if cell_b.y == cell_a.y - 1:
                return cell_a.walls & self.N == 0
            if cell_b.y == cell_a.y + 1:
                return cell_a.walls & self.S == 0
            if cell_b.x == cell_a.x + 1:
                return cell_a.walls & self.E == 0
            if cell_b.x == cell_a.x - 1:
                return cell_a.walls & self.W == 0
            return False

        @staticmethod
        def _cells_to_directions(cells: list) -> list[str]:
            directions = []
            for a, b in zip(cells, cells[1:]):
                if b.y == a.y - 1:
                    directions.append("N")
                elif b.y == a.y + 1:
                    directions.append("S")
                elif b.x == a.x + 1:
                    directions.append("E")
                elif b.x == a.x - 1:
                    directions.append("W")
            return directions

        def write_output_file(self) -> None:
            with open(self.settings.output, "w") as file:
                for row in self.grid:
                    line = "".join(f"{cell.walls:X}" for cell in row)
                    file.write(line + "\n")

                entry_x, entry_y = self.settings.entry
                exit_x, exit_y = self.settings.exit
                path = "".join(self.find_shortest_path())

                file.write("\n")
                file.write(f"{entry_x},{entry_y}\n")
                file.write(f"{exit_x},{exit_y}\n")
                file.write(f"{path}\n")

    class MazeGenerator:
        def __init__(self, representation):
            self.representation = representation

        def generate(self) -> None:
            rep = self.representation
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
