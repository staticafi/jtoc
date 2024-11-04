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
    @staticmethod
    def unify_symbol_name(symbol: str) -> str:
        var_name = symbol.split("::")[-1]
        if var_name.startswith('arg'):
            return var_name
        if var_name[0] in '0123456789':
            return f'local_{var_name}'
        if '.' in var_name:
            return var_name.replace('.', '_')
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
            return f'*({LineProcessor.stringify(irep.sub[0])})'
        
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
            return f'{LineProcessor.stringify(irep.sub[0])}.{irep.named_sub.component_name.id}'
        
        
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
