# Zero Heuristic

**Class:** `Zero` ([`heuristics/zero.py`](../../heuristics/zero.py)) · **CLI ID:** `zero`

## Definition

$$
h_{zero}(n) = 0 \quad \text{for all } n
$$

## Purpose

This is a **baseline**. With $h \equiv 0$, A\*'s evaluation becomes $f(n) = g(n)$, which is **uniform-cost search**. With unit move costs, it expands states in order of depth, like BFS. Comparing other heuristics against `zero` shows how much the heuristic information actually helps.

## Implementation

```python
class Zero(Heuristic):
    def calculate(self, state, puzzle) -> int:
        return 0
```

- **Parameters:** `state`, `puzzle`. Both are ignored.
- **Returns:** `0`.

## Example

For any board, for example `1 2 3 / 4 0 6 / 7 5 8`: $h = 0$.

## Complexity

$O(1)$ time and memory.

## Admissibility and consistency

- **Admissible:** $0 \le h^*(n)$ always holds.
- **Consistent:** $0 \le 1 + 0$ for every move.

A\* with `zero` therefore returns optimal solutions.

## Strengths and limitations

| Strengths | Limitations |
|---|---|
| Trivially correct, a reference point for comparisons | Gives no guidance, so the search is as large as uninformed search |
| No computation per node | In this implementation it is slower than BFS for the same result: heap operations cost $O(\log n)$, and the goal test happens when popping rather than when generating |
