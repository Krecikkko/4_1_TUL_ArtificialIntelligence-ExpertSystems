# 15-Puzzle Solver — Documentation

This directory contains the technical documentation of the 15-puzzle solver developed for the **Artificial Intelligence and Expert Systems** course. The documentation describes the code as it is currently implemented.

## Project overview

The 15-puzzle is a sliding-tile puzzle. Numbered tiles sit on a rectangular board with one empty cell, and a move slides a tile next to the empty cell into it. The solver takes an initial board configuration and searches for a sequence of moves that turns it into the target configuration.

### Assignment objectives

- Build a command-line solver for the generalized R×C sliding-tile puzzle.
- Implement and compare **uninformed** search strategies (BFS, DFS, IDFS) and **informed** strategies (Best-first, A\*, SMA\*).
- Make uninformed strategies configurable by a **movement order**, including a randomized order.
- Make informed strategies configurable by a **heuristic**.
- Read the puzzle from standard input and write the solution to standard output.

### Supported dimensions and target configuration

Any board with `R` rows and `C` columns is accepted (`R`, `C` ≥ 1). The board size is read from the input, so 3×3, 4×4, 2×3 and similar boards all work. The target configuration lists the tiles `1 … R·C−1` in row-major order, with the empty cell (`0`) in the bottom-right corner. For a 4×4 board:

```text
 1  2  3  4
 5  6  7  8
 9 10 11 12
13 14 15  0
```

### Feature status

| Feature | Status | Documentation |
|---|---|---|
| Breadth-first search (`-b`) | ✅ Implemented | [algorithms/bfs.md](algorithms/bfs.md) |
| Depth-first search (`-d`) | ✅ Implemented | [algorithms/dfs.md](algorithms/dfs.md) |
| Iterative deepening DFS (`-i`) | ✅ Implemented | [algorithms/idfs.md](algorithms/idfs.md) |
| Best-first search (`-h`) | ✅ Implemented | [algorithms/best-first.md](algorithms/best-first.md) |
| A\* search (`-a`) | ✅ Implemented | [algorithms/astar.md](algorithms/astar.md) |
| SMA\* (`-s`) | ✅ Implemented | [algorithms/sma.md](algorithms/sma.md) |
| Zero heuristic | ✅ Implemented | [heuristics/zero.md](heuristics/zero.md) |
| Misplaced-tiles heuristic | ✅ Implemented | [heuristics/misplaced-tiles.md](heuristics/misplaced-tiles.md) |
| Manhattan-distance heuristic | ✅ Implemented | [heuristics/manhattan.md](heuristics/manhattan.md) |
| Random movement order (`R…`) | ✅ Implemented (with caveats) | [puzzle-representation.md](puzzle-representation.md#random-successor-ordering) |
| Execution-time logging | ✅ Implemented (stderr) | [architecture.md](architecture.md#logging-and-execution-time-measurement) |
| Benchmark (empirical study) | ✅ Implemented (Linux only) | [benchmark.md](benchmark.md) |
| Solution viewer (Tkinter) | ✅ Implemented | [getting-started.md](getting-started.md#viewing-a-solution) |
| Solvability check | ⚠️ SMA\* only | [Known limitations](#known-limitations) |
| Automated unit tests | ❌ Not implemented (the benchmark verifies solutions) | [development.md](development.md#testing) |

### Technology stack

- **Language:** Python. Version 3.10 or newer is required because the code uses `X | None` type annotations (PEP 604). The project's `venv` uses Python 3.14.4.
- **Dependencies:** standard library only. The solver uses `argparse`, `collections`, `heapq`, `itertools`, `dataclasses`, `math`, `random`, `logging`, `time`, `abc` and `functools`. The viewer uses `tkinter`, and the benchmark uses `subprocess`, `csv` and `resource`. There is no `requirements.txt`.

### Known limitations

- Only **SMA\*** checks solvability. For an unsolvable input, the other algorithms keep searching until they have explored every reachable state (or every path, for IDFS) before printing `-1`. On a 4×4 board this is not feasible in practice.
- Best-first, A\* and SMA\* ignore the movement order and always generate successors in the `LURD` order.
- The SMA\* memory limit (10 000 nodes) cannot be changed from the command line.
- The random movement order is not seeded by the solver, so `R…` runs cannot be reproduced. The benchmark seeds them itself.
- The input is not validated (dimensions, row lengths, duplicate or missing tiles).
- Heuristic identifiers are names (`zero`, `misplaced`, `manhattan`), not numbers.
- Logging is enabled by default (`DEBUG = True`) and prints to standard error.
- The benchmark uses `resource` and runs only on Linux.

More details are in the [CLI reference](cli-reference.md#behavior-and-error-handling) and in each algorithm page.

## Documentation map

| Document | Contents |
|---|---|
| [getting-started.md](getting-started.md) | Installation, first run, input files |
| [cli-reference.md](cli-reference.md) | Command-line options, I/O formats, exit behavior |
| [architecture.md](architecture.md) | Modules, classes, data flow, diagrams |
| [puzzle-representation.md](puzzle-representation.md) | State encoding, moves, successor generation |
| [algorithms/README.md](algorithms/README.md) | Algorithm overview and comparison |
| [algorithms/bfs.md](algorithms/bfs.md) | Breadth-first search |
| [algorithms/dfs.md](algorithms/dfs.md) | Depth-first search |
| [algorithms/idfs.md](algorithms/idfs.md) | Iterative deepening DFS |
| [algorithms/best-first.md](algorithms/best-first.md) | Greedy best-first search |
| [algorithms/astar.md](algorithms/astar.md) | A\* search |
| [algorithms/sma.md](algorithms/sma.md) | SMA\* (memory-bounded A\*) |
| [heuristics/README.md](heuristics/README.md) | Heuristic interface and comparison |
| [heuristics/zero.md](heuristics/zero.md) | Zero heuristic |
| [heuristics/misplaced-tiles.md](heuristics/misplaced-tiles.md) | Misplaced-tiles heuristic |
| [heuristics/manhattan.md](heuristics/manhattan.md) | Manhattan-distance heuristic |
| [benchmark.md](benchmark.md) | Empirical study: running, design, result files, summary |
| [development.md](development.md) | Extending the project, conventions, debugging |
