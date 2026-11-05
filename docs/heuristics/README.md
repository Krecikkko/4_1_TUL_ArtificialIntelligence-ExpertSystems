# Heuristics

A heuristic $h(n)$ estimates the number of moves still needed to reach the goal from state $n$. Informed algorithms use it to choose which node to expand next. Currently only [A\*](../algorithms/astar.md) uses one. Best-first and SMA\* are planned to use the same interface.

## Shared interface

```python
# heuristics/heuristic.py
class Heuristic(ABC):
    @abstractmethod
    def calculate(self, state: tuple[int, ...], puzzle: Puzzle) -> int: ...
```

| Parameter | Meaning |
|---|---|
| `state` | Flattened row-major board tuple, where `0` is the empty cell |
| `puzzle` | The `Puzzle` instance. It gives access to the geometry (`puzzle.cols`) |
| **returns** | Non-negative integer estimate |

Heuristics are **stateless**. The algorithm calls `calculate` once for every state it generates. Because the interface takes the whole `Puzzle`, any informed algorithm can use any heuristic with any board size. The heuristic is chosen at runtime by name:

```python
from heuristics.factory import create_heuristic
h = create_heuristic("manhattan")   # -> Manhattan()
```

`create_heuristic` lowercases the ID, looks it up in a dictionary of classes, and raises `ValueError` for unknown names. It is **not** re-exported from `heuristics/__init__.py`, so import it from `heuristics.factory`.

## Implemented heuristics

| CLI ID | Class | Definition | Docs |
|---|---|---|---|
| `zero` | `Zero` | $h(n) = 0$ | [zero.md](zero.md) |
| `misplaced` | `MisplacedTiles` | Number of non-blank tiles that are not in their goal cell | [misplaced-tiles.md](misplaced-tiles.md) |
| `manhattan` | `Manhattan` | Sum of the grid distances of all tiles to their goal cells | [manhattan.md](manhattan.md) |

## Comparison

| Property | `zero` | `misplaced` | `manhattan` |
|---|---|---|---|
| Admissible | ✔ | ✔ | ✔ |
| Consistent | ✔ | ✔ | ✔ |
| Cost per call | $O(1)$ | $O(R \cdot C)$ | $O(R \cdot C)$ |
| Informativeness | none | low | higher |

For every state: $0 = h_{zero} \le h_{misplaced} \le h_{manhattan} \le h^*$. Every misplaced tile adds at least 1 to the Manhattan sum, so Manhattan **dominates** misplaced tiles, and A\* with Manhattan never expands more nodes than with misplaced tiles (apart from tie-breaking effects).

## Implementation note: implicit goal layout

`MisplacedTiles` and `Manhattan` do not read `puzzle.goal_state`. They compute goal positions with the formula *tile `t` belongs at index `t − 1`*. This matches the goal that `Puzzle` builds (`1…N−1, 0`). If the goal definition ever changes, both heuristics have to be updated as well.
