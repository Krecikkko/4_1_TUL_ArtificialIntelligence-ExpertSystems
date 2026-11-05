
from .algorithm import Algorithm, measure_execution
from heuristics import Heuristic
from puzzle import Puzzle


class AStar(Algorithm):

    def __init__(self, heuristic: Heuristic):
        self.heuristic = heuristic

    @measure_execution
    def solve(
        self,
        puzzle: Puzzle,
        parameter: str = ""
    ) -> str | None:

        initial_state = puzzle.initial_state

        h = self.heuristic.calculate(
            initial_state, puzzle
        )

        # Priority = g(n) + h(n)
        # Implement A* search here.

        raise NotImplementedError
