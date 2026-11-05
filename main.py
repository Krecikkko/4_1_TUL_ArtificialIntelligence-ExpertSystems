import argparse

from algorithms import Bfs
from algorithms.algorithm import configure_logging

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="15-Puzzle Solver"
    )
    
    algorithms = parser.add_mutually_exclusive_group(required=True)

    algorithms.add_argument(
        "-b", "--bfs",
        metavar="ORDER",
        help="Breadth-first search (e.g. LURD)"
    )

    algorithms.add_argument(
        "-d", "--dfs",
        metavar="ORDER",
        help="Depth-first search (e.g. LURD)"
    )

    algorithms.add_argument(
        "-i", "--idfs",
        metavar="ORDER",
        help="Iterative deepening DFS (e.g. LURD)"
    )

    # algorithms.add_argument(
    #     "-h", "--bf",
    #     metavar="HEURISTIC",
    #     help="Best-first search heuristic"
    # )

    algorithms.add_argument(
        "-a", "--astar",
        metavar="HEURISTIC",
        help="A* search heuristic"
    )

    algorithms.add_argument(
        "-s", "--sma",
        metavar="HEURISTIC",
        help="SMA* search heuristic"
    )

    return parser.parse_args()


def read_puzzle():
    rows, cols = map(int, input().split())

    board = []

    for _ in range(rows):
        row = list(map(int, input().split()))
        board.append(row)

    return rows, cols, board


def main():
    configure_logging()

    args = parse_arguments()

    rows, cols, board = read_puzzle()

    if args.bfs is not None:
        algorithm = Bfs()
        solution = algorithm.solve(
            args.bfs, rows, cols, board
        )
    else:
        raise NotImplementedError(
            "Selected algorithm is not implemented yet"
        )

    if solution is None:
        print(-1)
        print()
    else:
        print(len(solution))
        print(solution)


if __name__ == '__main__':
    main()