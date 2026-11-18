# Getting Started

## Requirements

- Python **3.10+**. The type hints `str | None` and `tuple[int, ...]` are evaluated at import time and fail on older versions.
- No third-party packages.

## Installation

```bash
git clone <repository-url>
cd 4_1_TUL_ArtificialIntelligence-ExpertSystems

# Optional: an isolated environment (the project has no external dependencies)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

You do not need to install anything else. Run the solver from the repository root so that the top-level modules `puzzle`, `algorithms` and `heuristics` can be imported.

## First run

The repository ships with three sample inputs in [`tests/examples/`](../tests/examples/).

```bash
python3 main.py -b LURD < tests/examples/puzzle1.txt
```

Output (the log lines go to standard error; the timing value will differ):

```text
[INFO] Algorithm started
[INFO] Algorithm finished | Execution time: 0.000102 s
2
UL
```

The first line on standard output is the solution length. The second line is the move sequence. To see only the solution, discard standard error:

```bash
python3 main.py -a manhattan < tests/examples/puzzle1.txt 2>/dev/null
```

## Writing your own input

The input is the board size followed by the board rows. `0` is the empty cell:

```text
3 3
1 2 3
4 0 6
7 5 8
```

```bash
python3 main.py -a manhattan < my_puzzle.txt
```

You can also type the input interactively: run the command without `<` and type the lines by hand.

## Notes on the sample inputs

| File | Size | Notes |
|---|---|---|
| `puzzle1.txt` | 4×4 | Two moves from the goal (`UL`). Every algorithm solves it instantly (DFS with a long, non-optimal solution). |
| `puzzle3.txt` | 4×4 | Eight moves from the goal (`RRULDLUL`). Every algorithm finishes quickly. |
| `puzzle2.txt` | 4×4 | Solvable, but far from the goal. Only Best-first solves it in reasonable time (`-h manhattan` finds a 188-move solution). A\*, SMA\* and the uninformed algorithms do not finish in practice. |

Ready-to-paste commands for every algorithm are in [`commands.md`](../commands.md).

## Viewing a solution

The `viewer` package opens a Tkinter window that replays a solution move by move. It needs the puzzle file and a file with the solver's output:

```bash
mkdir -p tests/solutions
python3 main.py -a manhattan < tests/examples/puzzle3.txt > tests/solutions/solution.txt
python3 -m viewer.app tests/examples/puzzle3.txt tests/solutions/solution.txt
```

Use the `|<`, `< Previous`, `Next >` and `>|` buttons or the slider to move through the steps. The viewer validates both files and refuses a solution of `-1` (`Puzzle was not solved`). Tkinter is part of the standard library, but some Linux distributions ship it as a separate package (for example `python3-tk`). `tests/solutions/` is ignored by git.

## Running the benchmark

The [benchmark](benchmark.md) runs every algorithm configuration on 40 generated boards (Linux only):

```bash
python3 -m benchmark --check
```

## Next steps

- All options: [CLI reference](cli-reference.md)
- How the solver works: [Architecture](architecture.md)
- The empirical study: [Benchmark](benchmark.md)
