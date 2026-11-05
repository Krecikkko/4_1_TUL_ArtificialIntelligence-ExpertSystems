# CLI Reference

```text
python3 main.py (-b ORDER | -d ORDER | -i ORDER | -h HEURISTIC | -a HEURISTIC | -s HEURISTIC) < input
python3 main.py --help
```

Exactly one algorithm option is required. The options form an `argparse` mutually exclusive group with `required=True`.

## Options

| Argument | Algorithm | Parameter | Status |
|---|---|---|---|
| `-b`, `--bfs` | Breadth-first search | Movement order | ✅ Functional |
| `-d`, `--dfs` | Depth-first search | Movement order | ❌ Parsed only, raises `NotImplementedError` |
| `-i`, `--idfs` | Iterative deepening DFS | Movement order | ❌ Parsed only, raises `NotImplementedError` |
| `-h`, `--bf` | Best-first search | Heuristic ID | ❌ Parsed only, raises `NotImplementedError` |
| `-a`, `--astar` | A\* | Heuristic ID | ✅ Functional |
| `-s`, `--sma` | SMA\* | Heuristic ID | ❌ Parsed only, raises `NotImplementedError` |
| `--help` | — | — | Shows usage and exits |

> **Note:** `-h` selects Best-first search, as the assignment requires. For this reason the parser is created with `add_help=False`, and help is available **only** as `--help`.

## Movement order

The movement order is a permutation of the letters `L`, `R`, `U`, `D`. It sets the order in which successors are generated, and so the order in which uninformed algorithms explore them.

| Letter | Meaning (the **numbered tile** moves…) |
|---|---|
| `L` | left, into the empty cell |
| `R` | right, into the empty cell |
| `U` | up, into the empty cell |
| `D` | down, into the empty cell |

The letters describe **tile** movement, not movement of the empty cell. See [Puzzle representation](puzzle-representation.md#movement-semantics).

Rules enforced by `Puzzle.get_successors`:

- The order must contain exactly four characters and use each of `L`, `R`, `U`, `D` once. Letters are case-sensitive. Otherwise the program raises `ValueError("Invalid movement order")`.
- If the order **starts with `R`**, the successor order is **randomized for every expanded node**. For example, `RLUD`, `RDLU` and `RUDL` all mean "random".

Consequences of these rules:

- A single `R` (for example `-b R`) is **rejected** because it is not four letters long.
- The six deterministic orders that start with `R` (such as `RDLU`) cannot be used deterministically, because they all mean "random".
- The order is validated only when the first node is expanded. If the initial state is already the goal, an invalid order is never detected.

## Heuristic identifiers

These are used by `-a` (and, once implemented, by `-h` and `-s`). Matching is case-insensitive (`heuristic_id.lower()`).

| ID | Class | Documentation |
|---|---|---|
| `zero` | `Zero` | [heuristics/zero.md](heuristics/zero.md) |
| `misplaced` | `MisplacedTiles` | [heuristics/misplaced-tiles.md](heuristics/misplaced-tiles.md) |
| `manhattan` | `Manhattan` | [heuristics/manhattan.md](heuristics/manhattan.md) |

Any other value raises `ValueError("Unknown heuristic: <id>")`.

## Input format (standard input)

```text
R C
t11 t12 ... t1C
...
tR1 tR2 ... tRC
```

- Line 1: the number of rows `R` and columns `C`, separated by whitespace.
- The next `R` lines: `C` integers each. `0` is the empty cell.
- `read_puzzle()` in `main.py` reads exactly `R + 1` lines with `input()`. Extra lines are ignored.

The input is **not validated**. Wrong row lengths, duplicate tiles or a missing `0` lead to undefined behavior or an exception later on.

## Output format (standard output)

| Situation | Line 1 | Line 2 |
|---|---|---|
| Solution found | number of moves | move sequence, e.g. `UL` |
| Initial state is the goal | `0` | empty line |
| Search space exhausted without a solution | `-1` | empty line |

Example:

```text
2
UL
```

## Standard error and logging

When `DEBUG = True` in [`algorithms/algorithm.py`](../algorithms/algorithm.py) (the default), the `measure_execution` decorator writes the following to **standard error**:

```text
[INFO] Algorithm started
[INFO] Algorithm finished | Execution time: 0.000102 s
```

Exceptions and `argparse` errors also go to standard error. Standard output contains only the solution, so it can be redirected safely:

```bash
python3 main.py -a manhattan < puzzle.txt > solution.txt 2> log.txt
```

## Examples

```bash
# BFS, fixed order
python3 main.py -b LURD < tests/examples/puzzle1.txt
python3 main.py --bfs DRUL < tests/examples/puzzle1.txt

# BFS, randomized order for each expanded node
python3 main.py -b RLUD < tests/examples/puzzle1.txt

# A* with each heuristic
python3 main.py -a manhattan < tests/examples/puzzle1.txt
python3 main.py -a misplaced < tests/examples/puzzle1.txt
python3 main.py --astar zero < tests/examples/puzzle1.txt

# Inline input through a here-document
python3 main.py -a manhattan <<'EOF'
3 3
1 2 3
4 0 6
7 5 8
EOF
```

## Behavior and error handling

| Condition | Result |
|---|---|
| No algorithm option, or two of them | `argparse` usage error on stderr, exit code 2 |
| `-d`, `-i`, `-h`, `-s` | The puzzle is read from stdin **first**, then `NotImplementedError` with a traceback |
| Unknown heuristic ID | `ValueError: Unknown heuristic: …` with a traceback |
| Invalid movement order | `ValueError: Invalid movement order` with a traceback (raised when the first node is expanded) |
| Unsolvable puzzle | No early detection. The search runs until the reachable space is exhausted, which on 4×4 boards does not finish in practice |

The program has no custom exception handling. Errors appear as standard Python tracebacks with exit code 1.
