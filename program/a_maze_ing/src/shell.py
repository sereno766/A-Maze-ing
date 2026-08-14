from a_maze_ing.src.runner import Runner
from a_maze_ing.includes.includes import clear
from pathlib import Path
from a_maze_ing.includes.includes import GREEN, WHITE, BOLD, DEFAULT, RED

OPTIONS = """1.  Re-generate a new maze
2.  Show or hide the shortest path 
3.  Change colors
4.  Quit"""

checks = [
    "invalid line:",
    "Unknown setting",
    "Missing settings:",
    "is not valid!"
]

class Shell:
    def __init__(self):
        self.runner = Runner()
        self.fpath: Path

    def init_shell(self, fpath: Path = None):
        print("shell initiated!")
        self.fpath = fpath

    def get_maze_info(self, maze_info: dict):
        maze = maze_info.get("maze_grid")
        path = maze_info.get("maze_path")
        return maze, path

    def shell(self):
        print("shell opened")
        cmd = 1
        while True:
            try:
                match cmd:
                    case 1:
                        clear()
                        try:
                            maze_info = self.runner.run(self.fpath if self.fpath else None)
                            maze, path = self.get_maze_info(maze_info)
                            if not maze:
                                continue
                            for i in maze:
                                print(f"[{'0' if len(str(i)) == 1 else ''}{i}]" if i != '\n' else '\n', end='')
                        except Exception as e:
                            print(f"{RED}Error: {e}{DEFAULT}")
                    case 2:
                        clear()
                        print("path")
                    case 3: #color 1 - 6
                        clear()
                        print("color")
                    case 4:
                        clear()
                        print("exiting")
                        break
                    case _:
                        clear()
                        print("command invalid")
                cmd = None
            except Exception as e:
                print(e)
                pass
            print(f"{BOLD}=== A-Maze-ing ==={DEFAULT}")
            print(f"{WHITE}{OPTIONS}{DEFAULT}")
            entry = input(f"{GREEN}Choice? (1-4): {DEFAULT}")
            try:
                cmd = int(entry)
            except Exception:
                print("Choice is not a integer!")