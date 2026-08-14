import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import cast
from a_maze_ing.src.seed import validate_seed, gen_seed
from a_maze_ing.includes.includes import gen_nbr, split_by


def parse_coord(value: str) -> tuple[int, int]:
    """Parse a "x,y" config value into an (x, y) integer tuple.

    Args:
        value: Raw string in the form "x,y" (e.g. "19,14").

    Returns:
        The parsed (x, y) coordinate.
    """
    x, y = value.split(",", 1)
    return int(x), int(y)


def parser_seed(value: str = "") -> str:
    """Normalize the raw SEED value read from the config file.

    Args:
        value: Raw SEED value from the config file, or "" if the
            SEED key was not present at all.

    Returns:
        The cleaned seed string, or the internal marker
        "not-setted" if the user did not provide one.
    """
    if value == "":
        return "not-setted"
    return value.replace('"', '')


PARSER = {
    "WIDTH": int,
    "HEIGHT": int,
    "ENTRY": parse_coord,
    "EXIT": parse_coord,
    "OUTPUT_FILE": str,
    "SEED": parser_seed,
    "PERFECT": lambda s: s == "True"
}


@dataclass
class Settings:
    """Fully parsed and validated maze configuration.

    Attributes:
        width: Maze width, in cells.
        height: Maze height, in cells.
        entry: (x, y) coordinates of the entry cell.
        exit: (x, y) coordinates of the exit cell.
        output: Path of the output file to write the maze to.
        seed: Seed used to make generation reproducible.
        perfect: Whether the maze must be a perfect maze (single
            path, no loops) or a Pac-Man-style board (loops allowed).
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output: str
    seed: str
    perfect: bool


def validate_dimensions(settings: dict) -> None:
    """Validate width/height/entry/exit consistency of a raw settings dict.

    Args:
        settings: Raw settings dict, as produced by `parser_settings`
            or `agc`.

    Raises:
        ValueError: If width/height are not positive, if entry or
            exit fall outside the maze bounds, or if entry and exit
            are the same cell.
    """
    width = settings.get("WIDTH")
    height = settings.get("HEIGHT")
    if width <= 0 or height <= 0:
        raise ValueError(
            "config.txt non-compliant: height and width values "
            "must be greater than 0."
        )

    entry_x, entry_y = settings.get("ENTRY")
    exit_x, exit_y = settings.get("EXIT")

    if not (0 <= entry_x < width and 0 <= entry_y < height):
        raise ValueError(
            "config.txt non-compliant: the entry value must be "
            "positive and smaller than the maze dimensions."
        )

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        raise ValueError(
            "config.txt non-compliant: the exit value must be "
            "positive and smaller than the maze dimensions."
        )

    if settings.get("ENTRY") == settings.get("EXIT"):
        raise ValueError(
            "config.txt non-compliant: entry and exit must be distinct"
        )


def gen_size(min: int, max: int) -> int:
    """Generate a random size strictly between `min` and `max`.

    Used by `agc` to build a random configuration.

    Args:
        min: Exclusive lower bound.
        max: Inclusive upper bound.

    Returns:
        A random integer in the (min, max] range.
    """
    size = int(gen_nbr(2))
    while size > max or size <= min:
        size = int(gen_nbr(2))
    return size


def agc() -> dict:
    """Auto-generate a random, valid configuration.

    Used when the program is run without a config file, as a
    convenience/demo mode.

    Returns:
        A raw settings dict, in the same shape as
        `parser_settings` would produce.
    """
    width = gen_size(min=15, max=25)
    height = gen_size(min=15, max=20)
    entry = split_by(gen_nbr(2), 1, 2)
    exit = split_by(gen_nbr(4), 0, 2)
    valid = False
    while not valid:
        if ((int(exit[0]) >= width or int(exit[0]) >= height)
           or (int(exit[1]) >= width or int(exit[1]) >= height)):
            exit = split_by(gen_nbr(4), 0, 2)
        else:
            valid = True
    seed = gen_seed(20)
    return dict(
        WIDTH=width,
        HEIGHT=height,
        ENTRY=entry,
        EXIT=exit,
        OUTPUT_FILE="maze.txt",
        SEED=seed,
        PERFECT=True
    )


def config_file(path: str) -> Path:
    """argparse `type=` helper: validate the config file argument.

    Args:
        path: Raw path string received from the command line.

    Returns:
        The validated Path.

    Raises:
        argparse.ArgumentTypeError: If the file does not have a
            .txt extension, or does not exist.
    """
    file = Path(path)

    if file.suffix != ".txt":
        raise argparse.ArgumentTypeError(
            "Configuration file must be a .txt extension")
    if not file.is_file():
        raise argparse.ArgumentTypeError(f"{file} not found in path!")
    return file


def parser_settings(path: Path) -> dict[str, object]:
    """Read a config.txt file into a raw settings dict.

    Each non-empty, non-comment line must follow the `KEY=VALUE`
    format. Every key is converted to its proper type using the
    `PARSER` dispatch table.

    Args:
        path: Path to the config.txt file.

    Returns:
        A dict mapping each config key to its converted value.

    Raises:
        ValueError: If a line is malformed, or references an
            unknown key.
    """
    settings: dict[str, object] = {}
    with path.open() as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if "=" not in line:
                raise ValueError(f"invalid line: '{line}'")
            key, value = line.split("=", 1)
            if key not in PARSER:
                raise ValueError(f"Unknown setting '{key}'")
            settings[key] = PARSER[key](value)
        if "SEED" not in settings:
            settings["SEED"] = PARSER["SEED"]("")
    return settings


def validate_settings(settings: dict) -> None:
    """Validate that every mandatory key is present, and resolve the seed.

    If the SEED key was not provided, a new one is generated and
    written back into `settings`. If it was provided, its format is
    validated.

    Args:
        settings: Raw settings dict, mutated in place.

    Raises:
        ValueError: If a mandatory key is missing, or the provided
            seed has an invalid format.
    """
    missing = PARSER.keys() - settings.keys()
    if missing:
        raise ValueError(f"Missing settings: {', '.join(sorted(missing))}")

    seed = settings.get("SEED")

    if seed == "not-setted":
        settings["SEED"] = gen_seed(20)
    elif not validate_seed(seed):
        raise ValueError(
            f"Seed '{seed}' is not valid, try to run "
            f"`python -m seed_generator` for a valid seed"
        )


def parser_file(fpath: Path = None) -> Settings:
    """Run the full config parsing pipeline and return a typed Settings.

    Args:
        fpath: Path to the config.txt file. If None, a random
            configuration is generated instead (see `agc`).

    Returns:
        A fully validated Settings instance.
    """
    if fpath:
        settings = parser_settings(fpath)
    else:
        settings = agc()
    validate_dimensions(settings)
    validate_settings(settings)
    return Settings(
        width=cast(int, settings["WIDTH"]),
        height=cast(int, settings["HEIGHT"]),
        entry=cast(tuple[int, int], settings["ENTRY"]),
        exit=cast(tuple[int, int], settings["EXIT"]),
        output=cast(str, settings["OUTPUT_FILE"]),
        seed=cast(str, settings["SEED"]),
        perfect=cast(bool, settings["PERFECT"])
    )
