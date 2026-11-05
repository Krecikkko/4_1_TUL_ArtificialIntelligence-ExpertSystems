# Development Guide

## Project structure

```text
.
├── main.py                  # CLI entry point and composition root
├── puzzle.py                # Puzzle model (states, goal, successors)
├── algorithms/
│   ├── __init__.py          # Re-exports algorithm classes
│   ├── algorithm.py         # Algorithm ABC, DEBUG, configure_logging, measure_execution
│   ├── bfs.py               # Bfs          (implemented)
│   ├── astar.py             # AStar        (implemented)
│   ├── dfs.py               # Dfs          (stub)
│   ├── idfs.py              # Idfs         (stub)
│   ├── best_first.py        # BestFirst    (stub)
│   └── sma.py               # Sma          (stub)
├── heuristics/
│   ├── __init__.py          # Re-exports Heuristic and concrete heuristics
│   ├── heuristic.py         # Heuristic ABC
│   ├── factory.py           # create_heuristic(id)
│   ├── zero.py
│   ├── misplaced_tiles.py
│   └── manhattan.py
├── tests/examples/          # Sample input files (no automated tests)
└── docs/                    # This documentation
```

## Environment

- Python **≥ 3.10**, because of `X | None` annotations. The local `venv/` uses Python 3.14.4.
- No third-party dependencies and no `requirements.txt`. Only the standard library is used.
- Run everything from the repository root. Modules use absolute imports such as `from puzzle import Puzzle`, which need the root on `sys.path`.
- `.gitignore` excludes `venv/`, `.venv/` and `__pycache__/`.

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
4. Export the class in `algorithms/__init__.py`. Replace the existing stub if there is one.
5. Add a branch in `main.main()`, or uncomment the prepared one.
6. Document it in `docs/algorithms/<name>.md` and update the table in [algorithms/README.md](algorithms/README.md).

Uninformed example (movement order passed through):

```python
# algorithms/dfs.py — illustrative skeleton, not the project's implementation
from .algorithm import Algorithm, measure_execution
from puzzle import Puzzle


class Dfs(Algorithm):

    def __init__(self, max_depth: int = 20):
        self.max_depth = max_depth

    @measure_execution
    def solve(self, puzzle: Puzzle, parameter: str) -> str | None:
        start = puzzle.initial_state
        if puzzle.is_goal(start):
            return ""
        stack = [(start, "")]
        visited = {start}
        while stack:
            state, path = stack.pop()
            if len(path) >= self.max_depth:
                continue
            for move, nxt in puzzle.get_successors(state, parameter):
                if nxt in visited:
                    continue
                if puzzle.is_goal(nxt):
                    return path + move
                visited.add(nxt)
                stack.append((nxt, path + move))
        return None
```

Informed example (heuristic injected like in `AStar`):

```python
# algorithms/best_first.py — illustrative skeleton
from .algorithm import Algorithm, measure_execution
from heuristics import Heuristic
from puzzle import Puzzle


class BestFirst(Algorithm):

    def __init__(self, heuristic: Heuristic):
        self.heuristic = heuristic

    @measure_execution
    def solve(self, puzzle: Puzzle, parameter: str = "") -> str | None:
        ...  # priority = self.heuristic.calculate(state, puzzle)
```

and in `main.py`:

```python
elif args.bf is not None:
    heuristic = create_heuristic(args.bf)
    algorithm = BestFirst(heuristic)
    solution = algorithm.solve(puzzle)
```

The DFS skeleton above is only an example of how to use the interface. The design decisions for the real DFS and IDFS (depth limit, visited-set policy) belong to the assignment and still have to be made.

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
from algorithms import Bfs, AStar
from heuristics import Manhattan

p = Puzzle(3, 3, [[1, 2, 3], [4, 0, 6], [7, 5, 8]])

for move, state in p.get_successors(p.initial_state, "LURD"):
    print(move, state)

print(Bfs().solve(p, "LURD"))          # "UL"
print(AStar(Manhattan()).solve(p))     # "UL"
```

When used as a library, call `configure_logging()` first if you want to see the timing log lines.

## Testing

The repository contains **no automated tests** and no test framework configuration. `tests/examples/` contains only two input files:

```bash
python3 main.py -b LURD < tests/examples/puzzle1.txt      # expected: 2 / UL
python3 main.py -a manhattan < tests/examples/puzzle1.txt # expected: 2 / UL
```

If you add a test suite, the standard library `unittest` module is enough and keeps the project free of dependencies. Useful properties to test: BFS and A\* return solutions of the same (optimal) length; applying the returned moves to the initial state produces the goal; each heuristic returns 0 on the goal state.

## Debugging and logging

- Toggle `DEBUG` in [`algorithms/algorithm.py`](../algorithms/algorithm.py):
  - `True` (default): `INFO` level, so "Algorithm started" and "Algorithm finished | Execution time" go to stderr.
  - `False`: logging level is `CRITICAL` and the decorator skips its log calls.
- Without changing code, discard the log output with `2>/dev/null`.
- Each algorithm class has its own logger (`logging.getLogger(self.__class__.__name__)`), so log levels can be set per algorithm.

## Execution-time measurement

`@measure_execution` uses `time.perf_counter()` (monotonic, high resolution) around the wrapped `solve` call, and logs the time with 6 decimal places in a `finally` block. Only the search is timed, not input parsing. The value is logged but not returned. To collect statistics programmatically (time, expanded nodes, maximum depth), extend the decorator or the `Algorithm` interface.

## Design principles

The current design follows these principles, and new code should do the same:

- **Single Responsibility:** `Puzzle` models the problem, algorithms search, heuristics evaluate, and `main.py` wires everything together.
- **Open/Closed and Dependency Inversion:** algorithms depend on the `Heuristic` abstraction, and heuristics are injected through the constructor and chosen by the factory.
- **Liskov substitution:** every `Algorithm` must be usable through `solve(puzzle, parameter)`.
- **Immutability of states**, which keeps hashing and duplicate detection correct.

Possible improvements (not implemented):

- Move the duplicated `reconstruct_path` from `Bfs` and `AStar` into `Algorithm`.
- Add a solvability (inversion parity) check before searching.
- Validate the input and the movement order in `main.py` and report errors without tracebacks.
- Allow seeding the random generator for reproducible `R…` runs.
- Fix the stub classes' signatures (`self` is missing).
