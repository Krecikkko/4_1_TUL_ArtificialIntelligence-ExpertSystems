import argparse

from algorithms import Algorithm, Bfs

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

    puzzle = []

    for _ in range(rows):
        row = list(map(int, input().split()))
        puzzle.append(row)

    return rows, cols, puzzle


def main():
    args = parse_arguments()

    R, C, board = read_puzzle()

    for i in range(R):
            print(str(board[i][0]) + " " + str(board[i][1]))


    if args.bfs is not None:
        print("Algorithm: BFS")
        print("Order:", args.bfs)
        Bfs.solve(args.bfs, R, C, board)

    elif args.dfs is not None:
        print("Algorithm: DFS")
        print("Order:", args.dfs)

    elif args.idfs is not None:
        print("Algorithm: IDFS")
        print("Order:", args.idfs)

    elif args.bf is not None:
        print("Algorithm: Best-first")
        print("Heuristic:", args.bf)

    elif args.astar is not None:
        print("Algorithm: A*")
        print("Heuristic:", args.astar)

    elif args.sma is not None:
        print("Algorithm: SMA*")
        print("Heuristic:", args.sma)


if __name__ == '__main__':
    main()