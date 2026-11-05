from .heuristic import Heuristic
from puzzle import Puzzle


class Zero(Heuristic):

    def calculate(
        self,
        state: tuple[int, ...],
        puzzle: Puzzle
    ) -> int:
        return 0
