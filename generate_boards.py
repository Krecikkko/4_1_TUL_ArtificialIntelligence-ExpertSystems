import csv
import random
from pathlib import Path

from puzzle import Puzzle


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "tests" / "benchmark_boards_full"
GOAL = tuple(range(1, 16)) + (0,)

puzzle = Puzzle(4, 4, [list(GOAL[i:i + 4]) for i in range(0, 16, 4)])


def scramble(length, rng):
    state = GOAL
    previous = None

    for _ in range(length):
        choices = [
            next_state
            for _, next_state in puzzle.get_successors(state, "LURD")
            if next_state != previous
        ]
        previous, state = state, rng.choice(choices)

    return state


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    seen = {GOAL, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 12, 13, 14, 11, 15)}
    seed = 100

    with (OUTPUT / "boards.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["board_id", "scramble_length", "board_seed"])

        for length in (4, 8, 12, 20):
            for number in range(1, 11):
                while True:
                    state = scramble(length, random.Random(seed))
                    used_seed = seed
                    seed += 1
                    if state not in seen:
                        seen.add(state)
                        break

                board_id = f"scramble_{length}_{number}"
                rows = [
                    " ".join(map(str, state[i:i + 4]))
                    for i in range(0, 16, 4)
                ]
                (OUTPUT / f"{board_id}.txt").write_text(
                    "\n".join(["4 4", *rows]) + "\n",
                    encoding="utf-8",
                )
                writer.writerow([board_id, length, used_seed])
                print(f"Created {board_id}.txt with seed {used_seed}")


if __name__ == "__main__":
    main()