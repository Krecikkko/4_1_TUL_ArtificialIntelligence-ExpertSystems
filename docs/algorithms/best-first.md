# Greedy Best-First Search

**Class:** `BestFirst` ([`algorithms/best_first.py`](../../algorithms/best_first.py)) · **CLI:** `-h HEURISTIC`, `--bf HEURISTIC`

## 10.1 Theoretical background

Greedy best-first search is an **informed** strategy. It always expands the frontier node with the smallest heuristic value $h(n)$, that is, the node that *looks* closest to the goal. Unlike [A\*](astar.md), it ignores the cost $g(n)$ of the path already travelled.

**Properties:**

- **Complete** on a finite state space with duplicate detection.
- **Not optimal.** It follows whatever looks promising, so it can commit to a long detour.
- Usually **much faster** than optimal methods, because it heads straight for states with low $h$.

## 10.2 Implementation analysis

### `__init__(self, heuristic: Heuristic)`

The heuristic is injected through the constructor, in the same way as in `AStar`. `main.py` builds it with `create_heuristic(args.bf)`.

### `solve(self, puzzle: Puzzle, parameter: str = "") -> str | None`

| Parameter | Meaning |
|---|---|
| `puzzle` | The `Puzzle` instance |
| `parameter` | Ignored. The heuristic is the configuration |
| **returns** | Move string, `""` if the start is the goal, `None` if the reachable space is exhausted |

The method is wrapped by `@measure_execution`.

```python
frontier = [(h(initial_state), next(insertion_order), initial_state)]
parents  = {initial_state: None}

while frontier:
    _, _, state = heappop(frontier)
    if puzzle.is_goal(state):
        return self._reconstruct_path(parents, state)
    for move, successor in puzzle.get_successors(state):     # fixed LURD order
        if successor in parents:
            continue
        parents[successor] = (state, move)
        heappush(frontier, (h(successor), next(insertion_order), successor))
return None
```

- **Frontier:** a `heapq` min-heap of `(h, insertion counter, state)`. The counter breaks ties in FIFO order, so the result is deterministic and states are never compared directly.
- **Duplicate detection:** the `parents` dictionary also serves as the set of discovered states. A state is recorded when it is first generated and is **never reopened**, even if a shorter path to it is found later.
- **Goal test:** done when a state is **popped**.
- **Movement order:** `get_successors` is called without an order, so the default `LURD` is always used.

With the `zero` heuristic every priority is 0, so the counter alone decides the order. The search then behaves like BFS with a late goal test.

## 10.3 Pseudocode

```text
function BEST-FIRST-SOLVE(puzzle, h):
    s0 ← puzzle.initial_state
    open    ← min-heap containing (h(s0), 0, s0)
    parents ← {s0 ↦ nil}
    while open is not empty:
        (_, _, s) ← open.POP-MIN()
        if IS-GOAL(s): return RECONSTRUCT(parents, s)
        for (move, s') in SUCCESSORS(s, "LURD"):
            if s' ∈ parents: continue
            parents[s'] ← (s, move)
            open.PUSH((h(s'), counter++, s'))
    return nil
```

## 10.4 Complexity analysis

- **Time:** $O(|S| \log |S|)$ in the worst case. With a good heuristic, only a small part of the space is expanded.
- **Space:** every discovered state stays in `parents`, and the frontier can hold a large part of them.
- **Solution quality:** in the [benchmark](../benchmark.md), 279 of its 348 solved runs were optimal. At scramble length 20 the average solution had 29.4 moves, compared with 15.7 for A\*.

Best-first solved the most runs in the benchmark (348 of 360). It is also the only algorithm that solves the hard sample `tests/examples/puzzle2.txt` in reasonable time (a 188-move solution with `manhattan`).

## 10.5 Advantages and limitations

| Advantages | Limitations |
|---|---|
| Fastest strategy on hard instances | Not optimal; solutions can be much longer than necessary |
| Deterministic thanks to FIFO tie-breaking | Stores every discovered state |
| Works with any `Heuristic` | Never reopens a state, even if a shorter path to it appears |
| Simple: one heap and one dictionary | Ignores the movement order (always `LURD`) |
