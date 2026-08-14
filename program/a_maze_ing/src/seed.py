from a_maze_ing.includes.includes import gen_chars


def validate_seed(seed: str) -> bool:
    """Check whether a user-provided seed has a valid format.

    A valid seed is a non-empty alphanumeric string between 4 and 64
    characters long.

    Args:
        seed: The raw seed string read from the config file.

    Returns:
        True if the seed is valid, False otherwise.
    """
    if not seed:
        return False
    if not seed.isalnum():
        return False
    if not (4 <= len(seed) <= 64):
        return False
    return True


def gen_seed(amount: int) -> str:
    """Generate a new random alphanumeric seed.

    Args:
        amount: Number of characters the generated seed should have.

    Returns:
        A random alphanumeric string usable as a seed.
    """
    return gen_chars(amount)
