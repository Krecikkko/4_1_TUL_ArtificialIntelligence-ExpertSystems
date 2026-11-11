# List of exemplary commands

## Run puzzle solver

### Get input from file, display output in bash and save to file

```bash
python main.py --bfs LURD < tests/examples/puzzle1.txt | tee tests/solutions/solution.txt
```

### Get input from file and save to file

```bash
python main.py --bfs LURD < tests/examples/puzzle1.txt > tests/solutions/solution.txt
```

## Run viewer

```bash
python -m viewer.app tests/examples/puzzle1.txt tests/solutions/solution.txt
```