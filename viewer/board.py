class PuzzleBoard:
    DIRECTIONS = {
        "L": (0, 1),
        "R": (0, -1),
        "U": (1, 0),
        "D": (-1, 0),
    }

    def __init__(self, rows, cols, initial_board, solution):
        self.rows = rows
        self.cols = cols
        self.solution = solution

        self.states = [initial_board.copy()]
        self.generate_states()

    def generate_states(self):
        board = self.states[0].copy()

        for move in self.solution:
            zero = board.index(0)

            row, col = divmod(zero, self.cols)
            dr, dc = self.DIRECTIONS[move]

            new_row = row + dr
            new_col = col + dc

            if not (0 <= new_row < self.rows and
                    0 <= new_col < self.cols):
                raise ValueError(f"Invalid move: {move}")

            new_zero = new_row * self.cols + new_col

            board[zero], board[new_zero] = (
                board[new_zero], board[zero]
            )

            self.states.append(board.copy())

    def get_state(self, step):
        return self.states[step]

    def get_total_steps(self):
        return len(self.solution)
