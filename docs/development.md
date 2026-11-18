# Development Guide

## Project structure

```text
.
├── main.py                  # CLI entry point and composition root
├── puzzle.py                # Puzzle model (states, goal, successors)
├── commands.md              # Copy-paste demo commands
├── algorithms/
│   ├── __init__.py          # Re-exports algorithm classes
│   ├── algorithm.py         # Algorithm ABC, DEBUG, configure_logging, measure_execution
│   ├── bfs.py               # Bfs
│   ├── dfs.py               # Dfs
│   ├── idfs.py              # Idfs
│   ├── best_first.py        # BestFirst
│   ├── astar.py             # AStar
│   └── sma.py               # SMAStar
├── heuristics/
│   ├── __init__.py          # Re-exports Heuristic and concrete heuristics
│   ├── heuristic.py         # Heuristic ABC
│   ├── factory.py           # create_heuristic(id)
│   ├── zero.py
│   ├── misplaced_tiles.py
│   └── manhattan.py
├── viewer/                  # Tkinter solution viewer (python3 -m viewer.app)
│   ├── app.py
│   └── board.py
├── benchmark/               # Empirical study (python3 -m benchmark), see benchmark.md
│   ├── run.py
│   ├── generate_boards.py
│   ├── boards/              # 40 generated 4×4 boards
│   ├── boards_pilot/        # Pilot board set (unused by the scripts)
│   └── results/             # Result CSV files
├── tests/
│   ├── examples/            # Sample input files
│   └── solutions/           # Saved solver output for the viewer (git-ignored)
└── docs/                    # This documentation
```

## Environment

- Python **≥ 3.10**, because of `X | None` annotations. The local `venv/` uses Python 3.14.4.
- No third-party dependencies and no `requirements.txt`. Only the standard library is used.
- Run everything from the repository root. Modules use absolute imports such as `from puzzle import Puzzle`, which need the root on `sys.path`.
- `.gitignore` excludes `venv/`, `.venv/`, `__pycache__/` and `tests/solutions/*`.

## Coding conventions (as observed in the code)

- Classes in `PascalCase` (`AStar`, `MisplacedTiles`), functions and methods in `snake_case`.
- One class per module. Packages re-export their public classes in `__init__.py`.
- Type hints on public signatures (`tuple[int, ...]`, `str | None`).
- States are always immutable tuples. Algorithms keep their search data in local variables and do not store it on the instance.
- Short comments explain the intent of the data structures.

## Adding a new search algorithm

1. Create `algorithms/<name>.py` with a subclass of `Algorithm`. Implement `solve(self, puzzle, parameter)` and decorate it with `@measure_execution`.
2. Use only the public `Puzzle` API: `initial_state`, `is_goal()`, `get_successors(state, order)`.
3. Return a move string, `""` if the initial state is the goal, or `None` if there is no solution.
4. Export the class in `algorithms/__init__.py`.
5. Add a command-line option in `parse_arguments()` and a branch in `main.main()`.
6. To include it in the empirical study, add it to the `configurations` list in [`benchmark/run.py`](../benchmark/run.py).
7. Document it in `docs/algorithms/<name>.md` and update the tables in [algorithms/README.md](algorithms/README.md).

An informed algorithm receives its heuristic through the constructor, like `BestFirst`, `AStar` and `SMAStar`:

```python
# algorithms/ida_star.py — illustrative skeleton
from .algorithm import Algorithm, measure_execution
from heuristics import Heuristic
from puzzle import Puzzle


class IdaStar(Algorithm):

    def __init__(self, heuristic: Heuristic):
        self.heuristic = heuristic

    @measure_execution
    def solve(self, puzzle: Puzzle, parameter: str = "") -> str | None:
        ...  # bound = self.heuristic.calculate(puzzle.initial_state, puzzle)
```

and in `main.py`:

```python
elif args.ida is not None:
    heuristic = create_heuristic(args.ida)
    algorithm = IdaStar(heuristic)
    solution = algorithm.solve(puzzle)
```

The existing implementations are the best reference: [`dfs.py`](../algorithms/dfs.py) and [`idfs.py`](../algorithms/idfs.py) show the iterator-stack pattern for depth-first search, and [`best_first.py`](../algorithms/best_first.py) shows a compact priority-queue search.

## Adding a new heuristic

1. Create `heuristics/<name>.py` with a subclass of `Heuristic` that implements `calculate(self, state, puzzle) -> int`.
2. Export it in `heuristics/__init__.py`.
3. Register an ID in the `heuristics` dictionary in `heuristics/factory.py`.
4. Document it in `docs/heuristics/<name>.md`.

```python
# heuristics/linear_conflict.py — illustrative skeleton
from .heuristic import Heuristic
from .manhattan import Manhattan
from puzzle import Puzzle


class LinearConflict(Heuristic):

    def __init__(self):
        self._manhattan = Manhattan()

    def calculate(self, state: tuple[int, ...], puzzle: Puzzle) -> int:
        h = self._manhattan.calculate(state, puzzle)
        # + 2 for every pair of tiles in their goal row/column in reversed order
        return h
```

```python
# heuristics/factory.py
heuristics = {
    "zero": Zero,
    "misplaced": MisplacedTiles,
    "manhattan": Manhattan,
    "linear": LinearConflict,
}
```

Keep heuristics **admissible** (never overestimating) if A\* has to stay optimal. Read geometry from `puzzle.rows` and `puzzle.cols` instead of hard-coding 4×4.

## Reusing the `Puzzle` class

`Puzzle` can be used without the CLI, for example in experiments or tests:

```python
from puzzle import Puzzle
from algorithms import Bfs, Idfs, AStar, SMAStar
from heuristics import Manhattan

p = Puzzle(3, 3, [[1, 2, 3], [4, 0, 6], [7, 5, 8]])

for move, state in p.get_successors(p.initial_state, "LURD"):
    print(move, state)

print(Bfs().solve(p, "LURD"))          # "UL"
print(Idfs().solve(p, "LURD"))         # "UL"
print(AStar(Manhattan()).solve(p))     # "UL"
print(SMAStar(Manhattan(), memory_limit=100).solve(p))  # "UL"
```

When used as a library, call `configure_logging()` first if you want to see the timing log lines.

## Testing

The repository has **no unit tests** and no test framework configuration. Correctness is checked in two ways:

- **Sample inputs** in `tests/examples/` with known optimal solutions:

  ```bash
  python3 main.py -b LURD < tests/examples/puzzle1.txt      # expected: 2 / UL
  python3 main.py -i LURD < tests/examples/puzzle3.txt      # expected: 8 / RRULDLUL
  python3 main.py -a manhattan < tests/examples/puzzle3.txt # expected: 8 / RRULDLUL
  ```

- **The benchmark** replays every returned solution on its board and marks illegal or incomplete solutions as `invalid_solution`. `python3 -m benchmark --check` is a quick end-to-end check of all 18 configurations on one board (Linux only). See [benchmark.md](benchmark.md).

If you add a unit test suite, the standard library `unittest` module is enough and keeps the project free of dependencies. Useful properties to test: the optimal algorithms (BFS, IDFS, A\*, SMA\*) return solutions of the same length; applying the returned moves to the initial state produces the goal; each heuristic returns 0 on the goal state.

## Debugging and logging

- Toggle `DEBUG` in [`algorithms/algorithm.py`](../algorithms/algorithm.py):
  - `True` (default): `INFO` level, so "Algorithm started" and "Algorithm finished | Execution time" go to stderr.
  - `False`: logging level is `CRITICAL` and the decorator skips its log calls.
- Without changing code, discard the log output with `2>/dev/null`.
- Each algorithm class has its own logger (`logging.getLogger(self.__class__.__name__)`), so log levels can be set per algorithm.

## Execution-time measurement

`@measure_execution` uses `time.perf_counter()` (monotonic, high resolution) around the wrapped `solve` call, and logs the time with 6 decimal places in a `finally` block. Only the search is timed, not input parsing. The value is logged but not returned. The benchmark collects it by parsing standard error. To collect other statistics (expanded nodes, maximum depth), extend the decorator or the `Algorithm` interface. `SMAStar` already records `peak_nodes`, `evictions` and `regenerations` on the instance.

## Design principles

The current design follows these principles, and new code should do the same:

- **Single Responsibility:** `Puzzle` models the problem, algorithms search, heuristics evaluate, and `main.py` wires everything together.
- **Open/Closed and Dependency Inversion:** algorithms depend on the `Heuristic` abstraction, and heuristics are injected through the constructor and chosen by the factory.
- **Liskov substitution:** every `Algorithm` must be usable through `solve(puzzle, parameter)`.
- **Immutability of states**, which keeps hashing and duplicate detection correct.

Possible improvements (not implemented):

- Move the duplicated `reconstruct_path` from `Bfs`, `Dfs` and `AStar` into `Algorithm`.
- Add the solvability (inversion parity) check that `SMAStar` uses to every algorithm.
- Validate the input and the movement order in `main.py` and report errors without tracebacks.
- Allow seeding the random generator from the CLI for reproducible `R…` runs.
- Expose the SMA\* memory limit as a command-line option.
- Remove the unreachable `NotImplementedError` branch from `main.main()`.
