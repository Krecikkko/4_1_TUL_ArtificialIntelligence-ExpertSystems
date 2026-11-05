import random
from collections import deque

from .algorithm import Algorithm, measure_execution
from puzzle import Puzzle


class Bfs(Algorithm):

    @measure_execution
    def solve(
        self,
        puzzle: Puzzle,
        parameter: str
    ) -> str | None:

        initial_state = puzzle.initial_state
        order = parameter

        if puzzle.is_goal(initial_state):
            return ""

        # Queue stores states to explore.
        queue = deque([initial_state])

        # Remember the visited states.
        visited = {initial_state}

        # Store each state's parent and the move used.
        parents = {
            initial_state: (None, None)
        }

        while queue:
            current_state = queue.popleft()

            for move, next_state in puzzle.get_successors(
                current_state, order
            ):
                if next_state in visited:
                    continue

                visited.add(next_state)

                parents[next_state] = (current_state, move)

                if puzzle.is_goal(next_state):
                    return self.reconstruct_path(
                        parents, next_state
                    )

                queue.append(next_state)

        return None

    def reconstruct_path(self, parents, goal_state):
        moves = []
        current_state = goal_state

        while parents[current_state][0] is not None:
            parent_state, move = parents[current_state]
            moves.append(move)
            current_state = parent_state

        moves.reverse()
        return "".join(moves)
