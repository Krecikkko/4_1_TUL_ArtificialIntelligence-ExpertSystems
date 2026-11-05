import argparse

from algorithms import Bfs, AStar
from algorithms.algorithm import configure_logging
from heuristics.factory import create_heuristic
from puzzle import Puzzle

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="15-Puzzle Solver",
        add_help=False
    )

    parser.add_argument(
        "--help",
        action="help",
        help="Show this help message and exit"
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

    algorithms.add_argument(
        "-h", "--bf",
        metavar="HEURISTIC",
        help="Best-first search heuristic"
    )

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

    puzzle = Puzzle(rows, cols, board)

    if args.bfs is not None:
        algorithm = Bfs()
        solution = algorithm.solve(
            puzzle, args.bfs
        )
    # elif args.bf is not None:
    #     heuristic = create_heuristic(args.bf)
    #     algorithm = BestFirst(heuristic)
    #     solution = algorithm.solve(puzzle)
    elif args.astar is not None:
        heuristic = create_heuristic(args.astar)
        algorithm = AStar(heuristic)
        solution = algorithm.solve(puzzle)
    # elif args.sma is not None:
    #     heuristic = create_heuristic(args.sma)
    #     algorithm = SMAStar(heuristic)
    #     solution = algorithm.solve(puzzle)
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