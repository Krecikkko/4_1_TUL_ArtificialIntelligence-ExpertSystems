# Benchmark

The [`benchmark/`](../benchmark/) package runs the empirical comparison that the assignment requires. It runs every algorithm configuration on a fixed set of boards, under the same time and memory limits, and writes one CSV row per run.

## Layout

| Path | Content |
|---|---|
| `benchmark/run.py` | The benchmark runner (`python3 -m benchmark`) |
| `benchmark/__main__.py` | Makes `python3 -m benchmark` call `run.main()` |
| `benchmark/generate_boards.py` | Generates the board set in `benchmark/boards/` |
| `benchmark/boards/` | 40 boards (`scramble_<length>_<n>.txt`) and `boards.csv` with their metadata |
| `benchmark/boards_pilot/` | 4 boards from the pilot study. The current scripts do not use them |
| `benchmark/results/` | Result CSV files (see [Result files](#result-files)) |
| `benchmark/fifteen_puzzle_instruction.txt` | The assignment text |

## Requirements

- **Linux.** Each run sets a memory limit with `resource.setrlimit(RLIMIT_AS, ...)`, which is not available on Windows.
- Run the commands from the **repository root**, because the runner imports `puzzle` and starts `main.py` from there.

## Running

```bash
python3 -m benchmark --check   # 1 board, 1 trial (18 runs)  -> benchmark/results/full_check.csv
python3 -m benchmark           # full study (2160 runs)      -> benchmark/results/full_results.csv
```

Progress is printed to standard output, one line per run:

```text
[5/18] scramble_4_1 dfs DLUR trial=1 memory_limit length=None
```

The runner **refuses to overwrite** an existing result file. It stops with an error such as `full_results.csv already exists. Rename it before rerunning.` Rename or move the old file first.

## Study design

| Setting | Value |
|---|---|
| Boards | 40 boards of size 4×4: scramble lengths 4, 8, 12 and 20, 10 boards each |
| Uninformed configurations | BFS, DFS, IDFS × move orders `LURD`, `DLUR`, `RLUD` |
| Informed configurations | Best-first, A\*, SMA\* × heuristics `zero`, `misplaced`, `manhattan` |
| Trials | 3 per board and configuration |
| Total runs | 40 × 18 × 3 = 2160 |
| Time limit | 5 s per run (`TIMEOUT_SECONDS`) |
| Memory limit | 512 MiB address space per run (`MEMORY_MIB`) |
| Random seeds | `RLUD` runs use the search seeds 42, 43 and 44, one per trial. Other runs are not seeded |

The constants are at the top of [`benchmark/run.py`](../benchmark/run.py).

### How a run works

1. The runner starts a **new Python process** for every run. The process gets a small bootstrap script (`CHILD_CODE`) that sets the memory limit, seeds `random` if needed, and calls `main.main()`. A `MemoryError` makes it exit with code 73.
2. The board is passed on standard input, exactly as when you run `main.py` by hand.
3. The runner measures the wall-clock time of the process (`elapsed_ms`). It also reads the solver's own search time from the `Execution time:` log line on standard error (`search_ms`).
4. The solution on standard output is **replayed** on the board with `Puzzle.get_successors`. A run counts as `solved` only if every move is legal and the final state is the goal.

## Result files

All result files are in `benchmark/results/`.

| File | Content |
|---|---|
| `full_results.csv` | The full study (2160 rows) |
| `full_check.csv` | Output of `--check` |
| `pilot_results.csv` | An earlier pilot run on the sample puzzles. Its columns are a subset of the ones below |
| `results.csv` | The first trial run on the sample puzzles. Its columns are a subset of the ones below |

Columns of `full_results.csv` and `full_check.csv`:

| Column | Meaning |
|---|---|
| `board_id` | Board file name without `.txt` |
| `scramble_length`, `board_seed` | From `boards.csv` |
| `algorithm` | `bfs`, `dfs`, `idfs`, `best_first`, `astar` or `sma` |
| `move_order` | For uninformed algorithms, otherwise empty |
| `heuristic` | For informed algorithms, otherwise empty |
| `trial` | 1–3 |
| `search_seed` | Seed for `RLUD` runs, otherwise empty |
| `status` | See below |
| `elapsed_ms` | Wall-clock time of the whole process, including Python start-up |
| `search_ms` | Search time reported by `@measure_execution`, if the run got that far |
| `solution_length` | Number of moves, for `solved` runs |
| `timeout_seconds`, `address_space_limit_mib` | The limits used |

| Status | Meaning |
|---|---|
| `solved` | A valid solution was returned and verified |
| `timeout` | The run took longer than the time limit |
| `memory_limit` | The run hit the memory limit |
| `execution_error` | The process exited with another non-zero code; its stderr is printed |
| `no_solution_returned` | The solver printed `-1` |
| `invalid_output` | The output did not have the expected two-line format |
| `invalid_solution` | The moves are illegal or do not reach the goal |

## Generating boards

```bash
python3 -m benchmark.generate_boards
```

The generator starts from the goal and makes random legal moves, never undoing the previous move. It makes 4, 8, 12 and 20 moves for 10 boards each. Seeds start at 100 and increase by one for every attempt. A board is rejected if it equals the goal, the sample `tests/examples/puzzle1.txt`, or an earlier board. The board files and `boards.csv` are **overwritten**. The output is deterministic, so rerunning it reproduces the committed boards.

A scramble of length $k$ guarantees that a solution of at most $k$ moves exists. The optimal solution can be shorter.

## Summary of `full_results.csv`

Solved runs out of 90 per scramble length (all configurations and trials of an algorithm combined), with the mean solution length of the solved runs:

| Algorithm | Length 4 | Length 8 | Length 12 | Length 20 | Optimal solutions |
|---|---|---|---|---|---|
| BFS | 90 (4.0) | 90 (8.0) | 90 (11.0) | 63 (14.6) | 333 / 333 |
| DFS | 30 (2062.4) | 21 (1420.0) | 11 (51.1) | 0 | 14 / 62 |
| IDFS | 90 (4.0) | 90 (8.0) | 90 (11.0) | 54 (14.0) | 324 / 324 |
| Best-first | 90 (4.0) | 90 (9.0) | 90 (21.2) | 78 (29.4) | 279 / 348 |
| A\* | 90 (4.0) | 90 (8.0) | 90 (11.0) | 78 (15.7) | 348 / 348 |
| SMA\* | 90 (4.0) | 90 (8.0) | 90 (11.0) | 72 (15.7) | 342 / 342 |

"Optimal solutions" compares each solved run with the shortest solution that BFS or A\* found for the same board. The mean lengths at scramble length 20 are not directly comparable between algorithms, because each algorithm solved a different subset of boards.

Failure causes:

| Algorithm | `memory_limit` | `timeout` |
|---|---|---|
| BFS | 27 | 0 |
| DFS | 297 | 1 |
| IDFS | 0 | 36 |
| Best-first | 11 | 1 |
| A\* | 12 | 0 |
| SMA\* | 0 | 18 |
