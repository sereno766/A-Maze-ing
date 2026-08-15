*This project has been created as part of the 42 curriculum by smachado, vigomes-*

# A-MAZE-ING
*This is the way*

## DESCRIPTION

A-Maze-ing is a Python maze generator. Given a `config.txt` file, it builds a
grid-based maze (optionally a "perfect" maze with a single path between the
entry and the exit, or a Pac-Man-style board with multiple independent
routes), computes the shortest path between the entry and the exit, and
writes the result to a plain text file using a compact hexadecimal wall
encoding (one hex digit per cell). The maze generation algorithm is also
packaged separately as **`mazegen`**, a standalone, pip-installable module
with no dependency on this CLI or its config-parsing layer (see
[Reusable code](#reusable-code) below).

## INSTRUCTIONS

### Requirements
- Python 3.10+
- A virtual environment is recommended (`venv`)

### Setup
From the `program/` directory:
```bash
make install
# creates the venv (program/venv) and installs dependencies from
# requirements.txt in one step
source venv/bin/activate        # bash/zsh, optional
# or: source venv/bin/activate.fish   (fish shell)
```

### Running
```bash
make run
# equivalent to:
venv/bin/python -m a_maze_ing config.txt
```
`config.txt` is currently required (an explicit config file must be passed).

### Debugging
```bash
make debug
# runs the same entry point under pdb:
venv/bin/python -m pdb -m a_maze_ing config.txt
```

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

The maze generation algorithm is packaged separately from the CLI as
**`mazegen`**, a standalone module at [`mazegen/mazegen.py`](mazegen/mazegen.py),
with no dependency on `a_maze_ing`, `argparse`, or the config file parser --
it only needs the Python standard library. It exposes a single public class,
`MazeGenerator`.

Built as an installable package (`.whl`/`.tar.gz`, see below), it can be
`pip install`-ed and reused by any future project independently of this
repository's CLI.

### Usage example

```python
from mazegen import MazeGenerator

gen = MazeGenerator(
    width=20, height=15,
    entry=(0, 0), exit=(19, 14),
    perfect=False,        # False -> braided/loopy, Pac-Man-style board
    seed="my-seed-123",   # optional, for reproducible generation
)
gen.generate()

# Access the generated structure directly:
cell = gen.grid[0][0]     # grid[y][x]
print(cell.walls)         # 4-bit wall mask (N=1, E=2, S=4, W=8)
print(gen.wall_at(0, 0))  # same thing, via accessor

# Access a solution:
path = gen.shortest_path()   # e.g. ["E", "E", "S", ...]
```

Custom parameters (size, entry/exit, seed, perfect/non-perfect mode, and
whether to reserve the "42" pattern cells) are all passed directly to the
`MazeGenerator` constructor shown above -- no config file is required.

> Note: the in-memory structure (`Cell.walls`, a 4-bit mask per cell) is not
> the same format as `a_maze_ing`'s output file -- it grants direct access
> to the grid instead.

### Building the package

```bash
cd mazegen
python -m pip install build
python -m build
# -> dist/mazegen-1.0.0-py3-none-any.whl
# -> dist/mazegen-1.0.0.tar.gz
```

The built `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz` are
committed at the root of this repository, alongside [`LICENSE.md`](LICENSE.md)
(MIT), which explicitly allows reuse and distribution by later projects. See
[`mazegen/README.md`](mazegen/README.md) for the package's own short
documentation (mirrored from this section).

> The `program/a_maze_ing` CLI currently carries its own, similar internal
> generation logic (`program/a_maze_ing/src/maze.py`) to drive the
> interactive shell/renderer -- `mazegen` is the standalone, pip-installable
> module meant for reuse by future projects.

## RESOURCES

- [Wikipedia -- Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Jamis Buck -- "Maze Generation: Algorithm Recap"](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap) (overview and comparison of recursive backtracker, Prim's, Kruskal's, etc.)
- [Think Labyrinth -- Maze generation algorithms](https://www.astrolog.org/labyrnth/algrithm.htm)
- [Python `argparse` documentation](https://docs.python.org/3/library/argparse.html)
- [Python `collections.deque` documentation](https://docs.python.org/3/library/collections.html#collections.deque) (used for the BFS shortest-path queue)
- [PEP 257 -- Docstring Conventions](https://peps.python.org/pep-0257/)

### How AI was used

An AI assistant (Claude Code) was used mainly to **consult** on concepts
needed for the project (bitwise wall encoding, BFS, Python packaging, etc.)
and to **assist with documentation** -- the PEP 257 docstrings across every
module and this README. All AI-assisted changes were reviewed, tested, and
understood by the team before being kept.

## TEAM AND PROJECT MANAGEMENT

### Roles
- **smachado**: maze generation core -- the recursive-backtracker algorithm
  (`MazeGenerator`), the `Cell` representation, the BFS shortest-path solver,
  and the "perfect maze" mode.
- **vigomes-**: the visual/ASCII rendering layer (`Render`) and the config
  file parser (`parser.py`).
- **Both**: everything else -- shell/CLI integration, the interactive menu,
  lint/type-checking cleanup, the `mazegen` reusable package, and the
  README -- was shared/paired on.

### Planning
Tasks were tracked on a Kanban-style board (Backlog / In Progress),
broken down per feature (Seed System, Cell representation, Pathfinding,
Hex encoding/Export, ...), with sub-tasks as checklists on each card.

Work started on two parallel branches, `maze_ger` (config parsing, RNG/seed
handling, generation logic) and `maze_representation` (grid/cell state), each
merged into `main` independently as they matured. Partway through, the two
generator-related classes were deliberately refactored into a single `Maze`
class with nested collaborators (`MazeRepresentation`, `MazeGenerator`),
specifically to satisfy the "one reusable class" requirement -- the original
split made sense while iterating, but not as the final public shape. Visual
rendering (`maze_render` branch) and the interactive shell were planned and
built last, once generation/output were solid, followed by a final pass
dedicated to packaging (`mazegen`) and to strict lint/type-checking/docstring
compliance across the whole codebase.

### What worked well / what could be improved
**Worked well:**
- Splitting work into per-feature branches (`maze_ger`, `maze_representation`,
  `maze_render`) let generation, state, and rendering evolve independently
  without blocking each other.
- Writing `maze_analyzer.py` early, as an independent verification script,
  caught structural issues (wall coherence, connectivity, loop/dead-end
  counts) mechanically instead of relying on eyeballing ASCII output.

**Could be improved:**
- The two early branches modeled coordinates differently (`(x, y)` in
  `Settings` vs. `(row, col)` internally), and that mismatch resurfaced later
  as a real bug in the renderer (entry/exit swapped on non-square mazes) --
  worth agreeing on one convention project-wide from the start.
- The shell's error display and the parser's validation messages drifted out
  of sync: a hardcoded whitelist of "known" error substrings in the shell
  ended up hiding most of the parser's specific, well-written error messages
  behind a generic "unknown error". Two lists that must stay manually in sync
  across files is a fragile pattern to avoid.
- `flake8`/`mypy --strict` compliance and docstrings were treated as a final
  cleanup pass instead of enforced continuously -- retrofitting ~30 missing
  docstrings and dozens of type annotations at the end took longer than
  keeping `make lint` green from each merge onward would have.
- The Makefile's mandatory `install`/`debug` rules were left as empty stubs
  for most of the project and were nearly missed entirely.

### Tools used
- **Git** (feature branches per component, e.g. `maze_ger`,
  `maze_representation`, merged into `main`)
- A **Kanban board** (Trello-style) for task tracking
- **flake8** and **mypy** for linting/type-checking (`make lint`)
- The subject's own **`maze_analyzer.py`** to validate generated mazes
  (connectivity, wall coherence, loop count, dead-end count)
- An **AI assistant** used as described in the Resources section above
