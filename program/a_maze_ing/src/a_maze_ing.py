import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import cast

def parse_coord(value: str) -> tuple[int, int]:
    x, y = value.split(",", 1)
    return int(x), int(y)

PARSER = {
    "WIDTH": int,
    "HEIGHT": int,
    "ENTRY": parse_coord,
    "EXIT": parse_coord,
    "OUTPUT_FILE": str,
    "PERFECT": lambda s: s == "True",
}

@dataclass
class Settings:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output: str
    perfect: bool


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
            settings[key] = PARSER[key](value)
    return settings


def validate_settings(settings: dict) -> None:
    missing = PARSER.keys() - settings.keys()
    if missing:
        raise ValueError(f"Missing settings: {', '.join(sorted(missing))}")


def parser_file(fpath: Path) -> Settings:
    settings = parser_settings(fpath)
    validate_settings(settings)
    return Settings(
        width=cast(int, settings["WIDTH"]),
        height=cast(int, settings["HEIGHT"]),
        entry=cast(tuple[int, int], settings["ENTRY"]),
        exit=cast(tuple[int, int], settings["EXIT"]),
        output=cast(str, settings["OUTPUT_FILE"]),
        perfect=cast(bool, settings["PERFECT"])
    )


def a_maze_ing() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", nargs="?", type=config_file,
                        help="Maze configuration file")

    args = parser.parse_args()

    if args.config is not None:
        settings = parser_file(args.config)
        print(f"settings: {settings}")
    return 0

a_maze_ing()
