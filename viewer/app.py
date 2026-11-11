
import tkinter as tk
from board import PuzzleBoard


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

                label.grid(row=r, column=c, padx=2, pady=2)
                row.append(label)

            self.tiles.append(row)

        self.status = tk.Label(root)
        self.status.pack()

        controls = tk.Frame(root)
        controls.pack(pady=10)

        tk.Button(
            controls, text="|<",
            command=lambda: self.jump(0)
        ).pack(side="left")

        tk.Button(
            controls, text="< Previous",
            command=self.previous
        ).pack(side="left")

        tk.Button(
            controls, text="Next >",
            command=self.next
        ).pack(side="left")

        tk.Button(
            controls, text=">|",
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

        self.status.config(
            text=f"Step {self.step} / "
                 f"{self.puzzle.get_total_steps()}"
        )

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


if __name__ == "__main__":
    root = tk.Tk()

    puzzle = PuzzleBoard(
        rows=4,
        cols=4,
        initial_board=[
            1, 2, 3, 4,
            5, 6, 7, 8,
            9, 10, 0, 12,
            13, 14, 11, 15
        ],
        solution="RDL"
    )

    PuzzleViewer(root, puzzle)
    root.mainloop()
