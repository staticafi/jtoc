from abc import ABC, abstractmethod


class ProgramPass(ABC):
    @abstractmethod
    def do_the_pass(self) -> None:
        pass
