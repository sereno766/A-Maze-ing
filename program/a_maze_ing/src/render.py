from a_maze_ing.includes.includes import DEFAULT, RED, GREEN, clear

class Render:
    def __init__(self):
        self.maze_c: str
        self.path_c: str
        self.ftp_c: str
        self.maze_grid: list
        self.entry: tuple
        self.exit: tuple
        self.path: str
        self.maze: str
        self.maze_wpath: str

    visual_base = {
        1: "█",
        2: " "
    }

    def get_info(self, c_maze: str, c_path: str, c_ftp: str, maze_grid: list,
                 entry: tuple, exit: tuple, path: str) -> None:
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

    def binary_to_wall(self, cell_nbr: int) -> str:
        return "".join([
            "N" if cell_nbr & 1 else "",
            "E" if cell_nbr & 2 else "",
            "S" if cell_nbr & 4 else "",
            "W" if cell_nbr & 8 else "",
        ])

    def _grid_rows(self) -> list:
        """Transforma a lista plana (com '\n' como separador de linha) em
        uma lista de listas de códigos de parede (string N/E/S/W)."""
        rows = []
        current = []
        for item in self.maze_grid:
            if item == "\n":
                rows.append(current)
                current = []
            else:
                current.append(self.binary_to_wall(item))
        if current:
            rows.append(current)
        return rows

    def _path_cells(self) -> set:
        """Anda a partir de self.entry seguindo self.path (N/E/S/W)
        e devolve o conjunto de células (linha, coluna) do caminho."""
        moves = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
        pos = tuple(self.entry)
        cells = {pos}
        for step in self.path:
            dr, dc = moves.get(step, (0, 0))
            pos = (pos[0] + dr, pos[1] + dc)
            cells.add(pos)
        return cells

    def render_cell(self, render_path: bool, path_type: int) -> str:
        if not render_path:
            return self.visual_base[2]
        if path_type == 0:
            return f"{self.c_entry}{self.visual_base[1]}{DEFAULT}"
        if path_type == 1:
            return f"{self.c_exit}{self.visual_base[1]}{DEFAULT}"
        return f"{self.c_path}{self.visual_base[1]}{DEFAULT}"

    def _draw(self, rows: list, with_path: bool) -> str:
        """Método principal que orquestra o desenho"""
        n_rows, n_cols = len(rows), len(rows[0]) if rows else 0
        height, width = n_rows * 2 + 1, n_cols * 2 + 1
        canvas = self._init_canvas(height, width)
        colors = self._get_colors()
        entry, exit_ = tuple(self.entry), tuple(self.exit)
        path_cells = self._path_cells() if with_path else set()
        self._draw_normal_cells(canvas, rows, entry, exit_,
                                path_cells, colors, with_path)
        self._draw_pattern_cells(canvas, rows, colors)
        if with_path:
            self._draw_path(canvas, rows, entry, exit_, path_cells, colors)
        self._draw_border(canvas, colors)
        return "\n".join("".join(row) for row in canvas)

    def _init_canvas(self, height: int, width: int) -> list:
        """Inicializa o canvas com paredes"""
        wall = f"{self.c_maze}{self.visual_base[1]}{DEFAULT}"
        return [[wall for _ in range(width)] for _ in range(height)]

    def _get_colors(self) -> dict:
        """Retorna um dicionário com todas as cores"""
        return {
            'wall': f"{self.c_maze}{self.visual_base[1]}{DEFAULT}",
            'path': f"{self.c_path}{self.visual_base[1]}{DEFAULT}",
            'ftp': f"{self.c_ftp}{self.visual_base[1]}{DEFAULT}",
            'space': self.visual_base[2],
            'entry': self.c_entry,
            'exit': self.c_exit,
        }

    def _draw_normal_cells(self, canvas: list, rows: list, entry: tuple, 
                        exit_: tuple, path_cells: set, colors: dict, 
                        with_path: bool) -> None:
        """Desenha todas as células que NÃO são 15"""
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

    def _draw_pattern_cells(self, canvas: list,
                            rows: list, colors: dict) -> None:
        """Desenha as células 15 (padrão 42) - bloco 3x3 inteiro"""
        n_rows, n_cols = len(rows), len(rows[0])
        ftp = colors['ftp']
        for r in range(n_rows):
            for c in range(n_cols):
                if rows[r][c] == "NESW":
                    cy, cx = 2 * r + 1, 2 * c + 1
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            canvas[cy + dr][cx + dc] = ftp

    def _draw_path(self, canvas: list, rows: list, entry: tuple, 
                exit_: tuple, path_cells: set, colors: dict) -> None:
        """Desenha o caminho mais curto"""
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

    def _draw_border(self, canvas: list, colors: dict) -> None:
        """Desenha a borda decorativa"""
        height, width = len(canvas), len(canvas[0])
        frame = colors['ftp']
        for x in range(width):
            canvas[0][x] = frame
            canvas[height - 1][x] = frame
        for y in range(height):
            canvas[y][0] = frame
            canvas[y][width - 1] = frame

    def set_path(self) -> str:
        rows = self._grid_rows()
        return self._draw(rows, with_path=True)

    def render_maze(self) -> None:
        rows = self._grid_rows()
        self.maze = self._draw(rows, with_path=False)
        self.maze_wpath = self.set_path()

    def print_maze(self, print_path: bool) -> None:
        clear()
        if print_path:
            print(self.maze_wpath)
        else:
            print(self.maze)
        print(self.path)
