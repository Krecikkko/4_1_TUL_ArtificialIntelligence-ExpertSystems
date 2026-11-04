from abc import ABC, abstractmethod

class Algorithm(ABC):

    @abstractmethod
    def solve(self) -> str:
        pass