import random


class Puzzle:

    def __init__(
        self,
        rows: int,
        cols: int,
        board: list[list[int]]
    ):
        self.rows = rows
        self.cols = cols

        self.initial_state = tuple(
            value
            for row in board
            for value in row
        )

        self.goal_state = (
            tuple(range(1, rows * cols)) + (0,)
        )

        # Directions represent movements of numbered tiles.
        self.directions = {
            "L": (0, 1),
            "R": (0, -1),
            "U": (1, 0),
            "D": (-1, 0)
        }

    def get_free_space(self, state: tuple[int, ...]) -> int:
        return state.index(0)

    def is_goal(self, state: tuple[int, ...]) -> bool:
        return state == self.goal_state

    def get_successors(
        self,
        state: tuple[int, ...],
        order: str = "LURD"
    ):
        zero_index = self.get_free_space(state)
        zero_row, zero_col = divmod(zero_index, self.cols)

        if len(order) != 4 or set(order) != set("LRUD"):
            raise ValueError("Invalid movement order")

        # Assignment: order starting with R means random.
        if order.startswith("R"):
            move_order = list("LRUD")
            random.shuffle(move_order)
        else:
            move_order = order

        for move in move_order:
            dr, dc = self.directions[move]

            tile_row = zero_row + dr
            tile_col = zero_col + dc

            if not (0 <= tile_row < self.rows):
                continue

            if not (0 <= tile_col < self.cols):
                continue

            tile_index = tile_row * self.cols + tile_col

            new_state = list(state)

            new_state[zero_index], new_state[tile_index] = (
                new_state[tile_index],
                new_state[zero_index]
            )

            yield move, tuple(new_state)
