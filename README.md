# 15-Puzzle Solver

A command-line solver for the generalized R×C sliding-tile puzzle (15-puzzle), written in Python for the **Artificial Intelligence and Expert Systems** course. It compares uninformed and informed state-space search algorithms.

## Status

| Implemented | Planned |
|---|---|
| Breadth-first search (`-b`) | Depth-first search (`-d`) |
| A\* (`-a`) | Iterative deepening DFS (`-i`) |
| Heuristics: `zero`, `misplaced`, `manhattan` | Best-first search (`-h`) |
| Per-node random movement order (`R…`) | SMA\* (`-s`) |

## Quick start

Requires Python 3.10+ and no external packages.

```bash
python3 main.py -b LURD < tests/examples/puzzle1.txt
python3 main.py -a manhattan < tests/examples/puzzle1.txt 2>/dev/null
```

```text
2
UL
```

The input is `rows cols` followed by the board rows (`0` = empty cell). The output is the solution length followed by the moves. Moves name the direction in which the **tile** moves.

## Documentation

Full documentation is in [`docs/`](docs/README.md):

- [Getting started](docs/getting-started.md)
- [CLI reference](docs/cli-reference.md)
- [Architecture](docs/architecture.md)
- [Puzzle representation](docs/puzzle-representation.md)
- [Algorithms](docs/algorithms/README.md): [BFS](docs/algorithms/bfs.md), [A\*](docs/algorithms/astar.md)
- [Heuristics](docs/heuristics/README.md)
- [Development guide](docs/development.md)
