from a_maze_ing import checker, clear, RED, DEFAULT
import cowsay


def main() -> int:
    clear()
    print(RED, "HELLO", DEFAULT)
    checker()
    cowsay.cow("That is A... Maze.. ing")
    return 0


if __name__ == "__main__":
    main()
