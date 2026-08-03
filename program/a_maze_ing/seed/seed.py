from a_maze_ing.includes.includes import gen_nbr, gen_chars, split_by

def validate_seed(seed: str) -> bool:
    if seed == "":
        return False
    return True


def gen_seed(entry: list, exit: list, width: int, height: int) -> str:
    chars = gen_chars(20)
    print(chars)
    lchars = split_by(chars, 10, 2)
    print(lchars)
    init = f"{entry[0]}{entry[1]}"
    end = f"{exit[0]}{exit[1]}"
    return f"{init}{lchars[0]}{width}{height}{lchars[1]}{end}"