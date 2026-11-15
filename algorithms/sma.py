"""Simplified memory-bounded A* for the sliding-tile puzzle."""

from dataclasses import dataclass, field
from itertools import count
from math import inf

from heuristics import Heuristic
from puzzle import Puzzle

from .algorithm import Algorithm, measure_execution

DEFAULT_MEMORY_LIMIT = 10_000
_State = tuple[int, ...]
_Priority = tuple[float, int, int]


@dataclass(slots=True, eq=False)
class _Branch:
    # A forgotten branch retains its score, but not its board or descendants.
    score: float
    child: "_Node | None" = None
    forgotten: bool = False


@dataclass(slots=True, eq=False)
class _Node:
    state: _State
    depth: int
    serial: int
    floor: float
    parent: "_Node | None" = None
    move: str = ""
    branches: dict[str, _Branch] | None = None
    best: _Priority = field(init=False)
    worst: _Priority = field(init=False)

    def refresh(self) -> None:
        """Summarize the best search action and worst removable leaf."""
        if self.branches is None:
            self.best = (self.floor, -self.depth, -self.serial)
            self.worst = self.best
            return

        # Equal scores favor deeper, newer nodes for expansion, and
        # shallower, older leaves for eviction.
        self.best = (inf, -self.depth, -self.serial)
        worst_child = None
        for branch in self.branches.values():
            if branch.child is None:
                candidate = (branch.score, -self.depth, -self.serial)
            else:
                candidate = branch.child.best
                worst = branch.child.worst
                worst_child = worst if worst_child is None else max(worst_child, worst)
            self.best = min(self.best, candidate)
        self.worst = self.best if worst_child is None else worst_child


class SMAStar(Algorithm):
    """Retain at most memory_limit search nodes, including the root."""

    def __init__(
        self, heuristic: Heuristic, memory_limit: int = DEFAULT_MEMORY_LIMIT
    ) -> None:
        if memory_limit < 1:
            raise ValueError("SMAStar* memory limit must be at least one node")
        self.heuristic = heuristic
        self.memory_limit = memory_limit
        self.peak_nodes = 0
        self.evictions = 0
        self.regenerations = 0

    @measure_execution
    def solve(self, puzzle: Puzzle, parameter: str = "") -> str | None:
        # The CLI gives SMAStar* a heuristic ID, not a movement order.
        self.peak_nodes = self.evictions = self.regenerations = 0
        if not self._is_solvable(puzzle):
            return None

        numbers = count()
        root = _Node(puzzle.initial_state, 0, next(numbers), 0)
        root.floor = self._estimate(puzzle, root.state, root.depth, 0)
        root.refresh()
        resident = {root.serial: root}
        self.peak_nodes = 1

        while root.best[0] != inf:
            node = resident[-root.best[2]]
            if puzzle.is_goal(node.state):
                return self._solution(node)

            if node.branches is None:
                # Exclude only ancestors. A global visited map would grow
                # beyond the memory budget and can hide usable paths.
                ancestors = set()
                ancestor = node
                while ancestor is not None:
                    ancestors.add(ancestor.state)
                    ancestor = ancestor.parent

                node.branches = {
                    move: _Branch(self._estimate(puzzle, state, node.depth + 1, node.floor))
                    for move, state in puzzle.get_successors(node.state)
                    if state not in ancestors
                }
                del ancestors
                self._backup(node)
                continue

            move, branch = min(
                ((move, branch) for move, branch in node.branches.items()
                 if branch.child is None),
                key=lambda item: item[1].score,
            )
            if len(resident) == self.memory_limit:
                victim = self._worst_other_leaf(root, node, resident)
                self._forget(victim, resident)
                del victim
                self.evictions += 1

            # Re-create the board on demand. A move uniquely identifies a
            # successor of this board.
            state = next(
                state for action, state in puzzle.get_successors(node.state)
                if action == move
            )
            child = _Node(state, node.depth + 1, next(numbers), branch.score, node, move)
            child.refresh()
            if branch.forgotten:
                self.regenerations += 1
            branch.child = child
            resident[child.serial] = child
            self.peak_nodes = max(self.peak_nodes, len(resident))
            self._backup(node)

        return None

    def _estimate(self, puzzle: Puzzle, state: _State, depth: int, floor: float) -> float:
        if puzzle.is_goal(state):
            return max(floor, depth)
        # A non-goal on the deepest storable level cannot be expanded.
        if depth >= self.memory_limit - 1:
            return inf
        score = max(floor, depth + self.heuristic.calculate(state, puzzle))
        # All built-in heuristics are admissible. Paths needing more nodes
        # than the budget cannot end at a storable goal.
        return score if score < self.memory_limit else inf

    @staticmethod
    def _backup(node: _Node) -> None:
        while node is not None:
            node.refresh()
            node = node.parent

    @staticmethod
    def _worst_other_leaf(
        root: _Node, node: _Node, resident: dict[int, _Node]
    ) -> _Node:
        worst = root.worst
        if -worst[2] == node.serial:
            # Keep the parent of the child we're about to add. Find the
            # worst leaf in a sibling subtree along its path back to root.
            alternatives = []
            child = node
            while child.parent is not None:
                parent = child.parent
                alternatives.extend(
                    branch.child.worst for branch in parent.branches.values()
                    if branch.child is not None and branch.child is not child
                )
                child = parent
            # A resident tree that is only this path would already be at
            # the depth limit and could not request another child.
            worst = max(alternatives)
        return resident[-worst[2]]

    @classmethod
    def _forget(cls, node: _Node, resident: dict[int, _Node]) -> None:
        parent = node.parent
        branch = parent.branches[node.move]
        branch.score = node.best[0]
        branch.forgotten = True
        branch.child = None
        del resident[node.serial]
        cls._backup(parent)

    @staticmethod
    def _solution(node: _Node) -> str:
        moves = []
        while node.parent is not None:
            moves.append(node.move)
            node = node.parent
        return "".join(reversed(moves))

    @staticmethod
    def _is_solvable(puzzle: Puzzle) -> bool:
        """Check reachability for the project's standard ordered goal."""
        tiles = [tile for tile in puzzle.initial_state if tile]
        if puzzle.rows == 1 or puzzle.cols == 1:
            return tiles == sorted(tiles)
        inversions = sum(
            tile > other for index, tile in enumerate(tiles) for other in tiles[index + 1:]
        )
        if puzzle.cols % 2:
            return inversions % 2 == 0
        blank_row_from_bottom = puzzle.rows - puzzle.initial_state.index(0) // puzzle.cols
        return (inversions + blank_row_from_bottom) % 2 == 1
