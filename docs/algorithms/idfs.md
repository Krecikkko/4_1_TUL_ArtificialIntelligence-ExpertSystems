# Iterative Deepening DFS (IDFS)

**Class:** `Idfs` ([`algorithms/idfs.py`](../../algorithms/idfs.py)) · **CLI:** `-i ORDER`, `--idfs ORDER`

## 9.1 Theoretical background

Iterative deepening runs a **depth-limited DFS** repeatedly with the limits 0, 1, 2, …, until a solution is found. It combines the strengths of both basic strategies:

- like **BFS**, it is complete and finds a shortest solution, because every path of length $L$ is tried before any path of length $L + 1$;
- like **DFS**, it needs memory only for the current path.

The cost is that shallow levels are explored again in every iteration. Because the number of nodes grows exponentially with depth, the last iteration dominates the total time, so the overhead is a constant factor.

## 9.2 Implementation analysis

### `solve(self, puzzle: Puzzle, parameter: str) -> str | None`

| Parameter | Meaning |
|---|---|
| `puzzle` | The `Puzzle` instance |
| `parameter` | Movement order, e.g. `"LURD"`, or one starting with `R` for random order |
| **returns** | Move string, `""` if the start is the goal, `None` if no solution exists |

The method is wrapped by `@measure_execution`.

Unlike the other algorithms, `Idfs` **validates the movement order immediately**. If `parameter` is not a permutation of `LRUD`, it raises `ValueError("Move order must be a permutation of LRUD")` before any search starts.

```python
for limit in count():                          # 0, 1, 2, ...
    solution, cutoff = self._depth_limited_search(puzzle, parameter, limit)
    if solution is not None:
        return solution
    if not cutoff:
        return None
```

The `cutoff` flag records whether any branch was stopped by the depth limit. If no branch was stopped, a larger limit cannot reach anything new. The search space is exhausted and the method returns `None`.

### `_depth_limited_search(puzzle, order, limit) -> (str | None, bool)`

This is an iterative DFS that uses the same iterator stack as [`Dfs`](dfs.md#82-implementation-analysis), with these differences:

- **Depth limit:** `moves` holds the current path. When `len(moves) == limit`, the current frame is not extended, `cutoff` is set to `True`, and the search backtracks.
- **Cycle check on the current path only:** `on_path` contains the states on the current path. A successor already on the path is skipped. There is **no global visited set**, so a state can be reached again through a different path. This keeps memory proportional to the depth, but it means the same state can be expanded many times.
- **Goal test:** done when a state is generated, before it is pushed.
- **Path:** the moves are kept in the `moves` list during the search, so no `parents` map is needed.

## 9.3 Pseudocode

```text
function IDFS-SOLVE(puzzle, order):
    require order is a permutation of LRUD
    for limit ← 0, 1, 2, …:
        (solution, cutoff) ← DLS(puzzle, order, limit)
        if solution ≠ nil: return solution
        if not cutoff: return nil

function DLS(puzzle, order, limit):
    s0 ← puzzle.initial_state
    if IS-GOAL(s0): return ("", false)
    stack ← [(s0, SUCCESSORS(s0, order))];  on_path ← {s0};  moves ← [];  cutoff ← false
    while stack is not empty:
        (s, it) ← stack.TOP()
        if it is exhausted: POP-FRAME(); continue
        (move, s') ← it.NEXT()
        if s' ∈ on_path: continue
        if |moves| = limit: cutoff ← true; POP-FRAME(); continue
        moves.APPEND(move)
        if IS-GOAL(s'): return (JOIN(moves), cutoff)
        on_path ← on_path ∪ {s'};  stack.PUSH((s', SUCCESSORS(s', order)))
    return (nil, cutoff)

POP-FRAME(): remove the top frame and its state from on_path; drop the last move if a frame remains
```

## 9.4 Complexity analysis

Let $b$ be the branching factor and $d$ the optimal solution depth.

- **Time:** $O(b^d)$. Iteration $L$ costs about $b^L$, and the sum over $L = 0 … d$ is dominated by the last term. Because only cycles on the current path are removed, transpositions (the same state reached by different paths) are expanded again, so the real effective branching factor is higher than with BFS.
- **Space:** $O(d)$ stack frames, plus the `on_path` set and `moves` list of the same size. This is the main advantage over BFS and DFS.
- **Unsolvable inputs:** on a 4×4 board the search never finishes in practice, because the number of simple paths explodes before every one of them stops reaching the limit.

In the [benchmark](../benchmark.md), IDFS solved all boards up to scramble length 12 with optimal solutions. At length 20 it solved 54 of 90 runs; the rest hit the 5 s timeout. It never ran out of memory.

## 9.5 Advantages and limitations

| Advantages | Limitations |
|---|---|
| Optimal for unit move costs, like BFS | Re-explores shallow levels in every iteration |
| Memory linear in the solution depth | No transposition detection, so many states are expanded repeatedly |
| Validates the movement order before searching | Slow on deep solutions; time, not memory, is the limit |
| Supports per-node random ordering | Practically never terminates on unsolvable 4×4 inputs |
