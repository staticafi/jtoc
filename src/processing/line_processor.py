from typing import Callable
from static import logger
from processing.data import AssignLine, DeclLine, FunctionCallLine, GotoLine, ProgramLine
from processing.expressions import Address, Array, Constant, Dereference, Expression, ExpressionType, Index, Member, Nil, Operator, Pointer, SideEffect, Struct, StructTag, Symbol, \
                                   Typecast, UnaryOperator, OPERATORS, UNARY_OPERATORS
from structs.assign import Assign
from structs.call import Call
from structs.decl import Decl
from structs.goto import Goto
from structs.instruction import Instruction
from structs.irep import Irep
from structs.meta import GotoInstruction
from structs.symbol_table import SymbolTable
from structs.type import Type


class LineProcessor:
    def __init__(self, symbols: SymbolTable) -> None:
        self.symbols = symbols

    def handle_printf(self, instr: Call) -> ProgramLine:
        arg_type = instr.arguments[1].named_sub.type._type
        formatting_str = '%d\\n'
        
        if arg_type == 'unsigned short int':
            formatting_str = '%lc\\n'
        if arg_type in {'double', 'float'}:
            formatting_str = '%f\\n'

        args = self.stringify(instr.arguments[1])
        return ProgramLine(line=f'printf("{formatting_str}", {args});', indent=1)

    def to_c_value(self, irep: Irep) -> str:
        assert irep.named_sub.type is not None
        if irep.named_sub.type == 'const char *':
            return f'"{irep.named_sub.value.id}"'
        if irep.named_sub.type.is_pointer():
            return irep.named_sub.value.id
        if irep.named_sub.type == 'bool':
            return str(irep.named_sub.value.id)
        if irep.named_sub.type == 'signed char':
            value = int(irep.named_sub.value.id, 16)
            sign = int(value & 0x80 == 0x80)
            return str((sign * -0x80) + (value & 0x7f))
        return str(int(irep.named_sub.value.id, 16))

    def to_expression(self, irep: Irep) -> Expression:
        if irep.id == 'comma':
            return self.to_expression(irep.sub[1])

        expr_type = ExpressionType.from_expr(irep.id)
        
        if expr_type == ExpressionType.Nil:
            return Nil.build()

        if expr_type == ExpressionType.Constant:
            value = self.to_c_value(irep)
            return Constant.build(value)

        if expr_type == ExpressionType.Symbol:
            original = irep.named_sub.identifier.id
            unified = self.symbols.unify_symbol_name(original)
            return Symbol.build(original, unified)

        if expr_type == ExpressionType.Typecast:
            typecast = self.unify_type(irep.named_sub.type)
            expr = self.to_expression(irep.sub[0])
            return Typecast.build(typecast, expr)

        if expr_type == ExpressionType.Operator:
            op = OPERATORS[irep.id]
            left = self.to_expression(irep.sub[0])
            right = self.to_expression(irep.sub[1])
            return Operator.build(op, left, right)

        if expr_type == ExpressionType.UnaryOperator:
            op = UNARY_OPERATORS[irep.id]
            value = self.to_expression(irep.sub[0])
            return UnaryOperator.build(op, value)

        if expr_type == ExpressionType.StructTag:
            original = irep.named_sub.identifier.id
            unified = self.symbols.unify_symbol_name(original)
            symbol = Symbol.build(original, unified)
            return StructTag.build(symbol)

        if expr_type == ExpressionType.Pointer:
            expr = self.to_expression(irep.sub[0])
            return Pointer.build(expr)

        if expr_type == ExpressionType.Dereference:
            expr = self.to_expression(irep.sub[0])
            return Dereference.build(expr)

        if expr_type == ExpressionType.Address:
            expr = self.to_expression(irep.sub[0])
            return Address.build(expr)

        if expr_type == ExpressionType.SideEffect:
            effect = irep.named_sub.statement.id
            args = [self.to_expression(arg) for arg in irep.sub]
            return SideEffect.build(effect, args)

        if expr_type == ExpressionType.Struct:
            original = irep.named_sub.type.raw_name
            unified = self.symbols.unify_symbol_name(original)
            symbol = Symbol.build(original, unified)
            args = [self.to_expression(sub) for sub in irep.sub]
            return Struct.build(symbol, args)

        if expr_type == ExpressionType.Member:
            original = irep.named_sub.type.raw_name
            unified = self.symbols.unify_symbol_name(original)
            member = Symbol.build(original, unified)
            obj = self.to_expression(irep.sub[0])
            return Member.build(member, obj)

        if expr_type == ExpressionType.Array:
            assert irep.named_sub.type is not None
            array_type = irep.named_sub.type
            elements = [self.to_expression(sub) for sub in irep.sub]
            return Array.build(array_type, elements)

        if expr_type == ExpressionType.Index:
            index = self.to_expression(irep.sub[1])
            obj = self.to_expression(irep.sub[0])
            return Index.build(index, obj)

        logger.warning(f'[to_expression] fall-through with expr_type {expr_type}')

    def unify_type(self, type_: Type | None) -> str:
        if not type_:
            return 'void'

        if type_.is_struct():
            unified = self.symbols.unify_symbol_name(type_.raw_name)
            return f'struct {unified}'
        
        if type_.is_array():
            return self.unify_type(type_.inside)
        
        if type_.is_pointer():
            return f'{self.unify_type(type_.inside)} *'

        return type_.to_string()

    def process_decl(self, decl: Decl) -> ProgramLine:
        var_name = self.symbols.unify_symbol_name(decl.name)
        var_type = self.unify_type(decl.var_type)
        array_width = None

        if decl.var_type.is_array():
            array_width = decl.var_type.width

        return DeclLine(indent=1, var_type=var_type, var_name=var_name, array_width=array_width)

    def process_assign(self, assign: Assign) -> ProgramLine:
        right = self.to_expression(assign.right)
        left = self.to_expression(assign.left)

        return AssignLine(indent=1, lhs=left, rhs=right)

    def process_goto(self, goto: Goto) -> ProgramLine:
        label = self.symbols.unify_label(goto.target_to)
        guard = None

        if goto.is_guarded():
            guard = self.to_expression(goto.guard)
        
        return GotoLine(indent=1, guard=guard, goto_label=label)

    def process_call(self, call: Call) -> ProgramLine:
        func_name = self.symbols.unify_func_name(call.func_info.name)
        args = ', '.join([self.to_expression(irep) for irep in call.arguments])
        
        return FunctionCallLine(indent=1, func_name=func_name, args=args)

    def get_line(self, instr: GotoInstruction) -> ProgramLine | None:
        process_functions: dict[Instruction, Callable[[GotoInstruction], ProgramLine]] = {
            Instruction.DECL: self.process_decl,
            Instruction.ASSIGN: self.process_assign,
            Instruction.GOTO: self.process_goto,
            Instruction.FUNCTION_CALL: self.process_call
        } 

        if instr.instruction not in process_functions:
            return None
        
        return process_functions[instr.instruction](instr)
