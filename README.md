# 15-Puzzle Solver

A command-line solver for the generalized R×C sliding-tile puzzle (15-puzzle), written in Python for the **Artificial Intelligence and Expert Systems** course. It compares uninformed and informed state-space search algorithms.

## Features

| Algorithm | Option | Parameter | Optimal |
|---|---|---|---|
| Breadth-first search | `-b`, `--bfs` | Movement order | Yes |
| Depth-first search | `-d`, `--dfs` | Movement order | No |
| Iterative deepening DFS | `-i`, `--idfs` | Movement order | Yes |
| Greedy best-first search | `-h`, `--bf` | Heuristic | No |
| A\* | `-a`, `--astar` | Heuristic | Yes |
| SMA\* (memory-bounded A\*) | `-s`, `--sma` | Heuristic | Yes, if the solution fits in its 10 000-node budget |

- **Movement order:** a permutation of `LURD`. An order starting with `R` (for example `RLUD`) randomizes the order separately for every expanded node.
- **Heuristics:** `zero`, `misplaced` and `manhattan`.
- **Solution viewer:** a Tkinter window that replays a saved solution.
- **Benchmark:** an empirical study that compares all algorithms on 40 generated boards.

## Quick start

Requires Python 3.10+ and no external packages.

```bash
python3 main.py -b LURD < tests/examples/puzzle1.txt
python3 main.py -a manhattan < tests/examples/puzzle1.txt 2>/dev/null
python3 main.py --help
```

```text
2
UL
```

The input is `rows cols` followed by the board rows (`0` = empty cell). The output is the solution length followed by the moves, or `-1` and an empty line if no solution was found. Moves name the direction in which the **tile** moves. The execution time is logged to standard error.

Ready-to-paste commands for every algorithm are in [`commands.md`](commands.md).

## Solution viewer

```bash
mkdir -p tests/solutions
python3 main.py -a manhattan < tests/examples/puzzle3.txt > tests/solutions/solution.txt
python3 -m viewer.app tests/examples/puzzle3.txt tests/solutions/solution.txt
```

## Benchmark

The [`benchmark/`](benchmark/) package runs the empirical study: every algorithm configuration on a fixed set of boards. Run all commands from the repository root. The benchmark needs **Linux** because it uses the `resource` module to limit memory.

```bash
python3 -m benchmark --check           # quick check: 1 board, 1 trial -> benchmark/results/full_check.csv
python3 -m benchmark                   # full study                    -> benchmark/results/full_results.csv
python3 -m benchmark.generate_boards   # regenerate the boards in benchmark/boards/
```

What the full study runs:

- **Boards:** 40 boards from [`benchmark/boards/`](benchmark/boards/), 10 each at scramble lengths 4, 8, 12 and 20.
- **Configurations:** 18 in total:
  - BFS, DFS and IDFS, each with the move orders `LURD`, `DLUR` and `RLUD`.
  - Best-first, A\* and SMA\*, each with the heuristics `zero`, `misplaced` and `manhattan`.
- **Trials:** 3 per board and configuration, so 2160 runs in total. `RLUD` runs use the search seeds 42, 43 and 44, one per trial.
- **Limits:** each run is a separate process limited to **5 s** and **512 MiB**.

Each row of the results CSV records:

- `status`: one of `solved`, `timeout`, `memory_limit`, `execution_error`, `invalid_solution`, `invalid_output` or `no_solution_returned`.
- `elapsed_ms`: the wall-clock time of the whole run.
- `search_ms`: the search time reported by the solver.
- `solution_length`: the number of moves in the solution.

Every solution is replayed on the board to check that it actually solves it. The benchmark refuses to overwrite an existing results file, so rename or move the old file before you rerun.

Generating boards is deterministic: the generator always produces the same boards. It overwrites the files in `benchmark/boards/`.

The full description of the study and a summary of the results are in [docs/benchmark.md](docs/benchmark.md).

## Documentation

Full documentation is in [`docs/`](docs/README.md):

- [Getting started](docs/getting-started.md)
- [CLI reference](docs/cli-reference.md)
- [Architecture](docs/architecture.md)
- [Puzzle representation](docs/puzzle-representation.md)
- [Algorithms](docs/algorithms/README.md): [BFS](docs/algorithms/bfs.md), [DFS](docs/algorithms/dfs.md), [IDFS](docs/algorithms/idfs.md), [Best-first](docs/algorithms/best-first.md), [A\*](docs/algorithms/astar.md), [SMA\*](docs/algorithms/sma.md)
- [Heuristics](docs/heuristics/README.md)
- [Benchmark](docs/benchmark.md)
- [Development guide](docs/development.md)
