# Demo commands

Copy-paste commands for showing the project. Run them from the project root.
The execution time of each run is printed in the `[INFO]` log line.

Example puzzles:

| File | Description | Optimal solution |
|---|---|---|
| `tests/examples/puzzle1.txt` | Very easy | 2 moves (`UL`) |
| `tests/examples/puzzle3.txt` | Medium, all algorithms finish quickly | 8 moves (`RRULDLUL`) |
| `tests/examples/puzzle2.txt` | Hard, only Best-first solves it in reasonable time | — |

Heuristics (for Best-first, A* and SMA*): `zero`, `misplaced`, `manhattan`.

## 0. Preparation

```bash
mkdir -p tests/solutions
```

```bash
python main.py --help
```

## 1. BFS (Breadth-first search)

Finds the shortest solution.

```bash
python main.py --bfs LURD < tests/examples/puzzle3.txt
```

Different movement order:

```bash
python main.py --bfs DULR < tests/examples/puzzle3.txt
```

Random movement order (order starting with `R`):

```bash
python main.py --bfs RLUD < tests/examples/puzzle3.txt
```

## 2. DFS (Depth-first search)

Finds *a* solution, usually much longer than the shortest one (here 782 moves instead of 8).

```bash
python main.py --dfs LURD < tests/examples/puzzle3.txt
```

```bash
python main.py --dfs LURD < tests/examples/puzzle1.txt
```

## 3. IDFS (Iterative deepening DFS)

Finds the shortest solution, like BFS.

```bash
python main.py --idfs LURD < tests/examples/puzzle3.txt
```

## 4. Best-first search

Fast, but the solution is not guaranteed to be the shortest.

```bash
python main.py --bf manhattan < tests/examples/puzzle3.txt
```

```bash
python main.py --bf misplaced < tests/examples/puzzle3.txt
```

The hard puzzle, which the other algorithms don't solve in reasonable time:

```bash
python main.py --bf manhattan < tests/examples/puzzle2.txt
```

## 5. A* (A-star)

Finds the shortest solution. Compare the execution times of the heuristics.

```bash
python main.py --astar manhattan < tests/examples/puzzle3.txt
```

```bash
python main.py --astar misplaced < tests/examples/puzzle3.txt
```

```bash
python main.py --astar zero < tests/examples/puzzle3.txt
```

## 6. SMA* (Simplified memory-bounded A*)

```bash
python main.py --sma manhattan < tests/examples/puzzle3.txt
```

```bash
python main.py --sma misplaced < tests/examples/puzzle3.txt
```

```bash
python main.py --sma zero < tests/examples/puzzle3.txt
```

## 7. Save the solution and show it in the viewer

Solve, print to terminal and save to file:

```bash
python main.py --astar manhattan < tests/examples/puzzle3.txt | tee tests/solutions/solution.txt
```

Open the viewer with the puzzle and the saved solution:

```bash
python -m viewer.app tests/examples/puzzle3.txt tests/solutions/solution.txt
```

Long DFS solution in the viewer:

```bash
python main.py --dfs LURD < tests/examples/puzzle1.txt | tee tests/solutions/solution.txt
python -m viewer.app tests/examples/puzzle1.txt tests/solutions/solution.txt
```

Best-first solution of the hard puzzle in the viewer:

```bash
python main.py --bf manhattan < tests/examples/puzzle2.txt | tee tests/solutions/solution.txt
python -m viewer.app tests/examples/puzzle2.txt tests/solutions/solution.txt
```

Save only to file (no terminal output):

```bash
python main.py --bfs LURD < tests/examples/puzzle3.txt > tests/solutions/solution.txt
```
