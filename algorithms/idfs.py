from itertools import count

from puzzle import Puzzle

from .algorithm import Algorithm, measure_execution


class Idfs(Algorithm):
    @measure_execution
    def solve(self, puzzle: Puzzle, parameter: str) -> str | None:
        """Return a shortest solution, or None if the search is exhausted."""
        if len(parameter) != 4 or set(parameter) != set("LRUD"):
            raise ValueError("Move order must be a permutation of LRUD")

        for limit in count():
            solution, cutoff = self._depth_limited_search(puzzle, parameter, limit)
            if solution is not None:
                return solution
            if not cutoff:
                return None

    def _depth_limited_search(
        self, puzzle: Puzzle, order: str, limit: int
    ) -> tuple[str | None, bool]:
        initial_state = puzzle.initial_state
        if puzzle.is_goal(initial_state):
            return "", False

        # Each frame retains its successor order while DFS explores a child.
        stack = [(initial_state, iter(puzzle.get_successors(initial_state, order)))]
        on_path = {initial_state}
        moves: list[str] = []
        cutoff = False

        while stack:
            state, successors = stack[-1]
            successor = next(successors, None)

            if successor is None:
                stack.pop()
                on_path.remove(state)
                if stack:
                    moves.pop()
                continue

            move, next_state = successor
            if next_state in on_path:
                continue

            if len(moves) == limit:
                # This branch could continue at a larger depth limit.
                cutoff = True
                stack.pop()
                on_path.remove(state)
                if stack:
                    moves.pop()
                continue

            moves.append(move)
            if puzzle.is_goal(next_state):
                return "".join(moves), cutoff

            on_path.add(next_state)
            stack.append(
                (next_state, iter(puzzle.get_successors(next_state, order)))
            )

        return None, cutoff
