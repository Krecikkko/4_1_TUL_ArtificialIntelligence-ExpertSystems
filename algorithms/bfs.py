import random
from collections import deque
from .algorithm import Algorithm, measure_execution


class Bfs(Algorithm):

    def __init__(self):
        # Directions describe movement of numbered tiles.
        # Each offset indicates where the tile is located
        # relative to the empty space.
        self.directions = {
            "L": (0, 1),
            "R": (0, -1),
            "U": (1, 0),
            "D": (-1, 0)
        }

    def get_free_space(self, board: tuple[int, ...]) -> int:
        return board.index(0)

    def get_successors(
        self,
        board: tuple[int, ...],
        rows: int,
        cols: int,
        order: str
    ):
        zero_index = self.get_free_space(board)
        zero_row, zero_col = divmod(zero_index, cols)

        # Randomize move order separately for every node
        if order.startswith("R"):
            move_order = list("LRUD")
            random.shuffle(move_order)
        else:
            move_order = order
            
        for move in move_order:
            dr, dc = self.directions[move]

            tile_row = zero_row + dr
            tile_col = zero_col + dc

            # Check whether the tile is inside the board.
            if not (0 <= tile_row < rows):
                continue

            if not (0 <= tile_col < cols):
                continue

            tile_index = tile_row * cols + tile_col

            # Create the next state.
            new_board = list(board)

            new_board[zero_index], new_board[tile_index] = (
                new_board[tile_index],
                new_board[zero_index]
            )

            yield move, tuple(new_board)

    @measure_execution
    def solve(
        self,
        order: str,
        rows: int,
        cols: int,
        board: list[list[int]]
    ) -> str | None:

        # Convert the 2D board into an immutable tuple.
        initial_state = tuple(
            value
            for row in board
            for value in row
        )

        # Generate the goal state.
        goal_state = tuple(range(1, rows * cols)) + (0,)

        # Validate the movement order.
        if len(order) != 4 or set(order) != set("LRUD"):
            raise ValueError("Invalid movement order")

        if initial_state == goal_state:
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

            for move, next_state in self.get_successors(
                current_state, rows, cols, order
            ):
                if next_state in visited:
                    continue

                visited.add(next_state)

                parents[next_state] = (current_state, move)

                if next_state == goal_state:
                    return self.reconstruct_path(
                        parents, goal_state
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
