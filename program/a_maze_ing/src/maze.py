from a_maze_ing.src.parser import Settings
from a_maze_ing.src.cell import Cell
from collections import deque
import random

from a_maze_ing import is_even


class Maze:
    """Top-level, reusable maze object.

    Wraps a :class:`MazeRepresentation` (the grid/state) and a
    :class:`MazeGenerator` (the generation algorithm) behind a single
    public class, as required for the reusable module.

    Example:
        >>> maze = Maze(settings)
        >>> maze.generator.generate()
        >>> maze.representation.write_output_file()
    """

    def __init__(self, setting: Settings) -> None:
        """Build a new, ungenerated maze from validated settings.

        Args:
            setting: Parsed and validated maze configuration.
        """
        self.setting = setting
        self.representation = self.MazeRepresentation(setting)
        self.generator = self.MazeGenerator(self.representation)

    class MazeRepresentation:
        """Grid-based state of the maze.

        Stores the maze as a 2D grid of :class:`Cell` objects and
        exposes helpers to query/mutate wall state, find neighbours,
        compute the shortest solution path, and write the output file.
        """

        N: int = 1
        E: int = 2
        S: int = 4
        W: int = 8

        def __init__(self, setting: Settings) -> None:
            """Create the grid, with every cell starting fully closed.

            Args:
                setting: Parsed and validated maze configuration.
            """
            self.settings = setting
            self.width = self.settings.width
            self.height = self.settings.height
            self.grid = [
                [Cell(x, y) for x in range(self.width)]
                for y in range(self.height)
            ]
            self.make_pattern()
            self.path_out = ""

        def debug_print(self) -> None:
            """Print the raw wall value of every cell, row by row.

            Debugging helper only -- not part of the required output
            format.
            """
            for linha in self.grid:
                print([f"{celula.walls:2}" for celula in linha])
            print("-" * 42, end="\n\n\n")
            print(self.represent())

        def get_cell(self, x: int, y: int) -> Cell:
            """Return the Cell stored at grid coordinates (x, y).

            Args:
                x: Column index.
                y: Row index.

            Returns:
                The Cell at that position.
            """
            return self.grid[y][x]

        def remove_wall(
            self, x1: int, y1: int, x2: int, y2: int,
        ) -> None:
            """Open the wall between two directly adjacent cells.

            Opens the matching wall on both cells at once, keeping
            the shared-wall encoding coherent on both sides.

            Args:
                x1: Column of the first cell.
                y1: Row of the first cell.
                x2: Column of the second cell.
                y2: Row of the second cell.

            Raises:
                ValueError: If the two cells are not direct
                    neighbours.
            """
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
            """Return the 4 potential neighbours of a cell.

            Args:
                x: Column index of the cell.
                y: Row index of the cell.

            Returns:
                A list of 4 items, in [North, South, East, West]
                order. Each item is either a (y, x) tuple for a
                neighbour that falls inside the grid, or None if
                that direction is out of bounds.
            """
            n = None if not self.is_valid_pos(x, y - 1) else (y - 1, x)
            s = None if not self.is_valid_pos(x, y + 1) else (y + 1, x)
            e = None if not self.is_valid_pos(x + 1, y) else (y, x + 1)
            w = None if not self.is_valid_pos(x - 1, y) else (y, x - 1)
            return [n, s, e, w]

        @staticmethod
        def get_coords(init_x: int, init_y: int) -> list[tuple[int, int]]:
            mapped = [
                    (0, 0), (0, 4), (0, 5), (0, 6),
                    (1, 0), (1, 6),
                    (2, 0), (2, 1), (2, 2), (2, 4), (2, 5), (2, 6),
                    (3, 2), (3, 4),
                    (4, 2), (4, 4), (4, 5), (4, 6)
                    ]
            coords: list[tuple[int, int]] = []
            for y, x in mapped:
                tup = (init_y + y, init_x + x)
                coords.append(tup)
            return coords

        def make_pattern(self) -> None:
            init_ft_x = int((self.width / 2 - 4) if is_even(self.width)
                            else ((self.width - 1) / 2 - 3))
            init_ft_y = int((self.height / 2 - 3) if is_even(self.height)
                            else ((self.height - 1) / 2 - 2))
            ft_coords = self.get_coords(init_ft_x, init_ft_y)
            if self.width <= 12 or self.height <= 12:
                return
            for y, x in ft_coords:
                if self.is_valid_pos(x, y):
                    self.get_cell(x, y).is_42 = True

        def get_hexbit(self, cell: Cell) -> str:
            if cell.is_42:
                return "F"
            return "".join(f"{cell.walls:X}")

        def represent(self) -> str:
            """Build the maze's hexadecimal text representation.

            Returns:
                One hexadecimal digit per cell (row by row, with a
                newline between rows), as required by the output
                file format.
            """
            build_representation = []
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.get_cell(x, y)
                    to_append = self.get_hexbit(cell)
                    build_representation.append(to_append)
                build_representation.append("\n")
            return "".join(build_representation)

        def is_valid_pos(self, x: int, y: int) -> bool:
            """Check whether (x, y) falls inside the grid bounds.

            Args:
                x: Column index to check.
                y: Row index to check.

            Returns:
                True if the position is inside the grid.
            """
            return (0 <= x < self.width and 0 <= y < self.height)

        def find_shortest_path(self) -> list[str]:
            """Compute the shortest path from entry to exit.

            Uses a breadth-first search, only moving through cells
            that already have an open wall between them.

            Returns:
                The path as a list of direction letters ("N", "E",
                "S", "W"), from entry to exit.
            """
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

        def _is_open(self, cell_a: Cell, cell_b: Cell) -> bool:
            """Check whether the wall between two adjacent cells is open.

            Args:
                cell_a: The reference cell.
                cell_b: A direct neighbour of `cell_a`.

            Returns:
                True if there is already an open passage between
                the two cells.
            """
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
            """Convert a list of consecutive cells into direction letters.

            Args:
                cells: A path, as an ordered list of adjacent Cell
                    objects.

            Returns:
                The same path expressed as a list of "N"/"E"/"S"/"W"
                letters, one per step.
            """
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
            """Write the maze to `settings.output`.

            Follows the subject's required format: one hexadecimal
            digit per cell (row by row), an empty line, then the
            entry coordinates, the exit coordinates, and the
            shortest solution path.
            """
            with open(self.settings.output, "w") as file:
                file.write(self.represent())

                entry_x, entry_y = self.settings.entry
                exit_x, exit_y = self.settings.exit
                path = "".join(self.find_shortest_path())
                self.path_out = path

                file.write("\n")
                file.write(f"{entry_x},{entry_y}\n")
                file.write(f"{exit_x},{exit_y}\n")
                file.write(f"{path}\n")

        def return_maze_grid(self) -> list[int | str]:
            maze_grid: list[int | str] = []
            for row in self.grid:
                for cell in row:
                    maze_grid.append(cell.walls)
                maze_grid.append("\n")
            return maze_grid

    class MazeGenerator:
        """Carves a maze into a given :class:`MazeRepresentation`.

        Uses a randomized recursive backtracker to build a perfect
        maze (a spanning tree, with zero loops), then optionally
        "braids" it by reconnecting dead-ends to create extra loops
        for the non-perfect (Pac-Man-style) mode.
        """

        def __init__(self, representation: "Maze.MazeRepresentation") -> None:
            """Store the representation this generator will carve into.

            Args:
                representation: The MazeRepresentation to generate
                    walls into.
            """
            self.representation = representation

        def generate(self) -> None:
            """Generate the maze layout.

            Always carves a perfect maze first. If
            `representation.settings.perfect` is False, extra loops
            are then added to satisfy the Pac-Man-style requirements.
            """
            rep = self.representation
            for row in rep.grid:
                for cell in row:
                    cell.visited = False
            self._carve_perfect_maze(rep)
            if not rep.settings.perfect:
                self._add_loops(rep, min_loops=2)

        def _carve_perfect_maze(self, rep: "Maze.MazeRepresentation") -> None:
            """Carve a perfect maze using a randomized recursive backtracker.

            Args:
                rep: The MazeRepresentation to carve into.
            """
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

        def _add_loops(
            self, rep: "Maze.MazeRepresentation", min_loops: int
        ) -> None:
            """Reduce dead-ends and add extra loops to a perfect maze.

            Finds dead-end cells (only one open wall) and tries to
            connect each one to an unconnected neighbour, until at
            least `min_loops` new loops have been created.

            Args:
                rep: The MazeRepresentation to modify.
                min_loops: Minimum number of independent loops to
                    create.
            """
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
            """Count how many of a cell's 4 walls are open.

            Args:
                walls: The cell's wall bitmask (0-15).

            Returns:
                The number of open walls (0 to 4).
            """
            return 4 - bin(walls).count("1")

        @staticmethod
        def _already_connected(
            rep: "Maze.MazeRepresentation", cell_a: Cell, cell_b: Cell
        ) -> bool:
            """Check whether two adjacent cells already have an open wall.

            Args:
                rep: The MazeRepresentation the cells belong to
                    (used for its N/E/S/W direction constants).
                cell_a: The reference cell.
                cell_b: A direct neighbour of `cell_a`.

            Returns:
                True if there is already a passage between the two
                cells.
            """
            if cell_b.y == cell_a.y - 1:
                return cell_a.walls & rep.N == 0
            if cell_b.y == cell_a.y + 1:
                return cell_a.walls & rep.S == 0
            if cell_b.x == cell_a.x + 1:
                return cell_a.walls & rep.E == 0
            if cell_b.x == cell_a.x - 1:
                return cell_a.walls & rep.W == 0
            return False
