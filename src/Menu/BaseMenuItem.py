from abc import ABC, abstractmethod

from src import Handler


class AbstractMenuItem(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class BaseMenuItem(AbstractMenuItem):

    name: str = None

    def __init__(self, handler: Handler) -> None:
        self.handler = handler

    def execute(self) -> None:
        pass

    def __str__(self) -> str:
        return self.name
