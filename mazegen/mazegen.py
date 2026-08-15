"""mazegen - a reusable, standalone maze generator.

Generates a random grid maze using a recursive-backtracker algorithm,
either "perfect" (a spanning tree: exactly one path between any two
cells) or "braided" (extra loops added, so the board is directly
usable as a Pac-Man-like level). It has no dependency on any other
project -- everything needed lives in this single module.

Wall encoding (matches the a_maze_ing project's own output format,
one hexadecimal digit per cell, bit set means the wall is closed)::

    N = 1   E = 2   S = 4   W = 8

Example:
    Basic usage, with a custom size and a reproducible seed::

        >>> from mazegen import MazeGenerator
        >>> gen = MazeGenerator(
        ...     width=10, height=10,
        ...     entry=(0, 0), exit=(9, 9),
        ...     perfect=True, seed="abc123",
        ... )
        >>> gen.generate()
        >>> gen.wall_at(0, 0)          # closed walls of the entry cell
        9
        >>> gen.shortest_path()        # one valid solution
        ['E', 'E', 'S', ...]

    Accessing the raw generated structure (a 2D grid of :class:`Cell`)::

        >>> cell = gen.grid[0][0]      # grid[y][x]
        >>> cell.walls, cell.is_pattern
        (9, False)
"""

from __future__ import annotations

import random
from collections import deque

__all__ = ["Cell", "MazeGenerator", "N", "E", "S", "W"]

N: int = 1
E: int = 2
S: int = 4
W: int = 8

_OPPOSITE = {N: S, S: N, E: W, W: E}
_LETTER = {N: "N", S: "S", E: "E", W: "W"}

# Offsets (dx, dy) of the cells forming the mandatory "42" pattern,
# relative to its top-left corner.
_PATTERN_CELLS = [
    (0, 0), (4, 0), (5, 0), (6, 0),
    (0, 1), (6, 1),
    (0, 2), (1, 2), (2, 2), (4, 2), (5, 2), (6, 2),
    (2, 3), (4, 3),
    (2, 4), (4, 4), (5, 4), (6, 4),
]
_PATTERN_MIN_SIZE = 12


class Cell:
    """A single maze cell.

    Attributes:
        x: Column index inside the maze grid.
        y: Row index inside the maze grid.
        walls: 4-bit mask of closed walls (``N=1, E=2, S=4, W=8``).
            Starts fully closed (``15``).
        visited: Set by the generation algorithm while carving.
        is_pattern: Whether this cell belongs to the mandatory "42"
            pattern (and is therefore never carved into).
    """

    __slots__ = ("x", "y", "walls", "visited", "is_pattern")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = N | E | S | W
        self.visited = False
        self.is_pattern = False


class MazeGenerator:
    """Generates and holds one maze grid.

    Args:
        width: Maze width, in cells. Must be > 0.
        height: Maze height, in cells. Must be > 0.
        entry: ``(x, y)`` coordinates of the entry cell.
        exit: ``(x, y)`` coordinates of the exit cell. Must differ
            from ``entry``.
        perfect: If True (default), carve a perfect maze (a single
            path between any two cells, no loops). If False, extra
            loops are added afterwards so the board is directly
            usable as a Pac-Man-like level.
        seed: Optional seed for reproducible generation. Any value
            accepted by :class:`random.Random`.
        pattern: If True (default), reserve the cells that draw the
            mandatory "42" pattern. Automatically skipped -- with a
            console message -- when the maze is too small to fit it.

    Raises:
        ValueError: If the dimensions, entry or exit are invalid.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool = True,
        seed: int | float | str | bytes | bytearray | None = None,
        pattern: bool = True,
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be greater than 0")
        self.width = width
        self.height = height
        if not self._in_bounds(*entry):
            raise ValueError(f"entry {entry} is outside the maze bounds")
        if not self._in_bounds(*exit):
            raise ValueError(f"exit {exit} is outside the maze bounds")
        if entry == exit:
            raise ValueError("entry and exit must be distinct")

        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self._rng = random.Random(seed)
        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(width)] for y in range(height)
        ]
        self._generated = False
        if pattern:
            self._mark_pattern()

    # -- public API ---------------------------------------------------- #
    def generate(self) -> None:
        """Carve the maze layout into :attr:`grid`.

        Always carves a perfect maze first, then -- unless
        :attr:`perfect` is True -- adds extra loops so the result is
        usable as a Pac-Man-like board. Safe to call again to
        re-generate a fresh layout with the same settings.
        """
        for row in self.grid:
            for cell in row:
                cell.visited = False
                if not cell.is_pattern:
                    cell.walls = N | E | S | W
        self._carve_perfect_maze()
        if not self.perfect:
            self._add_loops(min_loops=2)
        self._generated = True

    def wall_at(self, x: int, y: int) -> int:
        """Return the 4-bit closed-wall mask of the cell at ``(x, y)``."""
        return self.grid[y][x].walls

    def is_pattern_cell(self, x: int, y: int) -> bool:
        """Whether ``(x, y)`` belongs to the mandatory "42" pattern."""
        return self.grid[y][x].is_pattern

    def shortest_path(self) -> list[str]:
        """Compute a shortest solution from :attr:`entry` to :attr:`exit`.

        Returns:
            The path as a list of direction letters ("N", "E", "S",
            "W"), one per step.

        Raises:
            RuntimeError: If called before :meth:`generate`, or if
                the exit is unreachable from the entry.
        """
        if not self._generated:
            raise RuntimeError("call generate() before shortest_path()")

        start = self.grid[self.entry[1]][self.entry[0]]
        goal = self.grid[self.exit[1]][self.exit[0]]

        visited = {start}
        predecessors: dict[Cell, Cell] = {}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current is goal:
                break
            for nx, ny in self._neighbors(current.x, current.y):
                neighbor = self.grid[ny][nx]
                if neighbor in visited or not self._is_open(current, neighbor):
                    continue
                visited.add(neighbor)
                predecessors[neighbor] = current
                queue.append(neighbor)

        if goal is not start and goal not in predecessors:
            raise RuntimeError("exit is unreachable from entry")

        path = [goal]
        current = goal
        while current is not start:
            current = predecessors[current]
            path.append(current)
        path.reverse()
        return self._cells_to_directions(path)

    # -- internals: grid helpers ---------------------------------------- #
    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        candidates = [(x, y - 1), (x, y + 1), (x + 1, y), (x - 1, y)]
        return [(nx, ny) for nx, ny in candidates if self._in_bounds(nx, ny)]

    def _direction(self, x1: int, y1: int, x2: int, y2: int) -> int:
        if x2 == x1 and y2 == y1 - 1:
            return N
        if x2 == x1 and y2 == y1 + 1:
            return S
        if x2 == x1 + 1 and y2 == y1:
            return E
        if x2 == x1 - 1 and y2 == y1:
            return W
        raise ValueError(f"cells ({x1},{y1}) and ({x2},{y2}) are not adjacent")

    def _open_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        direction = self._direction(x1, y1, x2, y2)
        self.grid[y1][x1].walls &= ~direction
        self.grid[y2][x2].walls &= ~_OPPOSITE[direction]

    def _is_open(self, cell_a: Cell, cell_b: Cell) -> bool:
        direction = self._direction(cell_a.x, cell_a.y, cell_b.x, cell_b.y)
        return cell_a.walls & direction == 0

    @staticmethod
    def _open_wall_count(walls: int) -> int:
        return 4 - bin(walls).count("1")

    @staticmethod
    def _cells_to_directions(cells: list[Cell]) -> list[str]:
        directions = []
        for a, b in zip(cells, cells[1:]):
            if b.y == a.y - 1:
                directions.append(_LETTER[N])
            elif b.y == a.y + 1:
                directions.append(_LETTER[S])
            elif b.x == a.x + 1:
                directions.append(_LETTER[E])
            elif b.x == a.x - 1:
                directions.append(_LETTER[W])
        return directions

    # -- internals: generation ------------------------------------------ #
    def _carve_perfect_maze(self) -> None:
        start = self.grid[self.entry[1]][self.entry[0]]
        start.visited = True
        stack = [start]

        while stack:
            current = stack[-1]
            candidates = [
                self.grid[ny][nx]
                for nx, ny in self._neighbors(current.x, current.y)
                if not self.grid[ny][nx].visited
                and not self.grid[ny][nx].is_pattern
            ]
            if candidates:
                chosen = self._rng.choice(candidates)
                self._open_wall(current.x, current.y, chosen.x, chosen.y)
                chosen.visited = True
                stack.append(chosen)
            else:
                stack.pop()

    def _add_loops(self, min_loops: int) -> None:
        dead_ends = [
            cell
            for row in self.grid
            for cell in row
            if not cell.is_pattern and self._open_wall_count(cell.walls) == 1
        ]
        self._rng.shuffle(dead_ends)

        loops_created = 0
        for cell in dead_ends:
            if loops_created >= min_loops:
                break
            candidates = [
                self.grid[ny][nx]
                for nx, ny in self._neighbors(cell.x, cell.y)
                if not self.grid[ny][nx].is_pattern
                and not self._is_open(cell, self.grid[ny][nx])
            ]
            if candidates:
                chosen = self._rng.choice(candidates)
                self._open_wall(cell.x, cell.y, chosen.x, chosen.y)
                loops_created += 1

    def _mark_pattern(self) -> None:
        if self.width <= _PATTERN_MIN_SIZE or self.height <= _PATTERN_MIN_SIZE:
            print(
                "mazegen: maze too small for the '42' pattern "
                f"({self.width}x{self.height}, need > {_PATTERN_MIN_SIZE} "
                "on both sides); omitting it."
            )
            return

        off_x = int(
            (self.width / 2 - 4) if self.width % 2 == 0
            else ((self.width - 1) / 2 - 3)
        )
        off_y = int(
            (self.height / 2 - 3) if self.height % 2 == 0
            else ((self.height - 1) / 2 - 2)
        )
        coords = [(off_x + dx, off_y + dy) for dx, dy in _PATTERN_CELLS]

        if self.entry in coords or self.exit in coords:
            raise ValueError("entry/exit cannot fall inside the '42' pattern")

        for x, y in coords:
            if self._in_bounds(x, y):
                self.grid[y][x].is_pattern = True
