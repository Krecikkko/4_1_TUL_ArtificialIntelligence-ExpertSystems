# Depth-First Search (DFS)

**Class:** `Dfs` ([`algorithms/dfs.py`](../../algorithms/dfs.py)) · **CLI:** `-d ORDER`, `--dfs ORDER`

## 8.1 Theoretical background

Depth-first search is an **uninformed** strategy. It always extends the most recently generated path: it goes as deep as it can along one branch and backtracks only when that branch has no unexplored successors left. A **LIFO stack** produces this order.

**Properties:**

- **Complete** on a finite state space when repeated states are detected. The puzzle space is finite, and this implementation remembers every visited state, so it cannot loop forever.
- **Not optimal.** The first goal found is the one at the end of the first branch that reaches it. That branch is usually far longer than the shortest solution.

## 8.2 Implementation analysis

### `solve(self, puzzle: Puzzle, parameter: str) -> str | None`

| Parameter | Meaning |
|---|---|
| `puzzle` | The `Puzzle` instance |
| `parameter` | Movement order, e.g. `"LURD"`, or one starting with `R` for random order |
| **returns** | Move string, `""` if the start is the goal, `None` if the reachable space is exhausted |

The method is wrapped by `@measure_execution`.

**Data structures**

```python
stack   = [(initial_state, iter(puzzle.get_successors(initial_state, order)))]
visited = {initial_state}
parents = {initial_state: (None, None)}
```

- **Stack of iterators:** each stack frame holds a state and a *lazy* iterator over its successors. The algorithm takes one successor at a time from the top frame, so siblings are generated only when the search backtracks to that frame. This is the iterative equivalent of recursive DFS, and it avoids Python's recursion limit.
- **`visited`:** a global set of every state ever generated (graph search). A state is never entered twice, even through a different path.
- **`parents`:** back-pointers used to rebuild the path, the same as in [BFS](bfs.md#62-implementation-analysis).

**Main loop**

```python
while stack:
    current_state, successors = stack[-1]
    try:
        move, next_state = next(successors)
    except StopIteration:
        stack.pop()                      # all successors explored: backtrack
        continue
    if next_state in visited:
        continue
    visited.add(next_state)
    parents[next_state] = (current_state, move)
    if puzzle.is_goal(next_state):
        return self.reconstruct_path(parents, next_state)
    stack.append((next_state, iter(puzzle.get_successors(next_state, order))))
return None
```

- **Goal test:** done when a state is generated, as in BFS.
- **Movement order:** passed to `Puzzle.get_successors`, which validates it on the first expansion and reshuffles it for every node when it starts with `R`. In DFS the order has a very large effect: it decides which branch is followed first and therefore the length of the solution.
- **No depth limit:** the search can go as deep as the number of reachable states.

## 8.3 Pseudocode

```text
function DFS-SOLVE(puzzle, order):
    s0 ← puzzle.initial_state
    if IS-GOAL(s0): return ""
    stack   ← [(s0, SUCCESSORS(s0, order))]
    visited ← {s0}
    parents ← {s0 ↦ (nil, nil)}
    while stack is not empty:
        (s, it) ← stack.TOP()
        if it is exhausted: stack.POP(); continue
        (move, s') ← it.NEXT()
        if s' ∈ visited: continue
        visited ← visited ∪ {s'}
        parents[s'] ← (s, move)
        if IS-GOAL(s'): return RECONSTRUCT(parents, s')
        stack.PUSH((s', SUCCESSORS(s', order)))
    return nil
```

## 8.4 Complexity analysis

- **Time:** $O(|S|)$ in the worst case, where $|S|$ is the number of reachable states. Each state is generated at most once.
- **Space:** the stack holds at most one frame per state on the current path. However, `visited` and `parents` keep **every** generated state, so memory grows in the same way as in BFS. The usual low-memory advantage of tree-search DFS is lost in exchange for never revisiting states.
- **Solution length:** unbounded. In the sample runs, `-d LURD` solves `puzzle1.txt` (optimal: 2 moves) with 86 moves and `puzzle3.txt` (optimal: 8 moves) with 782 moves.

In the [benchmark](../benchmark.md), DFS solved only 62 of 360 runs. Most of the other runs hit the 512 MiB memory limit, because the search wanders deep into the 4×4 state space and stores everything it sees.

## 8.5 Advantages and limitations

| Advantages | Limitations |
|---|---|
| Very simple and fast per node | Solutions are usually far from optimal |
| Never revisits a state | Stores all visited states, so memory is not bounded by depth |
| Iterator stack avoids recursion limits | No depth limit, so it can drift far from a nearby goal |
| Supports per-node random ordering | Results depend strongly on the movement order |
