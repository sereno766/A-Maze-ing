from a_maze_ing.includes.includes import gen_nbr, gen_chars, split_by

def validate_seed(seed: str) -> bool:
    if not seed:
        return False
    if not seed.isalnum():
        return False
    if not (4 <= len(seed) <= 64)
        return False
    return True


def gen_seed(entry: list, exit: list, width: int, height: int) -> str:
    return gen_chars(20)
