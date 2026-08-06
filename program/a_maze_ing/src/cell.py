class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = 15  # all 4 walls closed (N=1, E=2, S=4, W=8)
        self.visited = False
