from .heuristic import Heuristic
from puzzle import Puzzle


class MisplacedTiles(Heuristic):

    def calculate(
        self,
        state: tuple[int, ...],
        puzzle: Puzzle
    ) -> int:

        misplaced = 0

        for index, tile in enumerate(state):
            if tile == 0:
                continue

            expected_tile = index + 1

            if tile != expected_tile:
                misplaced += 1

        return misplaced
