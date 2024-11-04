
from dataclasses import dataclass, field

INDENT_WIDTH = 4


@dataclass
class ProgramLine:
    line: str
    indent: int

    def __str__(self) -> str:
        return f'{" " * INDENT_WIDTH * self.indent}{self.line}'


@dataclass
class ProgramFunction:
    unified_name: str
    body: list[ProgramLine]
    header: ProgramLine
    func_calls: list[str] = field(default_factory=lambda: [])  # list of unified names

    def __str__(self) -> str:
        body = '\n'.join([str(line) for line in self.body])
        return f'{str(self.header)}\n{body}'

