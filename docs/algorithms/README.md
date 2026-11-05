# Search Algorithms

Every algorithm is a subclass of `Algorithm` ([`algorithms/algorithm.py`](../../algorithms/algorithm.py)) and implements

```python
solve(puzzle: Puzzle, parameter: str) -> str | None
```

The method returns the move string (`""` if the start is already the goal), or `None` if the reachable state space has been exhausted. Implemented algorithms decorate `solve` with `@measure_execution` to log the execution time (see [architecture](../architecture.md#logging-and-execution-time-measurement)).

## Status

| Algorithm | Class | CLI | Kind | Parameter | Status | Docs |
|---|---|---|---|---|---|---|
| Breadth-first search | `Bfs` | `-b` | Uninformed | Movement order | ✅ Implemented | [bfs.md](bfs.md) |
| A\* | `AStar` | `-a` | Informed | Heuristic (injected) | ✅ Implemented | [astar.md](astar.md) |
| Depth-first search | `Dfs` | `-d` | Uninformed | Movement order | ⏳ Stub | — |
| Iterative deepening DFS | `Idfs` | `-i` | Uninformed | Movement order | ⏳ Stub | — |
| Best-first (greedy) | `BestFirst` | `-h` | Informed | Heuristic | ⏳ Stub | — |
| SMA\* | `Sma` | `-s` | Informed | Heuristic | ⏳ Stub | — |

## Planned algorithms

The files `dfs.py`, `idfs.py`, `best_first.py` and `sma.py` contain only placeholder classes. Their `__init__` and `solve` take no `self` and have empty bodies. `main.py` does not instantiate them (the Best-first and SMA\* branches are commented out), so selecting them raises `NotImplementedError`.

When one of them is implemented, add `docs/algorithms/<name>.md` using the same section layout as [bfs.md](bfs.md) and [astar.md](astar.md) (theory → implementation → walkthrough → pseudocode → complexity → advantages and limitations), and link it from the table above. For guidance on the code, see [development.md](../development.md#adding-a-new-search-algorithm).

## Comparison of implemented algorithms

| Property | BFS | A\* |
|---|---|---|
| Frontier | FIFO `deque` | Min-heap on `(f, insertion order)` |
| Goal test | When a node is **generated** | When a node is **popped** |
| Duplicate detection | `visited` set (first discovery wins) | `g_score` (a cheaper path replaces the old one) |
| Uses movement order | Yes (including random) | No (fixed `LURD`) |
| Uses heuristic | No | Yes |
| Optimal (unit costs) | Yes | Yes, with admissible $h$ (all three implemented heuristics are admissible) |

See [astar.md § 7.7](astar.md#77-comparison-with-bfs) for a full comparison.
