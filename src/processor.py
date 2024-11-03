import re

from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

from logger import logger
from structs.assign import Assign
from structs.call import Call
from structs.decl import Decl
from structs.function import GotoFunction
from structs.goto import Goto
from structs.instruction import Instruction
from structs.irep import Irep, Type
from structs.meta import GotoInstruction
from structs.symbol_table import SymbolTable


INDENT_WIDTH = 4


UNARY_OPERATORS = {
    'unary-': '-',
    'not': '!',
}

OPERATORS = {
    'shr': '>>',
    'ashr': '>>',
    'lshr': '>>',
    'shl': '<<',
    'bitand': '&',
    'bitor': '|',
    'bitxor': '^',
    '+': '+',
    '-': '-',
    '*': '*',
    '/': '/',
    'mod': '%',
    'notequal': '!=',
    '=': '==',
    '>': '>',
    '>=': '>=',
    '<': '<',
    '<=': '<='
}


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


class LineProcessor:
    @staticmethod
    def unify_symbol_name(symbol: str) -> str:
        var_name = symbol.split("::")[-1]
        if var_name.startswith('arg'):
            return var_name
        if var_name[0] in '0123456789':
            return f'local_{var_name}'
        return var_name
    
    @staticmethod
    def unify_label(label_num: int) -> ProgramLine:
        return f'label{label_num}'

    @staticmethod
    def unify_func_name(func_name: str) -> str:
        match = re.search(r"(\w*)::(\w*\.)*([^:()]*){1}:?.*", func_name)
        if not match:
            logger.warning(f'[unify_func] name of function {func_name} does not confirm to regex')
            return func_name

        if 'clinit' in match.group(3):
            return f'{match.group(2)}_{match.group(3)}'
        return match.group(3)

    @staticmethod
    def handle_printf(instr: Call) -> ProgramLine:
        arg_type = instr.arguments[1].named_sub.type._type
        formatting_str = '%d\\n'
        
        if arg_type == 'unsigned short int':
            formatting_str = '%lc\\n'

        args = LineProcessor.stringify(instr.arguments[1])
        return ProgramLine(line=f'printf("{formatting_str}", {args});', indent=1)

    @staticmethod
    def stringify(irep: Irep) -> str:
        if irep.id == 'constant':
            if irep.named_sub.type._type == 'const char *':
                return f'"{irep.named_sub.value.id}"'
            if irep.named_sub.type._type == 'bool':
                return str(irep.named_sub.value.id)
            if irep.named_sub.type._type == 'signed char':
                value = int(irep.named_sub.value.id, 16)
                sign = int(value & 0x80 == 0x80)
                return str((sign * -0x80) + (value & 0x7f))
            return str(int(irep.named_sub.value.id, 16))

        if irep.id == 'symbol':
            return LineProcessor.unify_symbol_name(irep.named_sub.identifier.id)

        if irep.id == 'typecast':
            return f'({irep.named_sub.type}) ({LineProcessor.stringify(irep.sub[0])})'

        if irep.id in OPERATORS:
            left, right = LineProcessor.stringify(irep.sub[0]), LineProcessor.stringify(irep.sub[1])
            return f'({left}) {OPERATORS[irep.id]} ({right})'

        if irep.id in UNARY_OPERATORS:
            return f'{UNARY_OPERATORS[irep.id]} ({LineProcessor.stringify(irep.sub[0])})'

        if irep.id == 'struct_tag':
            return f'struct {LineProcessor.unify_symbol_name(irep.named_sub.identifier.id)}'
        
        if irep.id == 'pointer':
            return f'{LineProcessor.stringify(irep.sub[0])} *'
        
        if irep.id == 'dereference':
            return f'*{LineProcessor.stringify(irep.sub[0])}'
        
        if irep.id == 'address_of':
            return f'&({LineProcessor.stringify(irep.sub[0])})'

        if irep.id == 'side_effect':
            if irep.named_sub.statement.id == 'allocate':
                return f'malloc({LineProcessor.stringify(irep.sub[0])})'

        if irep.id == 'struct':
            fields: list[str] = []
            for sub in irep.sub:
                fields.append(LineProcessor.stringify(sub))

            return f'{{ {", ".join(fields)} }}'

        if irep.id == 'member':
            pass
        else:
            logger.warning(f'[stringify] unexpected irep type: {irep.id}')
        return "DON'T KNOW YET"

    @staticmethod
    def get_line(instr: GotoInstruction) -> list[ProgramLine]:
        if instr.instruction == Instruction.DECL:
            assert isinstance(instr, Decl)
            var_name = LineProcessor.unify_symbol_name(instr.name)
            return [ProgramLine(line = f'{instr.var_type} {var_name};', indent=1)]

        if instr.instruction == Instruction.GOTO:
            assert isinstance(instr, Goto)
            label = LineProcessor.unify_label(instr.target_to)
            
            if not instr.is_guarded():
                return [ProgramLine(line=f'goto {label};', indent=1)]

            guard = LineProcessor.stringify(instr.guard)
            return [
                ProgramLine(line=f'if ({guard})', indent=1), 
                ProgramLine(line=f'goto {label};', indent=2)
            ]
        
        if instr.instruction == Instruction.ASSIGN:
            assert isinstance(instr, Assign)

            right = LineProcessor.stringify(instr.right)
            if instr.is_return():
                return [ProgramLine(line=f'return {right};', indent=1)]
            
            left = LineProcessor.unify_symbol_name(instr.get_left_name())
            if instr.left.id == 'dereference':
                left = f'*{left}'

            return [ProgramLine(line=f'{left} = {right};', indent=1)]

        if instr.instruction == Instruction.FUNCTION_CALL:
            assert isinstance(instr, Call)

            if instr.is_system_clinit_wrapper():
                return []
            if instr.is_printf():
                return [LineProcessor.handle_printf(instr)]

            func_name = LineProcessor.unify_func_name(instr.func_info.name)
            args = ', '.join([LineProcessor.stringify(irep) for irep in instr.arguments])
            return [ProgramLine(line=f'{func_name}({args});', indent=1)]

        return []


class ProgramProcessor:
    def __init__(self, symbols: SymbolTable) -> None:
        self.symbols = symbols
        self.functions: dict[str, ProgramFunction] = {}
        self.classes: dict[str, ProgramFunction] = {}

    def translate_body(self, func: GotoFunction) -> list[ProgramLine]:
        logger.info(f'translating body of function {func.name}')
        lines: list[ProgramLine] = [ProgramLine(line='{', indent=0)]

        for instr in func.instructions:
            if instr.label:
                label_line = f'{LineProcessor.unify_label(instr.label)}:'
                lines.append(ProgramLine(line=label_line, indent=0))

            for line in LineProcessor.get_line(instr):
                lines.append(line)

        if 'main' in func.name:
            lines.append(ProgramLine(line='return 0;', indent=1))
        lines.append(ProgramLine(line='}', indent=0))
        return lines

    def translate_header(self, func: GotoFunction, name: str) -> ProgramLine:
        return_type = func.get_return_type()
        
        arg_list: list[str] = []
        for arg_id in func.signature:
            arg_type = self.symbols.get_symbol_type(arg_id)
            arg_name = LineProcessor.unify_symbol_name(arg_id)

            arg_list.append(f'{arg_type} {arg_name}')
        
        if name == 'main':
            return ProgramLine('int main(int agrc, char **argv)', indent=0)

        return ProgramLine(f'{return_type} {name}({", ".join(arg_list)})', indent=0)

    def translate(self, func: GotoFunction) -> ProgramFunction:
        logger.info(f'translating function {func.name}')
        body = self.translate_body(func)
        name = LineProcessor.unify_func_name(func.name)
        header = self.translate_header(func, name)
        return ProgramFunction(unified_name=name, body=body, header=header)

    def process(self, functions: list[GotoFunction]) -> None:
        translated: dict[str, ProgramFunction] = {}
        for f in functions:
            if f.is_internal:
                continue

            program_func = self.translate(f)  # translate instructions in functions into lines
            translated[program_func.unified_name] = program_func

        self.functions = translated

        structs: dict[str, ProgramFunction] = {}
        for c in self.symbols.get_classes():
            components = c['type']['namedSub']['components']['sub']
            lines: list[ProgramLine] = [ProgramLine(line='{', indent=0)]

            for component in components:
                component_type = Type(component['namedSub']['type'])
                component_name = LineProcessor.unify_symbol_name(component["namedSub"]["name"]["id"])
                line = f'{component_type._type} {component_name}'
                lines.append(ProgramLine(line, indent=1))

            name = c['name']
            header = f'struct {LineProcessor.unify_symbol_name(name)}'
            lines.append(ProgramLine(line='}', indent=0))
            structs[name] = ProgramFunction(name, lines, header)

        self.classes = structs


    def write_to_stdout(self) -> str:
        print('#include <stdio.h>\n')

        for struct in self.classes.values():
            print(str(struct.header), ';', sep='')

        print('\n')
        for struct in self.classes.values():
            print(str(struct))
            print('\n')

        for function in self.functions.values():
            if function.unified_name == 'main':
                continue

            print(str(function.header), ';', sep='')
    
        print('\n')

        for function in self.functions.values():
            print(str(function))
            print('\n')

    def write_to_file(self, file: Path) -> None:
        with open(file, 'w') as file:
            print('#include <stdio.h>', file=file)
            print('#include <stdbool.h>\n', file=file)
            if 'main' in self.functions:
                print(self.functions['main'], file=file)
            print('\n', file=file)
