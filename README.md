*This project has been created as part of the 42 curriculum by smachado, vigomes-*

# A-MAZE-ING
*This is the way*

## DESCRIPTION

A-Maze-ing is a Python maze generator. Given a `config.txt` file, it builds a
grid-based maze (optionally a "perfect" maze with a single path between the
entry and the exit, or a Pac-Man-style board with multiple independent
routes), computes the shortest path between the entry and the exit, and
writes the result to a plain text file using a compact hexadecimal wall
encoding (one hex digit per cell). The maze generation logic is organized as
a standalone, reusable module (`Maze`) that can be imported and reused by
future projects independently of the CLI/config-parsing layer.

## INSTRUCTIONS

### Requirements
- Python 3.10+
- A virtual environment is recommended (`venv`)

### Setup
From the `program/` directory:
```bash
make init-venv        # creates the venv (uses python3 under the hood)
source venv/bin/activate        # bash/zsh
# or: source venv/bin/activate.fish   (fish shell)
make depend            # installs dependencies from requirements.txt
```

### Running
```bash
make run
# equivalent to:
python -m a_maze_ing config.txt
```
If no config file is given, a random valid configuration is generated
automatically.

### Linting
```bash
make lint          # flake8 + mypy (required flags)
make lint-strict    # flake8 + mypy --strict
```

### Cleaning up
```bash
make clean          # removes __pycache__ and .mypy_cache
make fclean          # clean + removes the venv
```

## CONFIGURATION FILE FORMAT

The configuration file is plain text, one `KEY=VALUE` pair per line. Lines
starting with `#` are comments and are ignored.

| Key | Description | Example |
| :--- | :--- | :--- |
| `WIDTH` | Maze width (number of cells) | `WIDTH=20` |
| `HEIGHT` | Maze height (number of cells) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output file name | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether the maze is perfect (`True`/`False`) | `PERFECT=True` |
| `SEED` | Optional. Reproducibility seed (alphanumeric, 4-64 chars) | `SEED=abc123` |

If `SEED` is omitted, a new random seed is generated automatically and used
for that run. `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE` and `PERFECT`
are mandatory; the program will refuse to run and print a clear error if any
of them is missing, malformed, or inconsistent (e.g. `ENTRY`/`EXIT` outside
the grid, or identical).

A default configuration file is available at `program/config.txt`.

## MAZE GENERATION ALGORITHM

The maze is generated with a **randomized recursive backtracker** (an
iterative, stack-based depth-first search):

1. Start at the `ENTRY` cell, mark it visited, push it on a stack.
2. Look at the cell on top of the stack. Among its unvisited, non-"42"
   neighbours, pick one at random, open the wall between the two cells, mark
   the neighbour visited, and push it.
3. If the current cell has no unvisited neighbour left, pop it off the stack
   (backtrack).
4. Repeat until the stack is empty.

This always produces a **perfect maze** (a spanning tree over the grid: full
connectivity, exactly one path between any two cells, zero loops), which
satisfies the `PERFECT=True` requirement directly.

When `PERFECT=False` (the default / Pac-Man mode), a second pass **braids**
the perfect maze: every dead-end cell (a cell with only one open wall) is
considered, and, when possible, reconnected to a neighbour it is not already
connected to, until at least two new independent loops have been created.
This keeps the maze fully connected, keeps dead-ends rare, and guarantees at
least two independent routes between any two points, as required for a
playable Pac-Man-style board.

### Why this algorithm

- It is simple to implement correctly and reason about, while still
  producing long, winding corridors (as opposed to, e.g., Prim's algorithm,
  which tends to produce shorter, more uniform corridors).
- Being a spanning-tree algorithm, it satisfies the "perfect maze" mode
  (zero loops) for free, with no extra bookkeeping.
- Turning a perfect maze into a playable, looped board by "braiding" its
  dead-ends is a well-known, minimal-effort technique that reuses the exact
  same perfect-maze output as its starting point, instead of requiring a
  second, unrelated algorithm for the non-perfect mode.

## REUSABLE CODE

The maze generation logic lives entirely in `program/a_maze_ing/src/maze.py`
and `program/a_maze_ing/src/cell.py`, with no dependency on the CLI,
`argparse`, or the config file parser. It is organized as a single public
class, `Maze`, wrapping two internal collaborators:

- `Maze.MazeRepresentation`: the grid of `Cell` objects, plus helpers to
  query/mutate walls, find neighbours, compute the shortest path
  (`find_shortest_path`), and write the output file (`write_output_file`).
- `Maze.MazeGenerator`: the generation algorithm itself (`generate`).

### Usage example

```python
from a_maze_ing import Settings, Maze

settings = Settings(
    width=20, height=15,
    entry=(0, 0), exit=(19, 14),
    output="maze.txt", seed="my-seed-123", perfect=False,
)

maze = Maze(settings)
maze.generator.generate()

# Access the generated structure directly:
cell = maze.representation.get_cell(0, 0)
print(cell.walls)      # 4-bit wall mask (N=1, E=2, S=4, W=8)

# Access a solution:
path = maze.representation.find_shortest_path()   # e.g. ["E", "E", "S", ...]

# Or reuse the same encoding the CLI writes to disk:
maze.representation.write_output_file()
```

Custom parameters (size, entry/exit, seed, perfect/non-perfect mode) are all
passed through the `Settings` dataclass shown above -- no config file is
required to use the module programmatically.

> Note: the in-memory structure (`Cell.walls`, a 4-bit mask per cell) is not
> the same format as the output file -- it is converted to a hex digit only
> when `write_output_file` is called.

This module is intended to be packaged separately as an installable
`mazegen-*` package (`.whl`/`.tar.gz`) at the root of the repository, as
required for reuse by future projects.

## RESOURCES

- [Wikipedia -- Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Jamis Buck -- "Maze Generation: Algorithm Recap"](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap) (overview and comparison of recursive backtracker, Prim's, Kruskal's, etc.)
- [Think Labyrinth -- Maze generation algorithms](https://www.astrolog.org/labyrnth/algrithm.htm)
- [Python `argparse` documentation](https://docs.python.org/3/library/argparse.html)
- [Python `collections.deque` documentation](https://docs.python.org/3/library/collections.html#collections.deque) (used for the BFS shortest-path queue)
- [PEP 257 -- Docstring Conventions](https://peps.python.org/pep-0257/)

### How AI was used

An AI assistant (Claude) was used mainly to research and understand
concepts needed for the project (bitwise operations, BFS, argparse,
RNG seeding, etc.), and to help write the code documentation -- the
docstrings across the modules and this README.

## TEAM AND PROJECT MANAGEMENT

### Roles
<!-- TODO: fill in each member's main area of ownership, e.g.:
- smachado: ...
- vigomes-...: ...
-->

### Planning
Tasks were tracked on a Kanban-style board (Backlog / In Progress),
broken down per feature (Seed System, Cell representation, Pathfinding,
Hex encoding/Export, ...), with sub-tasks as checklists on each card.
<!-- TODO: describe how the plan evolved -- e.g. which estimates changed,
what got reprioritized, and why. -->

### What worked well / what could be improved
<!-- TODO: short retrospective from the team. -->

### Tools used
- **Git** (feature branches per component, e.g. `maze_ger`,
  `maze_representation`, merged into `main`)
- A **Kanban board** (Trello-style) for task tracking
- **flake8** and **mypy** for linting/type-checking (`make lint`)
- The subject's own **`maze_analyzer.py`** to validate generated mazes
  (connectivity, wall coherence, loop count, dead-end count)
- An **AI assistant** used as described in the Resources section above
