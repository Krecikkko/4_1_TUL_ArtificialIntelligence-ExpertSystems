from .heuristic import Heuristic
from puzzle import Puzzle


class Manhattan(Heuristic):

    def calculate(
        self,
        state: tuple[int, ...],
        puzzle: Puzzle
    ) -> int:

        distance = 0

        for index, tile in enumerate(state):
            if tile == 0:
                continue

            current_row, current_col = divmod(index, puzzle.cols)

            goal_index = tile - 1

            goal_row, goal_col = divmod(goal_index, puzzle.cols)

            distance += (
                abs(current_row - goal_row)
                + abs(current_col - goal_col)
            )

        return distance
