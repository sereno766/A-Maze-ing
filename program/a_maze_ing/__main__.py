from a_maze_ing import runner, config_file, RED, DEFAULT, Maze
import argparse


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", nargs="?", type=config_file,
                        help="Maze configuration file")

    args = parser.parse_args()

    try:
        if args.config:
            runner(fpath=args.config)
        else:
            runner()
    except Exception as e:
        print(f"{RED}Error: {e}{DEFAULT}")
        return 1
    return 0


if __name__ == "__main__":
    main()
    import random
    print(
        random.choice(["-L-", "-O-", "-N-", "-S-"]),
        random.choice(["-L-", "-O-", "-N-", "-S-"]),
        random.choice(["-L-", "-O-", "-N-", "-S-"])
    )
