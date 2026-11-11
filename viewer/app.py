
import argparse
import tkinter as tk

from .board import PuzzleBoard


def load_puzzle(path):
    with open(path, encoding="utf-8") as f:
        values = list(map(int, f.read().split()))

    if len(values) < 2:
        raise ValueError("Invalid puzzle file")

    rows, cols = values[:2]
    board = values[2:]

    if rows <= 0 or cols <= 0:
        raise ValueError("Invalid puzzle dimensions")

    if len(board) != rows * cols:
        raise ValueError("Invalid puzzle dimensions")

    if sorted(board) != list(range(rows * cols)):
        raise ValueError("Invalid puzzle tiles")

    return rows, cols, board


def load_solution(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    if not lines:
        raise ValueError("Empty solution file")

    length = int(lines[0].strip())
    solution = lines[1].strip() if len(lines) > 1 else ""

    if length == -1:
        raise ValueError("Puzzle was not solved")

    if len(solution) != length:
        raise ValueError("Solution length mismatch")

    if any(move not in "LRUD" for move in solution):
        raise ValueError("Invalid solution moves")

    return solution


class PuzzleViewer:
    def __init__(self, root, puzzle):
        self.root = root
        self.puzzle = puzzle
        self.step = 0

        root.title("15-Puzzle Solution Viewer")

        self.board_frame = tk.Frame(root)
        self.board_frame.pack(padx=20, pady=20)

        self.tiles = []

        for r in range(puzzle.rows):
            row = []

            for c in range(puzzle.cols):
                label = tk.Label(
                    self.board_frame,
                    width=5,
                    height=2,
                    font=("Arial", 20),
                    relief="ridge",
                    borderwidth=2
                )

                label.grid(
                    row=r,
                    column=c,
                    padx=2,
                    pady=2
                )
                row.append(label)

            self.tiles.append(row)

        self.status = tk.Label(root)
        self.status.pack()

        controls = tk.Frame(root)
        controls.pack(pady=10)

        tk.Button(
            controls,
            text="|<",
            command=lambda: self.jump(0)
        ).pack(side="left")

        tk.Button(
            controls,
            text="< Previous",
            command=self.previous
        ).pack(side="left")

        tk.Button(
            controls,
            text="Next >",
            command=self.next
        ).pack(side="left")

        tk.Button(
            controls,
            text=">|",
            command=lambda: self.jump(
                self.puzzle.get_total_steps()
            )
        ).pack(side="left")

        self.slider = tk.Scale(
            root,
            from_=0,
            to=puzzle.get_total_steps(),
            orient="horizontal",
            command=lambda value: self.jump(int(value))
        )
        self.slider.pack(fill="x", padx=20)

        self.render()

    def render(self):
        board = self.puzzle.get_state(self.step)

        for i, value in enumerate(board):
            r, c = divmod(i, self.puzzle.cols)

            self.tiles[r][c].config(
                text=str(value) if value else "",
                bg="white" if value else "lightgray"
            )

        move = (
            self.puzzle.solution[self.step - 1]
            if self.step > 0 else "Initial"
        )

        self.status.config(
            text=f"Step {self.step} / "
                 f"{self.puzzle.get_total_steps()} "
                 f"| Move: {move}"
        )

        if self.slider.get() != self.step:
            self.slider.set(self.step)

    def jump(self, step):
        self.step = max(
            0,
            min(step, self.puzzle.get_total_steps())
        )
        self.render()

    def next(self):
        self.jump(self.step + 1)

    def previous(self):
        self.jump(self.step - 1)


def main():
    parser = argparse.ArgumentParser(
        description="15-Puzzle Solution Viewer"
    )

    parser.add_argument(
        "puzzle_file",
        help="Path to initial puzzle"
    )

    parser.add_argument(
        "solution_file",
        help="Path to solver output"
    )

    args = parser.parse_args()

    rows, cols, board = load_puzzle(args.puzzle_file)
    solution = load_solution(args.solution_file)

    puzzle = PuzzleBoard(
        rows=rows,
        cols=cols,
        initial_board=board,
        solution=solution
    )

    root = tk.Tk()
    PuzzleViewer(root, puzzle)
    root.mainloop()


if __name__ == "__main__":
    main()
