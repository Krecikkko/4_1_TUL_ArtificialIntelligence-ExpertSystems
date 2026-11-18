import csv
import subprocess
import sys
import argparse
import re
from pathlib import Path
from time import perf_counter

from puzzle import Puzzle


ROOT = Path(__file__).resolve().parent


def verify_solution(output, puzzle):
    lines = output.splitlines()
    if len(lines) != 2:
        return "invalid_output", None

    try:
        length = int(lines[0])
    except ValueError:
        return "invalid_output", None

    moves = lines[1]
    if length == -1 and not moves:
        return "no_solution_returned", None
    if length < 0 or length != len(moves):
        return "invalid_output", None

    state = puzzle.initial_state
    for move in moves:
        successors = dict(puzzle.get_successors(state))
        if move not in successors:
            return "invalid_solution", None
        state = successors[move]

    if not puzzle.is_goal(state):
        return "invalid_solution", None

    return "solved", length


TIMEOUT_SECONDS = 5
MEMORY_MIB = 512
SEARCH_SEEDS = (42, 43, 44)

SEARCH_TIME_PATTERN = re.compile(r"Execution time:\s*([\d.]+)\s*s")

# Run each search in a fresh, resource-limited Linux process.
CHILD_CODE = """
import random
import resource
import sys

memory_bytes = int(sys.argv.pop(1))
seed = sys.argv.pop(1)
resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))

if seed:
    random.seed(int(seed))

try:
    import main
    main.main()
except MemoryError:
    sys.exit(73)
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run one board and one trial before starting the full study",
    )
    args = parser.parse_args()

    directory = ROOT / "tests" / "benchmark_boards_full"
    with (directory / "boards.csv").open(newline="", encoding="utf-8") as file:
        boards = list(csv.DictReader(file))

    if args.check:
        boards = boards[:1]

    configurations = [
        (algorithm, flag, order, "")
        for algorithm, flag in [("bfs", "-b"), ("dfs", "-d"), ("idfs", "-i")]
        for order in ("LURD", "DLUR", "RLUD")
    ] + [
        (algorithm, flag, "", heuristic)
        for algorithm, flag in [("best_first", "-h"), ("astar", "-a"), ("sma", "-s")]
        for heuristic in ("zero", "misplaced", "manhattan")
    ]

    trials = 1 if args.check else 3
    filename = "full_check.csv" if args.check else "full_results.csv"
    results_file = ROOT / filename

    # Refuse to overwrite an earlier run. Rename it before rerunning.
    if results_file.exists():
        parser.error(f"{filename} already exists. Rename it before rerunning.")

    planned = len(boards) * len(configurations) * trials
    completed = 0

    with results_file.open("x", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "board_id", "scramble_length", "board_seed", "algorithm",
            "move_order", "heuristic", "trial", "search_seed", "status",
            "elapsed_ms", "search_ms", "solution_length",
            "timeout_seconds", "address_space_limit_mib",
        ])

        for board_info in boards:
            board_id = board_info["board_id"]
            board_text = (directory / f"{board_id}.txt").read_text(encoding="utf-8")
            header, *board_lines = board_text.splitlines()
            rows, cols = map(int, header.split())
            board = [list(map(int, line.split())) for line in board_lines]
            puzzle = Puzzle(rows, cols, board)

            for trial in range(1, trials + 1):
                for algorithm, flag, order, heuristic in configurations:
                    search_seed = SEARCH_SEEDS[trial - 1] if order == "RLUD" else ""
                    command = [
                        sys.executable, "-c", CHILD_CODE,
                        str(MEMORY_MIB * 1024 * 1024), str(search_seed),
                        flag, order or heuristic,
                    ]

                    length = search_ms = None
                    start = perf_counter()
                    try:
                        result = subprocess.run(
                            command,
                            cwd=ROOT,
                            input=board_text,
                            capture_output=True,
                            text=True,
                            timeout=TIMEOUT_SECONDS,
                        )
                    except subprocess.TimeoutExpired:
                        elapsed_ms = (perf_counter() - start) * 1000
                        status = "timeout"
                    else:
                        elapsed_ms = (perf_counter() - start) * 1000
                        timing = SEARCH_TIME_PATTERN.search(result.stderr)
                        if timing:
                            search_ms = round(float(timing.group(1)) * 1000, 3)

                        if result.returncode == 73:
                            status = "memory_limit"
                        elif result.returncode != 0:
                            status = "execution_error"
                            print(result.stderr, file=sys.stderr)
                        else:
                            status, length = verify_solution(result.stdout, puzzle)

                    writer.writerow([
                        board_id, board_info["scramble_length"],
                        board_info["board_seed"], algorithm, order, heuristic,
                        trial, search_seed, status, round(elapsed_ms, 3),
                        search_ms, length, TIMEOUT_SECONDS, MEMORY_MIB,
                    ])
                    file.flush()
                    completed += 1
                    print(
                        f"[{completed}/{planned}] {board_id} {algorithm} "
                        f"{order or heuristic} trial={trial} {status} length={length}",
                        flush=True,
                    )

if __name__ == "__main__":
    main()