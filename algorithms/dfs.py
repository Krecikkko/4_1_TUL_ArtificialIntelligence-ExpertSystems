from .algorithm import Algorithm, measure_execution
from puzzle import Puzzle


class Dfs(Algorithm):

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

        # Stack stores states and their successor iterators.
        stack = [
            (
                initial_state,
                iter(puzzle.get_successors(initial_state, order))
            )
        ]

        # Remember visited states.
        visited = {initial_state}

        # Store each state's parent and the move used.
        parents = {
            initial_state: (None, None)
        }

        while stack:
            current_state, successors = stack[-1]

            try:
                move, next_state = next(successors)
            except StopIteration:
                # All successors have been explored.
                stack.pop()
                continue

            if next_state in visited:
                continue

            visited.add(next_state)

            parents[next_state] = (current_state, move)

            if puzzle.is_goal(next_state):
                return self.reconstruct_path(
                    parents, next_state
                )

            # Explore this successor before its siblings.
            stack.append(
                (
                    next_state,
                    iter(puzzle.get_successors(next_state, order))
                )
            )

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
