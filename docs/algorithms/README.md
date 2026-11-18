# Search Algorithms

Every algorithm is a subclass of `Algorithm` ([`algorithms/algorithm.py`](../../algorithms/algorithm.py)) and implements

```python
solve(puzzle: Puzzle, parameter: str) -> str | None
```

The method returns the move string (`""` if the start is already the goal), or `None` if no solution was found after the search space was exhausted. Every algorithm decorates `solve` with `@measure_execution` to log the execution time (see [architecture](../architecture.md#logging-and-execution-time-measurement)).

## Overview

| Algorithm | Class | CLI | Kind | Parameter | Docs |
|---|---|---|---|---|---|
| Breadth-first search | `Bfs` | `-b` | Uninformed | Movement order | [bfs.md](bfs.md) |
| Depth-first search | `Dfs` | `-d` | Uninformed | Movement order | [dfs.md](dfs.md) |
| Iterative deepening DFS | `Idfs` | `-i` | Uninformed | Movement order | [idfs.md](idfs.md) |
| Best-first (greedy) | `BestFirst` | `-h` | Informed | Heuristic (injected) | [best-first.md](best-first.md) |
| A\* | `AStar` | `-a` | Informed | Heuristic (injected) | [astar.md](astar.md) |
| SMA\* | `SMAStar` | `-s` | Informed | Heuristic (injected) | [sma.md](sma.md) |

Uninformed algorithms receive the movement order through `solve(puzzle, order)`. Informed algorithms receive the heuristic through the constructor and ignore `parameter`.

## Comparison

| Property | BFS | DFS | IDFS | Best-first | A\* | SMA\* |
|---|---|---|---|---|---|---|
| Frontier | FIFO `deque` | Stack of successor iterators | Stack of successor iterators, depth-limited | Min-heap on `(h, insertion order)` | Min-heap on `(f, insertion order)` | Explicit tree with cached best/worst leaves |
| Goal test | On generation | On generation | On generation | On pop | On pop | On selection |
| Duplicate detection | Global `visited` set | Global `visited` set | Current path only | Global (`parents`), never reopened | `g_score`, cheaper path reopens | Ancestors only |
| Uses movement order | Yes (incl. random) | Yes (incl. random) | Yes (incl. random) | No (`LURD`) | No (`LURD`) | No (`LURD`) |
| Uses heuristic | No | No | No | Yes, $h$ | Yes, $g + h$ | Yes, $g + h$ with pathmax |
| Optimal (unit costs) | Yes | No | Yes | No | Yes, with admissible $h$ | Yes, if the solution fits in memory |
| Memory | All generated states | All generated states | $O(d)$ | All discovered states | All generated states | At most 10 000 nodes |
| Solvability check | No | No | No | No | No | Yes |

All three implemented heuristics are admissible and consistent (see [heuristics](../heuristics/README.md#comparison)).

Measured results for all six algorithms are in the [benchmark documentation](../benchmark.md#summary-of-full_resultscsv). To add a new algorithm, follow [development.md](../development.md#adding-a-new-search-algorithm) and document it here using the same section layout as the existing pages (theory → implementation → pseudocode → complexity → advantages and limitations).
