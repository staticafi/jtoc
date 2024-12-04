from __future__ import annotations
from dataclasses import dataclass

from static import INDENT_WIDTH
from processing.expressions import Expression
from structs.type import Type


@dataclass
class ProgramLine:
    indent: int

    def get_indent(self, indent: int | None=None) -> str:
        if not indent:
            return " " * INDENT_WIDTH * self.indent
    
        return " " * INDENT_WIDTH * indent


@dataclass
class DeclLine(ProgramLine):
    var_type: str
    var_name: str
    array_width: int | None

    def __str__(self) -> str:
        indent = self.get_indent()
        if self.array_width:
            return f'{indent}{self.var_type} {self.var_name}[{self.array_width}];'
        
        return f'{indent}{self.var_type} {self.var_name};'


@dataclass
class AssignLine(ProgramLine):
    lhs: Expression
    rhs: Expression

    def __str__(self) -> str:
        indent = self.get_indent()
        left = str(self.lhs)
        right = str(self.rhs)

        if left.endswith('return_value'):
            return f'{indent}{left} = {right};\n{indent}return {right};'

        return f'{indent}{left} = {right};'


@dataclass
class GotoLine(ProgramLine):
    guard: Expression | None
    goto_label: str

    def __str__(self) -> str:
        indent = self.get_indent()
        if not self.guard:
            return f'{indent}goto {self.goto_label};'

        return f'{indent}if ({str(self.guard)})\n{self.get_indent(self.indent + 1)}goto {self.goto_label};'


@dataclass
class FunctionCallLine(ProgramLine):
    func_name: str
    args: list[Expression]

    def __str__(self) -> str:
        indent = self.get_indent()
        args = ', '.join([str(arg) for arg in self.args])
        return f'{indent}{self.func_name}({args});'


@dataclass 
class TextLine(ProgramLine):
    text: str

    def __str__(self) -> str:
        indent = self.get_indent()
        return f'{indent}{self.text}'


@dataclass
class InputArgument:
    arg_type: str
    arg_name: str

    def __str__(self) -> str:
        return f'{self.arg_type} {self.arg_name}'


@dataclass
class HeaderLine:
    return_type: str
    unified_name: str
    args: list[InputArgument]

    @staticmethod
    def main_function_header() -> HeaderLine:
        args = [
            InputArgument(arg_type='int', arg_name='argc'),
            InputArgument(arg_type='char **', arg_name='argv')
        ]
        return HeaderLine(return_type='int', unified_name='main', args=args)

    def __str__(self) -> str:
        arguments = ", ".join([str(arg) for arg in self.args])
        return f'{self.return_type} {self.unified_name}({arguments})'


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