# SMA\* (Simplified Memory-Bounded A\*)

**Class:** `SMAStar` ([`algorithms/sma.py`](../../algorithms/sma.py)) · **CLI:** `-s HEURISTIC`, `--sma HEURISTIC`

## 11.1 Theoretical background

[A\*](astar.md) is optimal, but it keeps every generated state in memory. SMA\* keeps the A\* ordering by $f = g + h$, but it stores **at most a fixed number of nodes**. When memory is full and a new node is needed, it **forgets** the least promising leaf (the one with the highest $f$). The forgotten leaf's $f$-value is **backed up** into its parent, so the parent still knows how good that branch was. If every other branch later turns out to be worse, the forgotten branch is regenerated.

**Properties** (with an admissible heuristic):

- **Complete** if the shallowest solution fits in memory, that is, if its path has fewer nodes than the memory limit.
- **Optimal** among the solutions that fit in memory.

## 11.2 Implementation analysis

### Configuration

| Item | Value |
|---|---|
| `DEFAULT_MEMORY_LIMIT` | `10_000` nodes, including the root. It is a constructor argument (`SMAStar(heuristic, memory_limit=...)`) and cannot be set from the CLI |
| Heuristic | Injected through the constructor, as in `AStar` |
| Movement order | Not used. Successors are always generated in `LURD` order |
| Statistics | After `solve`, the instance holds `peak_nodes`, `evictions` and `regenerations`. They are not printed |

### Solvability check

Before searching, `_is_solvable` applies the inversion-parity test for the standard goal. For an unsolvable board, `solve` returns `None` at once and the program prints `-1`. **SMA\* is the only algorithm with this check.**

### Search tree

SMA\* stores an explicit tree instead of a frontier and a visited set:

- **`_Node`:** a stored node with its `state`, `depth`, a unique `serial`, its `floor` ($f$-value), its `parent`, the `move` that led to it, and `branches`. `branches` is `None` until the node is expanded.
- **`_Branch`:** one possible move from an expanded node. It holds a `score` (the $f$-value estimate), a `child` (`None` if the child is not stored), and a `forgotten` flag.
- **`best` and `worst`:** every node caches the best action in its subtree (lowest $f$; ties prefer deeper, newer nodes) and the worst removable leaf (highest $f$; ties prefer shallower, older nodes). `_backup` refreshes these summaries from a changed node up to the root.
- **`resident`:** a dictionary from serial number to stored node. Its size is the memory usage.

### Main loop

1. Take the node selected by `root.best`. If it is the goal, return its path.
2. If the node has not been expanded yet, create its `branches`: one per successor that is **not an ancestor** (a cycle check along the path only). Each branch gets a score from `_estimate`. No child nodes are created yet.
3. Otherwise, choose its lowest-scored branch that has no stored child. If memory is full, first evict the worst leaf (`_worst_other_leaf`, which never evicts the node being extended). Then create the child, store it, and back up the scores.

The loop ends with `None` when `root.best` is $\infty$, which means no stored or forgotten branch can still lead to a solution within the memory limit.

### Score estimate (`_estimate`)

- Goal state: `max(floor, depth)`.
- A non-goal at depth `memory_limit - 1` or deeper: $\infty$, because its children could not be stored.
- Otherwise: `max(parent floor, depth + h(state))`. Taking the maximum with the parent's value (*pathmax*) keeps $f$ non-decreasing along a path. A score of `memory_limit` or more becomes $\infty$, because with an admissible heuristic such a path cannot end at a storable goal.

### Forgetting (`_forget`)

The evicted leaf is removed from `resident` and its parent's branch is updated: `score` becomes the leaf's backed-up value, `child` becomes `None`, and `forgotten` becomes `True`. When a forgotten branch is chosen again, the child is regenerated from its parent's state, and `regenerations` is incremented.

## 11.3 Pseudocode

```text
function SMA*-SOLVE(puzzle, h, M):
    if not SOLVABLE(puzzle): return nil
    root ← NODE(s0, depth 0, f = max(0, h(s0)))
    resident ← {root}
    while root.best.f < ∞:
        n ← node selected by root.best
        if IS-GOAL(n.state): return PATH(n)
        if n is not expanded:
            n.branches ← { m ↦ ESTIMATE(s', n.depth + 1, n.f) : (m, s') ∈ SUCCESSORS(n), s' ∉ ancestors(n) }
            BACKUP(n); continue
        m ← lowest-scored branch of n without a stored child
        if |resident| = M:
            FORGET(worst leaf other than n)            # back up its f into its parent
        child ← NODE(successor of n by m, f = branch score)
        resident ← resident ∪ {child};  BACKUP(n)
    return nil
```

## 11.4 Complexity analysis

- **Space:** at most `memory_limit` stored nodes, plus a set of ancestors that is built temporarily during each expansion. Memory does not grow with the length of the search.
- **Time:** in the best case close to A\*. When memory is tight, the same subtrees are forgotten and regenerated many times, and the running time can grow sharply.
- **Per-step overhead:** each expansion walks the path to the root (to collect ancestors and to back up scores), so steps are more expensive than in A\*.

In the [benchmark](../benchmark.md), SMA\* returned optimal solutions in every solved run (342 of 360). It never ran out of memory; the 18 unsolved runs, all at scramble length 20, hit the 5 s timeout.

## 11.5 Advantages and limitations

| Advantages | Limitations |
|---|---|
| Hard upper bound on stored nodes | Slower than A\* when memory is tight, because of regenerations |
| Optimal (with admissible $h$) when the solution fits in memory | The memory limit cannot be set from the CLI |
| Detects unsolvable boards immediately | Fixed `LURD` order; the movement order is not used |
| Backed-up scores avoid losing information about forgotten branches | More complex code and higher per-node cost |
