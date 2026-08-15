# mazegen

Reusable maze generator, standalone from the `a_maze_ing` CLI project. Single
module (`mazegen.py`), one public class: `MazeGenerator`.

## Install

From the built package (at the root of the repository):

```bash
pip install ../mazegen-1.0.0-py3-none-any.whl
```

Or build it yourself from source:

```bash
cd mazegen
python -m pip install build
python -m build
```

## Usage

Instantiate with the maze size, entry/exit cells, and generate:

```python
from mazegen import MazeGenerator

gen = MazeGenerator(
    width=10, height=10,
    entry=(0, 0), exit=(9, 9),
    perfect=True,       # False -> braided/loopy, Pac-Man-style board
    seed="abc123",      # optional, for reproducible generation
)
gen.generate()
```

### Custom parameters

- `width`, `height`: maze size in cells (must be > 0).
- `entry`, `exit`: `(x, y)` coordinates, must be distinct and in bounds.
- `perfect`: `True` for a single-path maze (no loops), `False` for a
  playable board with at least two independent routes and rare dead-ends.
- `seed`: any value accepted by `random.Random`; same seed + same
  parameters always produce the same maze.
- `pattern`: set to `False` to skip reserving the "42" pattern cells.

### Accessing the generated structure and a solution

```python
cell = gen.grid[0][0]          # grid[y][x] -> Cell(x, y, walls, is_pattern)
gen.wall_at(0, 0)               # closed-wall bitmask (N=1, E=2, S=4, W=8)
gen.is_pattern_cell(0, 0)       # True if part of the mandatory "42" pattern
gen.shortest_path()             # e.g. ['E', 'E', 'S', ...] from entry to exit
```

This structure is **not** the same format as `a_maze_ing`'s output file --
it grants direct access to the grid of `Cell` objects instead.
