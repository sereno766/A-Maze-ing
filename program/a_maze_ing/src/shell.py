from a_maze_ing.src.runner import Runner
from a_maze_ing.includes.includes import clear
from pathlib import Path

class Shell:
    def __init__(self):
        self.runner = Runner()
        self.fpath: Path

    def init_shell(self, fpath: Path = None):
        print("shell initiated!")
        self.fpath = fpath

    def shell(self):
        print("shell opened")
        sig_exit = False
        while not sig_exit:
            entry = input("Choice? (1-4): ")
            try:
                cmd = int(entry)
            except Exception:
                print("Choice is not a integer!")
                continue
            match cmd:
                case 1:
                    clear()
                    maze_info = self.runner.run(self.fpath)
                    print(maze_info)
                case 2:
                    print(maze_info)
                    clear()
                case 3:
                    print(maze_info)
                    clear()
                case 4:
                    clear()
                    print("exiting")
                    sig_exit = True
                case _:
                    clear()
                    print("command invalid")