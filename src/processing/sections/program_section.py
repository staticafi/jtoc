from abc import ABC, abstractmethod
from typing import TextIO


class ProgramSection(ABC):
    @abstractmethod
    def write_to_file(self, write_to: TextIO | None) -> None:
        pass
