import heapq
from itertools import count

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

        if puzzle.is_goal(initial_state):
            return ""

        # Priority queue
        # (f_cost, insertion_order, g_cost, state)
        open_set = []

        # Ensures deterministric tie-breaking.
        counter = count()

        # Cheapest known cost from start to each state
        g_score = {
            initial_state: 0
        }

        # Store parent state and move from path reconstruction
        parents = {
            initial_state: (None, None)
        }

        initial_h = self.heuristic.calculate(
            initial_state, puzzle
        )

        heapq.heappush(
            open_set,
            (initial_h, next(counter), 0, initial_state)
        )

        while(open_set):
            f_cost, _, current_g, current_state = (
                heapq.heappop(open_set)
            )

            # Ignore outdated entries in the priority queue
            if current_g != g_score[current_state]:
                continue

            # Check whether the goal has been reached
            if puzzle.is_goal(current_state):
                return self.reconstruct_path(
                    parents,
                    current_state
                )

            # Explore all possible successors
            for move, next_state in puzzle.get_successors(
                current_state,
                "LURD"
            ):
                tentative_g = current_g + 1

                # Skip if a cheaper or equal path is known
                if tentative_g >= g_score.get(
                    next_state,
                    float("inf")
                ):
                    continue

                # Found a better path to next_state
                g_score[next_state] = tentative_g

                parents[next_state] = (
                    current_state,
                    move
                )

                h = self.heuristic.calculate(
                    next_state,
                    puzzle
                )

                f = tentative_g + h

                heapq.heappush(
                    open_set,
                    (
                        f,
                        next(counter),
                        tentative_g,
                        next_state
                    )
                )
        
        return None


    def reconstruct_path(
        self,
        parents: dict,
        goal_state: tuple[int, ...]
    ) -> str:

        moves = []
        current_state = goal_state

        while parents[current_state][0] is not None:
            parent_state, move = parents[current_state]
            moves.append(move)
            current_state = parent_state

        moves.reverse()

        return "".join(moves)
