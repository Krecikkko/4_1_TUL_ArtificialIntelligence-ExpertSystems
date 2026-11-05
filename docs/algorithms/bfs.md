# Breadth-First Search (BFS)

**Class:** `Bfs` ([`algorithms/bfs.py`](../../algorithms/bfs.py)) · **CLI:** `-b ORDER`, `--bfs ORDER`

## 6.1 Theoretical background

Breadth-first search is an **uninformed** (blind) search strategy. It uses only the problem definition (initial state, successor function, goal test) and no estimate of how close a state is to the goal.

BFS explores the state space **level by level**. All states at depth $d$ are expanded before any state at depth $d+1$. A **FIFO queue** produces this order: newly generated states are added at the back, and the next state to expand is taken from the front.

**Properties** (for branching factor $b$ and the depth $d$ of the shallowest goal):

- **Complete** if $b$ is finite. The puzzle has $b \le 4$, so a solution is always found if one exists, given enough memory.
- **Optimal** when all step costs are equal. Every puzzle move costs 1, so the first goal found has the minimum number of moves.

## 6.2 Implementation analysis

### `solve(self, puzzle: Puzzle, parameter: str) -> str | None`

| Parameter | Meaning |
|---|---|
| `puzzle` | The `Puzzle` instance (initial state, goal test, successor function) |
| `parameter` | Movement order, e.g. `"LURD"`, or one starting with `R` for random order |
| **returns** | Move string, `""` if the start is the goal, `None` if the search space is exhausted |

The method is wrapped by `@measure_execution`.

**Initialization**

```python
if puzzle.is_goal(initial_state):
    return ""
queue   = deque([initial_state])
visited = {initial_state}
parents = {initial_state: (None, None)}
```

- **Queue:** a `collections.deque`, which gives $O(1)$ `append` and `popleft`.
- **Visited-state tracking:** `visited` holds every state that has ever been **generated**, not only expanded ones. A state is marked when it is added to the queue. This guarantees that each state enters the queue at most once.
- **Parent tracking:** `parents[state] = (parent_state, move)`. The `visited` set and the key set of `parents` always contain the same states. They are kept as two separate structures.

**Main loop**

```python
while queue:
    current_state = queue.popleft()
    for move, next_state in puzzle.get_successors(current_state, order):
        if next_state in visited:
            continue
        visited.add(next_state)
        parents[next_state] = (current_state, move)
        if puzzle.is_goal(next_state):
            return self.reconstruct_path(parents, next_state)
        queue.append(next_state)
return None
```

- **Successor generation and movement order:** `order` is passed directly to `Puzzle.get_successors`. That method validates it, shuffles it for each node when it starts with `R`, and yields successors in that order (see [puzzle-representation](../puzzle-representation.md#successor-generation)). The order decides which of several optimal solutions BFS returns. It does not change the solution length.
- **Goal detection (early goal test):** each successor is tested **when it is generated**, not when it is dequeued. This is valid for BFS: every state at depth $d$ is generated before any state at depth $d+1$, so the first goal generated is at minimum depth. The early test saves the expansion of an entire level.
- **Termination:** the method returns as soon as a goal successor is generated, or returns `None` when the queue is empty. There is no depth, time or memory limit.

### `reconstruct_path(self, parents, goal_state) -> str`

Follows `parents` from `goal_state` back to the state whose parent is `None` (the initial state), collects the moves, reverses the list and joins it into a string. Time complexity is $O(d)$.

## 6.3 Algorithm walkthrough

The following 2×3 puzzle is solved with order `LURD`. The goal is `(1, 2, 3, 4, 5, 0)`. The trace below was produced by running the same logic against the real `Puzzle` class.

```text
Initial            Goal
1 2 3              1 2 3
0 4 5              4 5 0
```

Initial state `S0 = (1, 2, 3, 0, 4, 5)`. The gap is in the bottom-left corner, so only two moves are valid.

**Initialization:** `queue = [S0]`, `visited = {S0}`, `S0` is not the goal.

**Iteration 1: pop `S0`.** Successors in `LURD` order:

| Move | Valid? | Successor | Action |
|---|---|---|---|
| `L` | yes (tile 4 moves left) | `S1 = (1, 2, 3, 4, 0, 5)` | new, not the goal, enqueue |
| `U` | no (no tile below the gap) | — | — |
| `R` | no (no tile left of the gap) | — | — |
| `D` | yes (tile 1 moves down) | `S2 = (0, 2, 3, 1, 4, 5)` | new, not the goal, enqueue |

`queue = [S1, S2]`, `visited = {S0, S1, S2}`

**Iteration 2: pop `S1`** (the gap is in the bottom middle):

| Move | Successor | Action |
|---|---|---|
| `L` (tile 5 moves left) | `(1, 2, 3, 4, 5, 0)` | new, **goal** → `parents[goal] = (S1, "L")`, return |

The `U`, `R` and `D` successors of `S1` are never generated, because the generator stops at the goal. `S2` is still in the queue and is never expanded.

**Reconstruction:** goal → (`L`) → `S1` → (`L`) → `S0`. Reversed and joined: **`LL`**. The program prints `2` and `LL`.

## 6.4 Pseudocode

```text
function BFS-SOLVE(puzzle, order):
    s0 ← puzzle.initial_state
    if IS-GOAL(s0): return ""
    queue   ← FIFO containing s0
    visited ← {s0}
    parents ← {s0 ↦ (nil, nil)}
    while queue is not empty:
        s ← queue.POP-FRONT()
        for (move, s') in SUCCESSORS(s, order):       # random per call if order[0] = 'R'
            if s' ∈ visited: continue
            visited ← visited ∪ {s'}
            parents[s'] ← (s, move)
            if IS-GOAL(s'): return RECONSTRUCT(parents, s')
            queue.PUSH-BACK(s')
    return nil                                         # printed as -1

function RECONSTRUCT(parents, g):
    moves ← []
    while parents[g].parent ≠ nil:
        (p, m) ← parents[g];  moves.APPEND(m);  g ← p
    return JOIN(REVERSE(moves))
```

## 6.5 Complexity analysis

Let $b$ be the effective branching factor and $d$ the optimal solution depth.

- **Time:** $O(b^{d})$ generated states. Because of the early goal test, the last level is generated only partly. Each generation also costs $O(R \cdot C)$ to copy the tuple, plus hashing.
- **Space:** $O(b^{d})$. The frontier alone is $O(b^d)$, and `visited` and `parents` store **every** generated state until the search ends.
- **Branching factor:** between 2 and 4 depending on where the gap is (see [boundary handling](../puzzle-representation.md#boundary-handling)). On a 4×4 board the average over gap positions is $(4\cdot2 + 8\cdot3 + 4\cdot4)/16 = 3$. After removing the immediate reverse move, the effective growth rate is about 2.13 for the 15-puzzle, as reported in the literature (Korf).
- **State space:** half of the $(R \cdot C)!$ permutations can be reached from a given start. That is $9!/2 = 181\,440$ states for 3×3, but $16!/2 \approx 1.05 \times 10^{13}$ for 4×4.

**Why BFS is impractical for hard 4×4 puzzles.** Optimal 15-puzzle solutions can be up to 80 moves long, and random instances often need 50 or more. With $2.13^{50} \approx 10^{16}$ the number of nodes reaches the size of the entire reachable space. Each stored state needs a 16-element tuple plus entries in two hash tables (roughly hundreds of bytes per state in CPython). Main memory runs out after a few tens of millions of states. This happens long before such depths are reached. BFS is practical on 3×3 boards and on 4×4 instances that are only a few moves from the goal.

For **unsolvable** inputs, BFS has no early exit. It would have to enumerate the whole reachable half of the state space before it could return `None` (`-1`).

## 6.6 Advantages and limitations

| Advantages | Limitations |
|---|---|
| Complete and optimal for unit move costs | Exponential memory: stores every generated state |
| Simple, with no heuristic required | Ignores any information about the goal |
| Early goal test saves one level of expansion | No solvability check, depth limit or memory limit |
| Supports per-node random ordering | Random mode is unseeded, so runs are not reproducible |
| Duplicate detection prevents cycles and repeated states | `visited` and `parents` contain the same keys, which uses more memory than needed |
