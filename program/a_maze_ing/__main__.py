from a_maze_ing import config_file, Shell
import argparse


# def main() -> int:
#     parser = argparse.ArgumentParser()
#     parser.add_argument("config", nargs="?", type=config_file,
#                         help="Maze configuration file")

#     args = parser.parse_args()
#     shell = Shell()
#     try:
#         if args.config:
#             shell.init_shell(fpath=args.config)
#         else:
#             shell.init_shell()
#         shell.shell()
#     except Exception as e:
#         print(f"{RED}Error: {e}{DEFAULT}")
#         return 1
#     return 0

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", nargs="?", type=config_file,
                        help="Maze configuration file")

    args = parser.parse_args()
    shell = Shell()
    if args.config:
        shell.init_shell(fpath=args.config)
    else:
        shell.init_shell()
    shell.shell()
    return 0


if __name__ == "__main__":
    main()
