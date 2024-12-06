from __future__ import annotations
from dataclasses import dataclass

from processing.expressions.expressions import Expression
from processing.program_parts.lines import DeclLine, HeaderLine, ProgramLine


@dataclass
class ProgramFunction:
    header: HeaderLine
    body: list[ProgramLine]

    def __str__(self) -> str:
        body = '\n'.join([str(line) for line in self.body])
        return f'{str(self.header)}\n{{\n{body}\n}}'


@dataclass
class ProgramStruct:
    unified_name: str
    body: list[DeclLine]

    def __str__(self) -> str:
        lines = [
            f'struct {self.unified_name} {{',
            *[str(decl) for decl in self.body],
            '};'
        ]

        return '\n'.join(lines)

    @property
    def header(self) -> str:
        return f'struct {self.unified_name};'


@dataclass
class ProgramStaticVar:
    unified_name: str
    var_type: str
    array_width: int | None
    assigned_value: Expression

    def __str__(self) -> str:
        if self.array_width:
            if self.var_type in {'char', 'unsigned short int'}:
                items = str(self.assigned_value)
                return f'{self.var_type} {self.unified_name}[{self.array_width + 1}] = {items};'
            return f'{self.var_type} {self.unified_name}[{self.array_width}] = {str(self.assigned_value)};'
        return f'{self.var_type} {self.unified_name} = {str(self.assigned_value)};'