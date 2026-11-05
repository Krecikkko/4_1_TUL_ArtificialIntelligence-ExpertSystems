# Misplaced Tiles (Hamming Distance)

**Class:** `MisplacedTiles` ([`heuristics/misplaced_tiles.py`](../../heuristics/misplaced_tiles.py)) · **CLI ID:** `misplaced`

## Definition

$$
h_{mis}(n) = \sum_{i=0}^{R\cdot C-1} \big[\, s_i \neq 0 \ \land\ s_i \neq i + 1 \,\big]
$$

where $s_i$ is the value at index $i$ of the flattened state and $[\cdot]$ is 1 if the condition is true and 0 otherwise. **The empty cell is not counted.**

## Purpose

This is a cheap, admissible estimate. Every tile that is out of place must move at least once.

## Implementation

```python
class MisplacedTiles(Heuristic):
    def calculate(self, state, puzzle) -> int:
        misplaced = 0
        for index, tile in enumerate(state):
            if tile == 0:
                continue
            expected_tile = index + 1
            if tile != expected_tile:
                misplaced += 1
        return misplaced
```

- **Parameters:** `state` (flattened tuple), `puzzle` (not used).
- **Returns:** the number of misplaced non-blank tiles, in the range $0 … R \cdot C - 1$.

Procedure: go through every index. Skip `0`. Compare the tile with the value that belongs at that index (`index + 1`). Count the mismatches.

## Example

```text
State                 Goal
1 2 3                 1 2 3
4 0 6                 4 5 6
7 5 8                 7 8 0
```

Flattened: `(1, 2, 3, 4, 0, 6, 7, 5, 8)`

| index | tile | expected | misplaced? |
|---|---|---|---|
| 0–3 | 1, 2, 3, 4 | 1, 2, 3, 4 | no |
| 4 | 0 | — | skipped |
| 5 | 6 | 6 | no |
| 6 | 7 | 7 | no |
| 7 | 5 | 8 | **yes** |
| 8 | 8 | 9 | **yes** |

$h_{mis} = 2$. The true optimal cost is also 2 (`UL`).

## Complexity

$O(R \cdot C)$ time per call, $O(1)$ additional memory.

## Admissibility and consistency

- **Admissible:** each misplaced tile needs at least one move, and one move moves exactly one tile, so $h_{mis} \le h^*$.
- **Consistent:** a move changes the position of one tile only, so $h$ changes by at most 1: $h(n) \le 1 + h(n')$.

## Strengths and limitations

| Strengths | Limitations |
|---|---|
| Simple and cheap | Ignores **how far** a tile is from its goal: a tile one cell away and a tile six cells away both count as 1 |
| Admissible and consistent, so A\* stays optimal | Weak guidance on 4×4 boards, so many nodes are expanded |
| | Dominated by [Manhattan distance](manhattan.md) |
