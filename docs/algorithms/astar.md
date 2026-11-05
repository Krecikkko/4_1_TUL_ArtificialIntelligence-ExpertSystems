# A\* Search

**Class:** `AStar` ([`algorithms/astar.py`](../../algorithms/astar.py)) · **CLI:** `-a HEURISTIC`, `--astar HEURISTIC`

## 7.1 Theoretical background

A\* is an **informed** (heuristic) best-first search. It expands the frontier node with the lowest value of the evaluation function

$$
f(n) = g(n) + h(n)
$$

| Term | Meaning |
|---|---|
| $g(n)$ | Cost of the best known path from the initial state to $n$. Here it is the number of moves, because every move costs 1 |
| $h(n)$ | Heuristic estimate of the remaining cost from $n$ to the goal |
| $f(n)$ | Estimated cost of the cheapest solution that passes through $n$ |

The heuristic adds problem knowledge to the search, which an uninformed method like [BFS](bfs.md) does not have. A better (larger but still admissible) $h$ moves the search towards the goal and expands fewer nodes. With $h \equiv 0$, A\* becomes uniform-cost search.

## 7.2 Implementation analysis

### Construction (dependency injection)

```python
class AStar(Algorithm):
    def __init__(self, heuristic: Heuristic):
        self.heuristic = heuristic
```

`main.py` creates the heuristic with `create_heuristic(args.astar)` and passes it in. `AStar` only calls `self.heuristic.calculate(state, puzzle)`.

### `solve(self, puzzle: Puzzle, parameter: str = "") -> str | None`

| Parameter | Meaning |
|---|---|
| `puzzle` | Problem instance |
| `parameter` | **Ignored.** It exists for compatibility with the `Algorithm` interface. `main.py` calls `solve(puzzle)` |
| **returns** | Move string, `""` if the start is the goal, `None` if the open set runs empty |

The method is decorated with `@measure_execution`.

**Data structures**

| Name | Type | Purpose |
|---|---|---|
| `open_set` | `list` used as a binary heap via `heapq` | Frontier. Entries are `(f, insertion_order, g, state)` |
| `counter` | `itertools.count()` | Increasing insertion number used for tie-breaking |
| `g_score` | `dict[state, int]` | Cheapest known $g$ for every discovered state |
| `parents` | `dict[state, (parent, move)]` | Back-pointers for path reconstruction |

**Initialization**

```python
if puzzle.is_goal(initial_state): return ""
g_score = {initial_state: 0}
parents = {initial_state: (None, None)}
initial_h = self.heuristic.calculate(initial_state, puzzle)
heapq.heappush(open_set, (initial_h, next(counter), 0, initial_state))
```

**Main loop**

1. **Pop** the entry with the smallest `(f, insertion_order)`.
2. **Outdated-entry handling (lazy deletion).** `heapq` cannot change the priority of an entry already in the heap. When a cheaper path to a state is found, a *new* entry is pushed and the old one stays in the heap. When an entry is popped, `current_g != g_score[current_state]` shows that it is outdated, and it is skipped.
3. **Goal detection when popping.** The goal test runs when a state is *removed* from the heap, not when it is generated. This is needed for optimality: a goal generated through an expensive path may still be in the heap while a cheaper path is being found.
4. **Successor generation.** `puzzle.get_successors(current_state, "LURD")` always uses a **fixed** order. Random ordering is never used.
5. **Better-path detection.** For each successor, `tentative_g = current_g + 1`. If `tentative_g >= g_score.get(next_state, inf)`, the successor is skipped. Otherwise `g_score` and `parents` are updated, $h$ is computed, and `(tentative_g + h, next(counter), tentative_g, next_state)` is pushed.
6. If the heap runs empty, the method returns `None`.

**Tie-breaking.** The heap is ordered by `f`, then by the insertion counter. Among entries with equal `f`, the one inserted **first** is popped first (FIFO). The search is deterministic, and the heap never has to compare `g` or the state tuples. The counter makes every key unique. Tie-breaking does **not** prefer larger `g` (deeper nodes), even though that is a common optimization.

**No explicit closed set.** Expanded states are not stored in a closed set. They are covered by `g_score`. If a cheaper path to an already expanded state is found, the state is pushed again and **re-expanded** (reopening). With the consistent heuristics in this project, this never happens (see § 7.6).

**Path reconstruction.** `reconstruct_path(parents, goal_state)` is the same as in [BFS](bfs.md#reconstruct_pathself-parents-goal_state---str): follow the back-pointers, reverse the moves, join them.

## 7.3 Step-by-step example

Board 3×3, heuristic `manhattan`. The trace below was produced by running the real `Puzzle` and `Manhattan` classes.

```text
Initial S0         Goal
1 2 3              1 2 3
4 0 6              4 5 6
7 5 8              7 8 0
```

$h(S_0)$: tile 5 is at (2,1) and belongs at (1,1), distance 1. Tile 8 is at (2,2) and belongs at (2,1), distance 1. All other tiles are in place. So $h = 2$ and $f = 0 + 2 = 2$.

`open = [(f=2, #0, g=0, S0)]`

**Pop #0 (S0, g = 0).** Not the goal. Successors in `LURD` order:

| # | Move | Successor | g | Manhattan h | f |
|---|---|---|---|---|---|
| 1 | `L` (6 moves left) | `1 2 3 / 4 6 0 / 7 5 8` | 1 | 3 (tiles 5, 6, 8 each off by 1) | 4 |
| 2 | `U` (5 moves up) | `1 2 3 / 4 5 6 / 7 0 8` | 1 | 1 (tile 8) | **2** |
| 3 | `R` (4 moves right) | `1 2 3 / 0 4 6 / 7 5 8` | 1 | 3 (tiles 4, 5, 8) | 4 |
| 4 | `D` (2 moves down) | `1 0 3 / 4 2 6 / 7 5 8` | 1 | 3 (tiles 2, 5, 8) | 4 |

`open` (f, order): `(2,#2) (4,#1) (4,#3) (4,#4)`

**Pop #2 (g = 1, f = 2).** Not the goal. Successors (the gap is in the bottom middle, so `U` is invalid):

| # | Move | Successor | g | h | f |
|---|---|---|---|---|---|
| 5 | `L` (8 moves left) | `1 2 3 / 4 5 6 / 7 8 0` | 2 | 0 | **2** |
| 6 | `R` (7 moves right) | `1 2 3 / 4 5 6 / 0 7 8` | 2 | 2 | 4 |
| — | `D` (5 moves down) | `S0` | 2 | — | skipped: $2 \ge g(S_0)=0$ |

`open`: `(2,#5) (4,#1) (4,#3) (4,#4) (4,#6)`

**Pop #5 (g = 2, f = 2).** This is the goal. Reconstruction gives **`UL`**, with length 2.

Only two expansions were needed. The `f = 4` nodes were never expanded, because the heuristic correctly ranked them as worse. For comparison, $h_{misplaced}(S_0) = 2$ as well. On larger instances the two heuristics differ much more (see [heuristics](../heuristics/README.md#comparison)).

## 7.4 Pseudocode

```text
function ASTAR-SOLVE(puzzle, h):
    s0 ← puzzle.initial_state
    if IS-GOAL(s0): return ""
    g ← {s0 ↦ 0};  parents ← {s0 ↦ (nil, nil)};  c ← 0
    open ← min-heap;  PUSH(open, (h(s0), c++, 0, s0))
    while open is not empty:
        (f, _, gs, s) ← POP-MIN(open)
        if gs ≠ g[s]: continue                         # outdated entry
        if IS-GOAL(s): return RECONSTRUCT(parents, s)
        for (move, s') in SUCCESSORS(s, "LURD"):
            t ← gs + 1
            if t ≥ g.get(s', ∞): continue
            g[s'] ← t;  parents[s'] ← (s, move)
            PUSH(open, (t + h(s'), c++, t, s'))
    return nil
```

`RECONSTRUCT` is the same as in [BFS](bfs.md#64-pseudocode).

## 7.5 Complexity analysis

- **Time:** in the worst case $O(b^{d})$, the same as BFS. In practice it is much less with a good heuristic. The number of expansions grows roughly as $b_{\text{eff}}^{\,d}$, and a more informed $h$ lowers $b_{\text{eff}}$. Each push or pop costs $O(\log |open|)$. Each heuristic evaluation costs $O(R \cdot C)$ for the implemented heuristics, which recompute $h$ from scratch for every generated state.
- **Space:** $O(\text{number of generated states})$. `g_score`, `parents` and the heap (which also holds outdated entries) all grow with the search. Like BFS, A\* keeps every discovered state in memory, so **memory is usually the limit, not time**. SMA\* (planned) is meant to address this.
- **Effect of heuristic quality:** `zero` < `misplaced` < `manhattan` in how informative they are (see [heuristics](../heuristics/README.md#comparison)). With `zero`, A\* expands the same levels as BFS, and it is slower because of the heap and the late goal test.
- **Hard instances:** in a local run, `tests/examples/puzzle2.txt`, which is solvable, did not finish within 60 seconds with `manhattan`. Hard 4×4 instances usually need stronger heuristics (linear conflict, pattern databases) or memory-bounded or iterative methods (IDA\*, SMA\*). None of these are implemented.
- **Unsolvable inputs:** there is no parity check. A\* would explore the entire reachable component before returning `None`.

## 7.6 Optimality and completeness

- **Completeness:** the state space is finite and duplicates are detected, so A\* always terminates, given enough memory. It finds a solution if one exists.
- **Optimality:** A\* returns an optimal solution if $h$ is **admissible**, that is, $h(n) \le h^*(n)$ for all $n$, where $h^*$ is the true remaining cost. This implementation tests for the goal when popping and allows reopening, so admissibility alone is enough.
- **Consistency (monotonicity):** $h(n) \le c(n, n') + h(n')$ for every move. A consistent heuristic makes $f$ non-decreasing along every path. Then the first time a state is popped, its $g$ is already optimal, and no state is ever reopened.

| Heuristic | Admissible | Consistent | Reason |
|---|---|---|---|
| `zero` | ✔ | ✔ | $0 \le h^*$ trivially |
| `misplaced` | ✔ | ✔ | Each misplaced tile needs at least one move, and one move changes the count by at most 1 |
| `manhattan` | ✔ | ✔ | Each move moves one tile by one cell, so $h$ changes by exactly ±1 |

All `-a` runs with the implemented heuristics therefore return optimal (shortest) solutions.

## 7.7 Comparison with BFS

| Aspect | BFS (`Bfs`) | A\* (`AStar`) |
|---|---|---|
| Search strategy | Uninformed, level by level | Informed, by lowest $f = g + h$ |
| Frontier data structure | `deque` (FIFO) | `heapq` binary heap |
| Bookkeeping | `visited` set + `parents` | `g_score` dict + `parents` |
| Node selection | Oldest generated node | Smallest `(f, insertion order)` |
| Goal test | When a node is generated | When a node is popped |
| Heuristic usage | None | Injected `Heuristic.calculate` |
| Movement order | Respected, incl. random `R…` | Ignored, fixed `LURD` |
| Optimality | Yes (unit costs) | Yes, with admissible $h$ |
| Completeness | Yes (finite space) | Yes (finite space) |
| Time complexity | $O(b^d)$ | $O(b^d)$ worst case; much less with an informed $h$ |
| Memory | $O(b^d)$, all generated states | All generated states plus outdated heap entries |
| Per-node overhead | $O(1)$ queue operations | $O(\log n)$ heap operations + $O(R \cdot C)$ heuristic |
| Practical performance | Only shallow instances | Much deeper instances with `manhattan`, but still limited by memory on hard 4×4 puzzles |

No benchmark results are included here, because none have been measured systematically in this project.
