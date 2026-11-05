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

The repository ships with two sample inputs in [`tests/examples/`](../tests/examples/).

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
| `puzzle1.txt` | 4×4 | Two moves from the goal (`UL`). Solves instantly with BFS and A\*. |
| `puzzle2.txt` | 4×4 | Solvable (verified with an inversion-parity check), but far from the goal. In a local check, A\* with `manhattan` did **not** finish within 60 seconds, and BFS is not practical for it. See [A\* limitations](algorithms/astar.md#75-complexity-analysis). |

## Next steps

- All options: [CLI reference](cli-reference.md)
- How the solver works: [Architecture](architecture.md)
