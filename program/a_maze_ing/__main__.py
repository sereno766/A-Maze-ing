from a_maze_ing import runner, config_file, RED, DEFAULT, gen_chars, gen_nbr, agc, gen_seed
import argparse


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=config_file,
                        help="Maze configuration file")

    args = parser.parse_args()

    try:
        settings = runner(fpath=args.config)
        print(f"settings: {settings}")
    except Exception as e:
        print(f"{RED}Error: {e}{DEFAULT}")
        return 1
    return 0


if __name__ == "__main__":
    main()
    import random
    print(random.random(), random.random(), random.random())
    # print(gen_chars(50))
    # print(gen_nbr(3))
    # print(agc())
    # gen_seed()
