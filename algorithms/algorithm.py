import logging
import sys
import time

from abc import ABC, abstractmethod
from functools import wraps
from puzzle import Puzzle


# Change to False to disable logging
DEBUG = True


def configure_logging():
    logging.basicConfig(
        level=logging.INFO if DEBUG else logging.CRITICAL,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr
    )


def measure_execution(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logger = logging.getLogger(self.__class__.__name__)

        start_time = time.perf_counter()

        if DEBUG:
            logger.info("Algorithm started")

        try:
            return func(self, *args, **kwargs)
        finally:
            elapsed_time = time.perf_counter() - start_time

            if DEBUG:
                logger.info(
                    "Algorithm finished | Execution time: %.6f s",
                    elapsed_time
                )

    return wrapper


class Algorithm(ABC):

    @abstractmethod
    def solve(
        self,
        puzzle: Puzzle,
        parameter: str
    ) -> str | None:
        pass
