from a_maze_ing.includes.includes import DEFAULT, RED, GREEN, clear


class Render:
    """ASCII renderer for a generated maze.

    Turns the flat wall-mask grid produced by `Runner.run` into a
    colored, human-readable ASCII drawing -- with or without the
    shortest path highlighted -- for the interactive shell.
    """

    def __init__(self) -> None:
        """Declare the instance attributes, populated by `get_info`."""
        self.c_maze: str
        self.c_path: str
        self.c_ftp: str
        self.c_exit: str
        self.c_entry: str
        self.maze_grid: list[int | str]
        self.entry: tuple[int, int]
        self.exit: tuple[int, int]
        self.path: str
        self.maze: str
        self.maze_wpath: str

    def get_info(self, c_maze: str, c_path: str, c_ftp: str,
                 maze_grid: list[int | str], entry: tuple[int, int],
                 exit: tuple[int, int], path: str) -> None:
        """Store the maze data and colors, then render it immediately.

        Args:
            c_maze: ANSI color code for the walls.
            c_path: ANSI color code for the shortest path.
            c_ftp: ANSI color code for the "42" pattern.
            maze_grid: Flat wall-mask grid, as returned by
                `MazeRepresentation.return_maze_grid`.
            entry: (x, y) coordinates of the entry cell.
            exit: (x, y) coordinates of the exit cell.
            path: The shortest path as a string of "N"/"E"/"S"/"W".
        """
        self.c_maze = c_maze
        self.c_path = c_path
        self.c_ftp = c_ftp
        self.c_exit = RED
        self.c_entry = GREEN
        self.maze_grid = maze_grid
        self.entry = entry
        self.exit = exit
        self.path = path
        self.render_maze()

    @staticmethod
    def _to_row_col(xy: tuple[int, int]) -> tuple[int, int]:
        """Convert a Settings-style (x, y) coordinate to (row, col).

        Args:
            xy: An (x, y) coordinate, as used by `Settings`.

        Returns:
            The same position as a (row, col) tuple, matching the
            indexing used by `_grid_rows`.
        """
        x, y = xy
        return y, x

    def binary_to_wall(self, cell_nbr: int) -> str:
        """Decode a cell's wall mask into its closed-side letters.

        Args:
            cell_nbr: A cell's wall bitmask (N=1, E=2, S=4, W=8).

        Returns:
            The concatenation of the letters ("N", "E", "S", "W")
            for every side that is closed.
        """
        return "".join([
            "N" if cell_nbr & 1 else "",
            "E" if cell_nbr & 2 else "",
            "S" if cell_nbr & 4 else "",
            "W" if cell_nbr & 8 else "",
        ])

    def _grid_rows(self) -> list[list[str]]:
        """Split the flat maze grid into rows of wall-code strings.

        Returns:
            One list per maze row, each containing that row's cells
            as wall-code strings (e.g. "NESW", "NE", ...).
        """
        rows: list[list[str]] = []
        current: list[str] = []
        for item in self.maze_grid:
            if isinstance(item, str):
                rows.append(current)
                current = []
            else:
                current.append(self.binary_to_wall(item))
        if current:
            rows.append(current)
        return rows

    def _path_cells(self) -> set[tuple[int, int]]:
        """Walk `self.path` from the entry to collect every visited cell.

        Returns:
            The (row, col) coordinates of every cell on the
            shortest path, including entry and exit.
        """
        moves = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
        pos = self._to_row_col(self.entry)
        cells: set[tuple[int, int]] = {pos}
        for step in self.path:
            dr, dc = moves.get(step, (0, 0))
            pos = (pos[0] + dr, pos[1] + dc)
            cells.add(pos)
        return cells

    def render_cell(self, render_path: bool, path_type: int) -> str:
        """Return the glyph for a single path-related cell.

        Args:
            render_path: Whether the path should be drawn at all.
            path_type: 0 for the entry, 1 for the exit, anything
                else for a regular path cell.

        Returns:
            A single colored character (or a blank space if
            `render_path` is False).
        """
        if not render_path:
            return " "
        if path_type == 0:
            return f"{self.c_entry}█{DEFAULT}"
        if path_type == 1:
            return f"{self.c_exit}█{DEFAULT}"
        return f"{self.c_path}█{DEFAULT}"

    def _draw(self, rows: list[list[str]], with_path: bool) -> str:
        """Build the full ASCII drawing of the maze.

        Orchestrates the canvas init, cell/pattern/path/border
        drawing passes, one wall-thick canvas cell per maze wall.

        Args:
            rows: The maze grid, as returned by `_grid_rows`.
            with_path: Whether to highlight the shortest path.

        Returns:
            The complete drawing as a single multi-line string.
        """
        n_rows, n_cols = len(rows), len(rows[0]) if rows else 0
        height, width = n_rows * 2 + 1, n_cols * 2 + 1
        canvas = self._init_canvas(height, width)
        colors = self._get_colors()
        entry = self._to_row_col(self.entry)
        exit_ = self._to_row_col(self.exit)
        path_cells = self._path_cells() if with_path else set()
        self._draw_normal_cells(canvas, rows, entry, exit_,
                                path_cells, colors, with_path)
        self._draw_pattern_cells(canvas, rows, colors)
        if with_path:
            self._draw_path(canvas, rows, entry, exit_, path_cells, colors)
        self._draw_border(canvas, colors)
        return "\n".join("".join(row) for row in canvas)

    def _init_canvas(self, height: int, width: int) -> list[list[str]]:
        """Create a canvas fully filled with wall glyphs.

        Args:
            height: Canvas height, in characters.
            width: Canvas width, in characters.

        Returns:
            A `height` x `width` grid of the wall glyph, to be
            selectively cleared into corridors by the draw passes.
        """
        wall = f"{self.c_maze}█{DEFAULT}"
        return [[wall for _ in range(width)] for _ in range(height)]

    def _get_colors(self) -> dict[str, str]:
        """Build the glyph lookup table used by every draw pass.

        Returns:
            A dict mapping each role ("wall", "path", "ftp",
            "space", "entry", "exit") to its rendered glyph/color.
        """
        return {
            'wall': f"{self.c_maze}█{DEFAULT}",
            'path': f"{self.c_path}█{DEFAULT}",
            'ftp': f"{self.c_ftp}█{DEFAULT}",
            'space': " ",
            'entry': self.c_entry,
            'exit': self.c_exit,
        }

    def _draw_normal_cells(
        self, canvas: list[list[str]], rows: list[list[str]],
        entry: tuple[int, int], exit_: tuple[int, int],
        path_cells: set[tuple[int, int]], colors: dict[str, str],
        with_path: bool,
    ) -> None:
        """Carve every regular (non-"42") cell into the canvas, in place.

        Draws each cell's floor (entry/exit/path/space) and its
        four surrounding walls or openings.

        Args:
            canvas: The character grid being drawn into.
            rows: The maze grid, as returned by `_grid_rows`.
            entry: (row, col) of the entry cell.
            exit_: (row, col) of the exit cell.
            path_cells: (row, col) of every cell on the shortest
                path.
            colors: Glyph lookup table from `_get_colors`.
            with_path: Whether to highlight `path_cells`.
        """
        n_rows, n_cols = len(rows), len(rows[0])
        space, wall = colors['space'], colors['wall']
        for r in range(n_rows):
            for c in range(n_cols):
                walls = rows[r][c]
                if walls == "NESW":
                    continue
                cy, cx = 2 * r + 1, 2 * c + 1
                is_path = (r, c) in path_cells
                is_entry = (r, c) == entry
                is_exit = (r, c) == exit_
                if is_entry:
                    canvas[cy][cx] = f"{colors['entry']}█{DEFAULT}"
                elif is_exit:
                    canvas[cy][cx] = f"{colors['exit']}█{DEFAULT}"
                elif with_path and is_path:
                    canvas[cy][cx] = colors['path']
                else:
                    canvas[cy][cx] = space
                canvas[cy - 1][cx] = wall if "N" in walls else space
                canvas[cy][cx - 1] = wall if "W" in walls else space
                canvas[cy + 1][cx] = wall if "S" in walls else space
                canvas[cy][cx + 1] = wall if "E" in walls else space

    def _draw_pattern_cells(
        self, canvas: list[list[str]], rows: list[list[str]],
        colors: dict[str, str],
    ) -> None:
        """Paint the "42" pattern cells as solid 3x3 blocks, in place.

        Args:
            canvas: The character grid being drawn into.
            rows: The maze grid, as returned by `_grid_rows`.
            colors: Glyph lookup table from `_get_colors`.
        """
        n_rows, n_cols = len(rows), len(rows[0])
        ftp = colors['ftp']
        for r in range(n_rows):
            for c in range(n_cols):
                if rows[r][c] == "NESW":
                    cy, cx = 2 * r + 1, 2 * c + 1
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            canvas[cy + dr][cx + dc] = ftp

    def _draw_path(
        self, canvas: list[list[str]], rows: list[list[str]],
        entry: tuple[int, int], exit_: tuple[int, int],
        path_cells: set[tuple[int, int]], colors: dict[str, str],
    ) -> None:
        """Highlight the shortest path's cells and connecting openings.

        Args:
            canvas: The character grid being drawn into.
            rows: The maze grid, as returned by `_grid_rows`.
            entry: (row, col) of the entry cell (left unhighlighted,
                it keeps its own entry glyph).
            exit_: (row, col) of the exit cell (same as `entry`).
            path_cells: (row, col) of every cell on the shortest
                path.
            colors: Glyph lookup table from `_get_colors`.
        """
        n_rows, n_cols = len(rows), len(rows[0])
        path = colors['path']
        for r, c in path_cells:
            if not (0 <= r < n_rows and 0 <= c < n_cols):
                continue
            cy, cx = 2 * r + 1, 2 * c + 1
            walls = rows[r][c]
            if walls == "NESW":
                continue
            if (r, c) != entry and (r, c) != exit_:
                canvas[cy][cx] = path
            if ((r, c + 1) in path_cells
                    and c + 1 < n_cols
                    and "E" not in walls):
                canvas[cy][cx + 1] = path
            if ((r, c - 1) in path_cells
                    and c - 1 >= 0
                    and "W" not in walls):
                canvas[cy][cx - 1] = path
            if ((r + 1, c) in path_cells
                    and r + 1 < n_rows
                    and "S" not in walls):
                canvas[cy + 1][cx] = path
            if ((r - 1, c) in path_cells
                    and r - 1 >= 0
                    and "N" not in walls):
                canvas[cy - 1][cx] = path

    def _draw_border(
        self, canvas: list[list[str]], colors: dict[str, str]
    ) -> None:
        """Draw a decorative frame around the whole canvas, in place.

        Args:
            canvas: The character grid being drawn into.
            colors: Glyph lookup table from `_get_colors`.
        """
        height, width = len(canvas), len(canvas[0])
        frame = colors['wall']
        for x in range(width):
            canvas[0][x] = frame
            canvas[height - 1][x] = frame
        for y in range(height):
            canvas[y][0] = frame
            canvas[y][width - 1] = frame

    def set_path(self) -> str:
        """Render the maze with the shortest path highlighted.

        Returns:
            The drawing, as built by `_draw(rows, with_path=True)`.
        """
        rows = self._grid_rows()
        return self._draw(rows, with_path=True)

    def render_maze(self) -> None:
        """Pre-render both drawings (with and without the path).

        Populates `self.maze` and `self.maze_wpath`, so
        `print_maze` can switch between them instantly.
        """
        rows = self._grid_rows()
        self.maze = self._draw(rows, with_path=False)
        self.maze_wpath = self.set_path()

    def print_maze(self, print_path: bool) -> None:
        """Clear the terminal and print the pre-rendered maze.

        Args:
            print_path: Whether to print the path-highlighted
                drawing (`maze_wpath`) or the plain one (`maze`).
        """
        clear()
        if print_path:
            print(self.maze_wpath)
        else:
            print(self.maze)
