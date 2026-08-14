import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import cast
from a_maze_ing.src.seed import validate_seed, gen_seed
from a_maze_ing.includes.includes import gen_nbr, split_by


def parse_coord(value: str) -> tuple[int, int]:
    x, y = value.split(",", 1)
    return int(x), int(y)


def parser_seed(value: str = "") -> str:
    # print("value received:", value)
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
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output: str
    seed: str
    perfect: bool


def validate_dimensions(settings: dict) -> None:
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
    size = int(gen_nbr(2))
    while size > max or size <= min:
        size = int(gen_nbr(2))
    return size


def agc() -> dict:
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
    file = Path(path)

    if file.suffix != ".txt":
        raise argparse.ArgumentTypeError(
            "Configuration file must be a .txt extension")
    if not file.is_file():
        raise argparse.ArgumentTypeError(f"{file} not found in path!")
    return file


def parser_settings(path: Path) -> dict[str, object]:
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
            # print(f"key: {key}, value: {value}")
            settings[key] = PARSER[key](value)
        if "SEED" not in settings:
            settings["SEED"] = PARSER["SEED"]("")
    return settings


def validate_settings(settings: dict) -> None:
    missing = PARSER.keys() - settings.keys()
    if missing:
        raise ValueError(f"Missing settings: {', '.join(sorted(missing))}")

    seed = settings.get("SEED")

    if seed == "not-setted":
        settings["SEED"] = gen_seed(20)
    elif not validate_seed(seed):
        raise ValueError(
            f"Seed '{seed}' is not valid!"
        )

def file_is_empty(path: Path = None) -> bool:
    with path.open() as file:
        for line in file:
            if line != "":
                return False
    return True

def validate_values(path: Path = None) -> bool:
    with path.open() as file:
        for line in file:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key in ("WIDTH", "HEIGHT"):
                try:
                    int(value)
                except ValueError:
                    raise ValueError(
                        f"{key} must be an integer"
                    )
            elif key in ("ENTRY", "EXIT"):
                try:
                    x, y = value.split(",", 1)
                    int(x)
                    int(y)
                except ValueError:
                    raise ValueError(
                        f"{key} must be in the format X,Y and must be integer"
                    )
            elif key == "PERFECT":
                if value not in ("True", "False"):
                    raise ValueError(
                        "PERFECT must be True or False"
                    )
            elif key == "SEED":
                value = value.replace('"', "")
                if value and not validate_seed(value):
                    raise ValueError(
                        f"Seed '{value}' is not valid!"
                    )
            elif key == "OUTPUT_FILE":
                if not value:
                    raise ValueError(
                        "OUTPUT_FILE cannot be empty"
                    )
    return True


def validate_file(path: Path = None) -> bool:
    settings_in_file = []
    valid_settings = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                      "OUTPUT_FILE", "PERFECT", "SEED"]
    with path.open() as file:
            for line in file:
                if "=" in line:
                    splited = line.split("=")
                    if not splited[1]:
                        raise ValueError(f"{splited[0]} is missing a value")
                    settings_in_file.append(splited[0])
    for i in settings_in_file:
        if i not in valid_settings:
            raise ValueError(f"{i} is not a valid setting")
    for j in valid_settings:
        if j not in settings_in_file:
            if j == "SEED":
                continue
            raise ValueError(f"{j} is missing in config.txt")
    if validate_values(path):
        return True
    return False

def parser_file(fpath: Path = None) -> Settings:
    if fpath:
        if file_is_empty(fpath):
            raise SyntaxError("config.txt is empty!")
        if validate_file(fpath):
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
