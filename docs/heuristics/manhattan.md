# Manhattan Distance

**Class:** `Manhattan` ([`heuristics/manhattan.py`](../../heuristics/manhattan.py)) · **CLI ID:** `manhattan`

## Definition

$$
h_{man}(n) = \sum_{t \neq 0} \Big( |r_t - r^{goal}_t| + |c_t - c^{goal}_t| \Big)
$$

where $(r_t, c_t)$ is the current cell of tile $t$ and $(r^{goal}_t, c^{goal}_t) = \text{divmod}(t-1,\ C)$ is its goal cell. **The empty cell is not counted.**

## Purpose

This heuristic gives a lower bound on the number of moves each tile needs, assuming the tiles could pass through each other. It is the standard admissible heuristic for sliding-tile puzzles and the most informative one in this project.

## Implementation

```python
class Manhattan(Heuristic):
    def calculate(self, state, puzzle) -> int:
        distance = 0
        for index, tile in enumerate(state):
            if tile == 0:
                continue
            current_row, current_col = divmod(index, puzzle.cols)
            goal_index = tile - 1
            goal_row, goal_col = divmod(goal_index, puzzle.cols)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance
```

- **Parameters:** `state` (flattened tuple), `puzzle`. It uses `puzzle.cols` to convert indices to rows and columns, so it works for any R×C board.
- **Returns:** the sum of the distances, a non-negative integer.

## Example

```text
State (4×4)              Goal
 1  2  3  4               1  2  3  4
 5  6  7  8               5  6  7  8
 9 10  0 12               9 10 11 12
13 14 11 15              13 14 15  0
```

(This is `tests/examples/puzzle1.txt`.) Only tiles 11 and 15 are out of place:

| Tile | Current index → (r, c) | Goal index → (r, c) | Distance |
|---|---|---|---|
| 11 | 14 → (3, 2) | 10 → (2, 2) | 1 + 0 = 1 |
| 15 | 15 → (3, 3) | 14 → (3, 2) | 0 + 1 = 1 |

$h_{man} = 2$. This equals the optimal solution length (`UL`), so the heuristic is exact here.

A more informative example (3×3): `4 1 3 / 0 2 6 / 7 5 8`

| Tile | Current (r, c) | Goal (r, c) | Distance |
|---|---|---|---|
| 4 | (0, 0) | (1, 0) | 1 |
| 1 | (0, 1) | (0, 0) | 1 |
| 2 | (1, 1) | (0, 1) | 1 |
| 5 | (2, 1) | (1, 1) | 1 |
| 8 | (2, 2) | (2, 1) | 1 |
| 3, 6, 7 | in place | | 0 |

$h_{man} = 5$, while $h_{mis} = 5$ as well. The difference grows when tiles are more than one cell from their goal. For example, a tile two rows away adds 2 to Manhattan but only 1 to misplaced tiles.

## Complexity

$O(R \cdot C)$ time per call, $O(1)$ additional memory. The value is recomputed from scratch for every generated state. It is not updated incrementally, even though a move changes only one tile's contribution.

## Admissibility and consistency

- **Admissible:** a move moves one tile by exactly one cell, so each tile needs at least its Manhattan distance in moves. Therefore $h_{man} \le h^*$.
- **Consistent:** one move changes exactly one tile's distance by ±1, so $|h(n) - h(n')| = 1 \le c(n,n')$.

## Why it is more informative than misplaced tiles

For every misplaced tile, the Manhattan contribution is ≥ 1, so $h_{man} \ge h_{mis}$ in every state (**dominance**). An admissible heuristic that dominates another one makes A\* expand at most as many nodes (apart from ties), because fewer nodes have $f(n) < C^*$. Manhattan distance counts how far a tile is from its goal, while misplaced tiles only counts whether it is out of place.

## Strengths and limitations

| Strengths | Limitations |
|---|---|
| Admissible, consistent, dominates misplaced tiles | Ignores interactions between tiles (e.g. two tiles in their goal row in reversed order, a *linear conflict*) |
| Cheap: one pass over the board | Hard 4×4 instances can still be too large for A\* in practice |
| Works for any R×C board | Assumes the goal layout `1…N−1, 0` and does not read `puzzle.goal_state` |
