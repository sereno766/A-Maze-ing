from a_maze_ing.parser.parser import Settings


def validate_dimensions(settings: Settings) -> None:
    if settings.width <= 0 or settings.height <= 0:
        raise ValueError(
            "config.txt non-compliant: height and width values "
            "must be greater than 0."
        )

    entry_x, entry_y = settings.entry
    exit_x, exit_y = settings.exit

    if not (0 <= entry_x < settings.width and 0 <= entry_y < settings.height):
        raise ValueError(
            "config.txt non-compliant: the entry value must be "
            "positive and smaller than the maze dimensions."
        )

    if not (0 <= exit_x < settings.width and 0 <= exit_y < settings.height):
        raise ValueError(
            "config.txt non-compliant: the exit value must be "
            "positive and smaller than the maze dimensions."
        )

    if settings.entry == settings.exit:
        raise ValueError(
            "config.txt non-compliant: entry and exit must be distinct"
        )
