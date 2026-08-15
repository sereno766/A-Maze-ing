from typing import Any
from a_maze_ing.src.runner import Runner
from a_maze_ing.includes.includes import clear
from pathlib import Path
from a_maze_ing.includes.includes import GREEN, WHITE, BOLD, DEFAULT, RED
from a_maze_ing.includes.includes import YLOW, PINK, BLUE, CYAN
from a_maze_ing.src.render import Render

OPTIONS = """1.  Re-generate a new maze
2.  Show or hide the shortest path
3.  Change colors
4.  Quit"""

NO_MAZE = "No maze generated yet. Use option 1 to generate one."


class Shell:
    """Interactive terminal menu driving maze generation and display.

    Ties together `Runner` (parse + generate + write), `Render`
    (ASCII drawing), and a simple numbered-menu loop offering
    regeneration, path toggling, and color rotation.
    """

    def __init__(self) -> None:
        """Create the shell with its own `Runner` and `Render` instances."""
        self.runner = Runner()
        self.render = Render()
        self.fpath: Path | None = None

    def init_shell(self, fpath: Path | None = None) -> None:
        """Record the config file to use for every future generation.

        Args:
            fpath: Path to the config.txt file, or None to let
                `Runner`/`parser_file` decide (currently always
                required -- see `parser_file`).
        """
        print("shell initiated!")
        self.fpath = fpath

    def get_info(
        self, maze_info: dict[str, Any]
    ) -> tuple[list[int | str], str, tuple[int, int], tuple[int, int]]:
        """Unpack a `Runner.run` result into its four components.

        Args:
            maze_info: The dict returned by `Runner.run`.

        Returns:
            A `(maze_grid, path, entry, exit)` tuple.
        """
        maze = maze_info["maze_grid"]
        path = maze_info["maze_path"]
        entry = maze_info["entry"]
        exit_ = maze_info["exit"]
        return maze, path, entry, exit_

    @staticmethod
    def colorize(color_code: int) -> tuple[int, str, str, str]:
        """Advance to the next colour scheme in a fixed 3-way rotation.

        Args:
            color_code: The current scheme index. Any value outside
                `[0, 1]` wraps back around to scheme 0 (this also
                makes the very first call, with an out-of-range
                "priming" value, resolve to scheme 0).

        Returns:
            A `(new_code, maze_color, path_color, pattern_color)`
            tuple for the next scheme in the rotation.
        """
        maze_colors = {
            0: YLOW,
            1: PINK,
            2: CYAN,
        }
        path_colors = {
            0: BLUE,
            1: YLOW,
            2: PINK
        }
        ftp_colors = {
            0: GREEN,
            1: BLUE,
            2: YLOW
        }
        if color_code >= 2 or color_code < 0:
            color_code = 0
        else:
            color_code += 1
        nw_maze_c = maze_colors[color_code]
        nw_path_c = path_colors[color_code]
        nw_ftp_c = ftp_colors[color_code]
        return color_code, nw_maze_c, nw_path_c, nw_ftp_c

    @staticmethod
    def define_show_path(actual_definition: bool) -> bool:
        """Toggle the "show shortest path" flag.

        Args:
            actual_definition: The current flag value.

        Returns:
            The opposite of `actual_definition`.
        """
        return False if actual_definition else True

    def shell(self) -> None:
        """Run the interactive menu loop until the user quits.

        Repeatedly prompts for a choice (1: regenerate, 2: toggle
        path, 3: rotate colors, 4: quit), re-rendering the maze
        after every action. Never raises -- generation and
        rendering errors are caught and reported inline.
        """
        print("shell opened")
        c_code, c_maze, c_path, c_ftp = self.colorize(3)
        cmd = 1
        show_path = False
        maze = None
        m_path = None
        m_entry = None
        m_exit = None
        first_run = True
        run = True
        while run:
            if not first_run:
                print(f"{BOLD}=== A-Maze-ing ==={DEFAULT}")
                print(f"{WHITE}{OPTIONS}{DEFAULT}")
                entry = input(f"{GREEN}Choice? (1-4): {DEFAULT}")
                try:
                    cmd = int(entry)
                except ValueError:
                    clear()
                    print(f"{RED}Choice is not an integer!{DEFAULT}")
                    continue
            first_run = False
            match cmd:
                case 1:
                    clear()
                    try:
                        maze_info = self.runner.run(
                            self.fpath if self.fpath else None)
                    except Exception as e:
                        clear()
                        print(f"{RED}Error: {e}{DEFAULT}")
                        continue
                    maze, m_path, m_entry, m_exit = self.get_info(maze_info)
                    self.render.get_info(c_maze, c_path, c_ftp, maze,
                                         m_entry, m_exit, m_path)
                case 2:
                    clear()
                    try:
                        show_path = self.define_show_path(show_path)
                    except Exception:
                        clear()
                        print(f"{RED}Error rendering maze!{DEFAULT}")
                case 3:
                    clear()
                    if (maze is None or m_entry is None
                            or m_exit is None or m_path is None):
                        print(f"{RED}{NO_MAZE}{DEFAULT}")
                        continue
                    try:
                        c_code, c_maze, c_path, c_ftp = self.colorize(c_code)
                        self.render.get_info(c_maze, c_path, c_ftp, maze,
                                             m_entry, m_exit, m_path)
                    except Exception:
                        clear()
                        print(f"{RED}Error rendering maze!{DEFAULT}")
                case 4:
                    clear()
                    print("Exiting render shell...")
                    break
                case _:
                    clear()
                    print(f"{RED}Invalid command{DEFAULT}")
            if maze is not None:
                self.render.print_maze(show_path)
            else:
                print(f"{RED}{NO_MAZE}{DEFAULT}")
