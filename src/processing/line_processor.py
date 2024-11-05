import re

from logger import logger
from processing.data import ProgramLine
from structs.assign import Assign
from structs.call import Call
from structs.decl import Decl
from structs.goto import Goto
from structs.instruction import Instruction
from structs.irep import Irep
from structs.meta import GotoInstruction
from structs.symbol_table import SymbolTable


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


class LineProcessor:
    def __init__(self, symbols: SymbolTable) -> None:
        self.symbols = symbols

    def unify_symbol_name(self, symbol: str) -> str:
        if self.symbols.is_static_symbol(symbol):
            sections = symbol.split('::')
            symbol_name = '__'.join(sections[1:]).replace('.', '_')
            if symbol_name.startswith('@'):
                return f'___{symbol_name[1:]}___'
            
            result = re.search(r'(.*):.*#(\w*)', symbol_name)
            if result:
                new_symbol_name = f'{result.group(1)}_{result.group(2)}'
                return new_symbol_name.replace('[', '__').replace(']', '__')

            return '__'.join(sections[1:]).replace('.', '_')

        var_name = symbol.split("::")[-1].replace('[', '__').replace(']', '__')
        if symbol.startswith('@'):
            return f'___{var_name[1:].replace(".", "_")}___'
        if var_name.startswith('arg'):
            return var_name
        if var_name[0] in '0123456789':
            return f'local_{var_name}'
        return var_name.replace('.', '_')

    @staticmethod
    def unify_label(label_num: int) -> ProgramLine:
        return f'label{label_num}'

    @staticmethod
    def unify_func_name(func_name: str) -> str:
        match = re.search(r"(\w*)::((\w*)\.)*([^:()]*){1}:?.*", func_name)
        if not match:
            logger.warning(f'[unify_func] name of function {func_name} does not confirm to regex')
            return func_name

        if match.group(4) in {'<clinit>', '<clinit_wrapper>', '<init>'}:
            inside = re.search(r'<([^<>]*)>', match.group(4)).group(1)
            return f'___{match.group(3)}_{inside}___'
        return match.group(4)

    def handle_printf(self, instr: Call) -> ProgramLine:
        arg_type = instr.arguments[1].named_sub.type._type
        formatting_str = '%d\\n'
        
        if arg_type == 'unsigned short int':
            formatting_str = '%lc\\n'

        args = self.stringify(instr.arguments[1])
        return ProgramLine(line=f'printf("{formatting_str}", {args});', indent=1)

    def stringify(self, irep: Irep) -> str:
        if irep.id == 'constant':
            if irep.named_sub.type._type == 'const char *':
                return f'"{irep.named_sub.value.id}"'
            if irep.named_sub.type.is_pointer():
                return irep.named_sub.value.id
            if irep.named_sub.type._type == 'bool':
                return str(irep.named_sub.value.id)
            if irep.named_sub.type._type == 'signed char':
                value = int(irep.named_sub.value.id, 16)
                sign = int(value & 0x80 == 0x80)
                return str((sign * -0x80) + (value & 0x7f))
            return str(int(irep.named_sub.value.id, 16))

        if irep.id == 'symbol':
            return self.unify_symbol_name(irep.named_sub.identifier.id)

        if irep.id == 'typecast':
            return f'({irep.named_sub.type}) ({self.stringify(irep.sub[0])})'

        if irep.id in OPERATORS:
            left, right = self.stringify(irep.sub[0]), self.stringify(irep.sub[1])
            return f'({left}) {OPERATORS[irep.id]} ({right})'

        if irep.id in UNARY_OPERATORS:
            return f'{UNARY_OPERATORS[irep.id]} ({self.stringify(irep.sub[0])})'

        if irep.id == 'struct_tag':
            return f'struct {self.unify_symbol_name(irep.named_sub.identifier.id)}'
        
        if irep.id == 'pointer':
            return f'{self.stringify(irep.sub[0])} *'
        
        if irep.id == 'dereference':
            return f'*({self.stringify(irep.sub[0])})'
        
        if irep.id == 'address_of':
            return f'&({self.stringify(irep.sub[0])})'

        if irep.id == 'side_effect':
            if irep.named_sub.statement.id == 'allocate':
                return f'malloc({self.stringify(irep.sub[0])})'

        if irep.id == 'struct':
            fields: list[str] = []
            for sub in irep.sub:
                fields.append(self.stringify(sub))

            return f'{{ {", ".join(fields)} }}'

        if irep.id == 'member':
            member_name = self.unify_symbol_name(irep.named_sub.component_name.id)
            return f'{self.stringify(irep.sub[0])}.{member_name}'
        
        if irep.id == 'nil':
            return 'NULL'

        logger.warning(f'[stringify] unexpected irep type: {irep.id}')
        return "DON'T KNOW YET"

    def get_line(self, instr: GotoInstruction) -> list[ProgramLine]:
        if instr.instruction == Instruction.DECL:
            assert isinstance(instr, Decl)
            var_name = self.unify_symbol_name(instr.name)
            return [ProgramLine(line = f'{instr.var_type} {var_name};', indent=1)]

        if instr.instruction == Instruction.GOTO:
            assert isinstance(instr, Goto)
            label = self.unify_label(instr.target_to)
            
            if not instr.is_guarded():
                return [ProgramLine(line=f'goto {label};', indent=1)]

            guard = self.stringify(instr.guard)
            return [
                ProgramLine(line=f'if ({guard})', indent=1), 
                ProgramLine(line=f'goto {label};', indent=2)
            ]
        
        if instr.instruction == Instruction.ASSIGN:
            assert isinstance(instr, Assign)

            right = self.stringify(instr.right)
            if instr.is_return():
                return [ProgramLine(line=f'return {right};', indent=1)]
            
            left = self.unify_symbol_name(instr.get_left_name())
            if instr.left.id == 'dereference':
                left = f'*{left}'

            return [ProgramLine(line=f'{left} = {right};', indent=1)]

        if instr.instruction == Instruction.FUNCTION_CALL:
            assert isinstance(instr, Call)

            if instr.is_printf():
                return [self.handle_printf(instr)]

            func_name = self.unify_func_name(instr.func_info.name)
            args = ', '.join([self.stringify(irep) for irep in instr.arguments])
            return [ProgramLine(line=f'{func_name}({args});', indent=1)]

        return []
