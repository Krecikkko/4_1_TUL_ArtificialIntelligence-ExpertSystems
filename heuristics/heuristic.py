from abc import ABC, abstractmethod
from puzzle import Puzzle


class Heuristic(ABC):

    @abstractmethod
    def calculate(
        self,
        state: tuple[int, ...],
        puzzle: Puzzle
    ) -> int:
        pass
