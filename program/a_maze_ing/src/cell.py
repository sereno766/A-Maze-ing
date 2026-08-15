class Cell:
    """A single maze cell.

    Stores its own position, its wall state as a 4-bit mask
    (N=1, E=2, S=4, W=8 -- bit set means the wall is closed), whether
    it has already been visited by the generation algorithm, and
    whether it belongs to the mandatory "42" pattern.
    """

    def __init__(self, x: int, y: int) -> None:
        """Create a new cell with all 4 walls closed.

        Args:
            x: Column index of the cell inside the maze grid.
            y: Row index of the cell inside the maze grid.
        """
        self.x = x
        self.y = y
        self.walls: int = 15  # all 4 walls closed (N=1, E=2, S=4, W=8)
        self.visited: bool = False
        self.is_42: bool = False
