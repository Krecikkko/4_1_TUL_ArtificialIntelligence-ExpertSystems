# Puzzle Representation

All problem-specific knowledge lives in the `Puzzle` class in [`puzzle.py`](../puzzle.py). Search algorithms use only three of its members: `initial_state`, `is_goal()` and `get_successors()`.

## State encoding

A state is a **flat, row-major tuple** of `rows · cols` integers, where `0` is the empty cell. The board

```text
1 2 3
4 0 6
7 5 8
```

is stored as `(1, 2, 3, 4, 0, 6, 7, 5, 8)`. An index `i` and a cell `(row, col)` convert as follows:

$$
i = row \cdot C + col, \qquad (row,\ col) = \text{divmod}(i,\ C)
$$

The constructor flattens the input board (`list[list[int]]`) with a generator expression:

```python
self.initial_state = tuple(value for row in board for value in row)
```

### Why immutable tuples

- **Hashability.** Tuples can be members of `set` and keys of `dict`. BFS uses `visited` and `parents`, and A\* uses `g_score` and `parents`. These structures need the state itself as the key.
- **Safety.** A state cannot be changed after it has been stored. Successors are built from a temporary `list` copy and then frozen with `tuple(...)`.
- **Cheap comparison.** The goal test is a single tuple equality check.

The cost of this choice is that every successor is a new tuple of `R·C` elements, which means $O(R \cdot C)$ time and memory per generated state.

## Goal state

```python
self.goal_state = tuple(range(1, rows * cols)) + (0,)
```

For a 4×4 board this is `(1, 2, …, 15, 0)`. The goal is the same for every board of a given size. It cannot be configured.

## Locating the empty cell

```python
def get_free_space(self, state): return state.index(0)
```

This is a linear scan, $O(R \cdot C)$. It runs once per expanded node. The position of `0` is not cached in the state.

## Movement semantics

**The move letters describe the numbered tile that moves into the empty cell, not the movement of the empty cell.** This matches the assignment. The `directions` table therefore stores, for each letter, the position of the moving tile relative to the empty cell:

```python
self.directions = {
    "L": (0, 1),   # tile to the RIGHT of the gap moves LEFT
    "R": (0, -1),  # tile to the LEFT  of the gap moves RIGHT
    "U": (1, 0),   # tile BELOW the gap moves UP
    "D": (-1, 0),  # tile ABOVE the gap moves DOWN
}
```

When a tile moves in direction *X*, the empty cell moves in the **opposite** direction.

### Example

```text
Before          Move "U"        Move "L" (from "Before")
1 2 3           1 2 3           1 2 3
4 0 6           4 5 6           4 6 0
7 5 8           7 0 8           7 5 8
```

- `U`: tile **5**, below the gap, moves **up**, and the gap moves down. If the letters described the gap instead, this would be called "D".
- `L`: tile **6**, right of the gap, moves **left**, and the gap moves right.

With the move semantics clear, the solution `UL` for `tests/examples/puzzle1.txt` reads as: tile 11 moves up, then tile 15 moves left.

## Successor generation

```python
def get_successors(self, state, order="LURD"):
    zero_index = self.get_free_space(state)
    zero_row, zero_col = divmod(zero_index, self.cols)

    if len(order) != 4 or set(order) != set("LRUD"):
        raise ValueError("Invalid movement order")

    if order.startswith("R"):
        move_order = list("LRUD"); random.shuffle(move_order)
    else:
        move_order = order

    for move in move_order:
        dr, dc = self.directions[move]
        tile_row, tile_col = zero_row + dr, zero_col + dc
        if not (0 <= tile_row < self.rows): continue
        if not (0 <= tile_col < self.cols): continue
        tile_index = tile_row * self.cols + tile_col
        new_state = list(state)
        new_state[zero_index], new_state[tile_index] = new_state[tile_index], new_state[zero_index]
        yield move, tuple(new_state)
```

(Condensed. Line breaks differ from the source.)

Key properties:

1. **Generator.** Successors are produced lazily as `(move, state)` pairs in the requested order. BFS uses this to stop as soon as a goal successor appears.
2. **Validation on every call.** The order is checked each time, before any successor is produced. Because it is a generator, the check only runs when the generator is first iterated.
3. **No parent pruning.** The move that would undo the previous move is still generated. The algorithms remove such duplicates with their visited or `g_score` bookkeeping.
4. **Uniform cost.** Every move costs 1.

### Boundary handling

A move is valid only if the **moving tile** is on the board. The two range checks skip directions whose source cell lies outside the board. The number of successors (the branching factor without duplicate removal) therefore depends on where the gap is:

| Gap position | Successors |
|---|---|
| Corner | 2 |
| Edge (not corner) | 3 |
| Interior | 4 |

Boards with one row or one column work the same way: vertical or horizontal moves are simply never valid.

## Random successor ordering

> **Assignment requirement:** if the movement order begins with `R`, successor ordering must be randomized independently for each expanded node.

**Status: implemented.** The shuffle is done *inside* `get_successors`, and both BFS and A\* call `get_successors` once per expanded node. Every expansion therefore gets a fresh `random.shuffle` of `["L", "R", "U", "D"]`. The order is not chosen once per run.

Caveats:

- The RNG is **not seeded**, so runs cannot be reproduced. The solution length found by BFS is still optimal, but the move sequence may differ between runs when several optimal solutions exist.
- The parameter must still be a valid four-letter permutation. `R` alone is rejected (see the [CLI reference](cli-reference.md#movement-order)).
- Any permutation starting with `R` means "random". The six deterministic orders `R???` cannot be used.
- `AStar` always passes `"LURD"`, so it never uses random ordering.
