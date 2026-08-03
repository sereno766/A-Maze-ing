import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import cast
from a_maze_ing.seed.seed import validate_seed, gen_seed


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
    # print(settings.keys())
    missing = PARSER.keys() - settings.keys()
    if missing:
        raise ValueError(f"Missing settings: {', '.join(sorted(missing))}")
    seed = settings.get("SEED")
    if not validate_seed(seed):
        raise ValueError(f"Seed '{settings.get("seed")}'",
                         "is not valid, try to run `python -m",
                         "seed_generator` for a valid seed")
    if seed == "not-setted":
        generated_seed = gen_seed(
            settings.get("ENTRY"),
            settings.get("EXIT"),
            settings.get("WIDTH"),
            settings.get("HEIGHT")
        )


def parser_file(fpath: Path) -> Settings:
    settings = parser_settings(fpath)
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
