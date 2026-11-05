from .heuristic import Heuristic
from .zero import Zero
from .misplaced_tiles import MisplacedTiles
from .manhattan import Manhattan


def create_heuristic(heuristic_id: str) -> Heuristic:

    heuristics = {
        "zero": Zero,
        "misplaced": MisplacedTiles,
        "manhattan": Manhattan
    }

    heuristic_class = heuristics.get(heuristic_id.lower())

    if heuristic_class is None:
        raise ValueError(
            f"Unknown heuristic: {heuristic_id}"
        )

    return heuristic_class()
