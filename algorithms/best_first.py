"""Greedy best-first search for the sliding-tile puzzle."""

from heapq import heappop, heappush
from itertools import count

from heuristics import Heuristic
from puzzle import Puzzle

from .algorithm import Algorithm, measure_execution

_State = tuple[int, ...]


class BestFirst(Algorithm):
    def __init__(self, heuristic: Heuristic) -> None:
        self.heuristic = heuristic

    @measure_execution
    def solve(self, puzzle: Puzzle, parameter: str = "") -> str | None:
        """Return the first solution selected by heuristic priority, if any."""
        initial_state = puzzle.initial_state
        insertion_order = count()
        frontier = [
            (
                self.heuristic.calculate(initial_state, puzzle),
                next(insertion_order),
                initial_state,
            )
        ]

        # The parent map doubles as the set of discovered states.
        parents: dict[_State, tuple[_State, str] | None] = {initial_state: None}

        while frontier:
            _, _, state = heappop(frontier)
            if puzzle.is_goal(state):
                return self._reconstruct_path(parents, state)

            # The CLI selects a heuristic, so use Puzzle's default move order.
            for move, successor in puzzle.get_successors(state):
                if successor in parents:
                    continue

                parents[successor] = (state, move)
                # Use h alone. The counter preserves FIFO order on ties.
                priority = self.heuristic.calculate(successor, puzzle)
                heappush(frontier, (priority, next(insertion_order), successor))

        return None

    @staticmethod
    def _reconstruct_path(
        parents: dict[_State, tuple[_State, str] | None], state: _State
    ) -> str:
        moves = []
        while (entry := parents[state]) is not None:
            state, move = entry
            moves.append(move)
        return "".join(reversed(moves))
