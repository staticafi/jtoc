from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from static import logger
from structs.type import Type, Types


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



class ExpressionType(Enum):
    Nil = 'nil'
    Constant = 'constant'
    Symbol = 'symbol'
    Typecast = 'typecast'
    Operator = 'operator'
    UnaryOperator = 'unary_operator'
    StructTag = 'struct_tag'
    Pointer = 'pointer'
    Dereference = 'dereference'
    Address = 'address_of'
    SideEffect = 'side_effect'
    Struct = 'struct'
    Member = 'member'
    Array = 'array'
    Index = 'index'

    @staticmethod
    def from_expr(expr: str) -> ExpressionType:
        if expr in OPERATORS:
            return ExpressionType.Operator
        if expr in UNARY_OPERATORS:
            return ExpressionType.UnaryOperator
        if expr not in {type_.value for type_ in ExpressionType}:
            logger.info(f'[from_expr] unexpected expr {expr}')
            return ExpressionType.Nil

        return ExpressionType(expr)


@dataclass
class Expression:
    expr_type: ExpressionType


@dataclass
class Nil(Expression):
    @staticmethod
    def build() -> Nil:
        return Nil(expr_type=ExpressionType.Nil)

    def __str__(self) -> str:
        return 'NULL'


@dataclass
class Constant(Expression):
    value: str

    @staticmethod
    def build(value: str) -> Constant:
        return Constant(expr_type=ExpressionType.Constant, value=value)

    def __str__(self) -> str:
        return self.value


@dataclass
class Symbol(Expression):
    original: str
    unified: str

    @staticmethod
    def build(original: str, unified: str) -> Symbol:
        return Symbol(expr_type=ExpressionType.Symbol, original=original, unified=unified)

    def __str__(self) -> str:
        return self.unified


@dataclass
class Typecast(Expression):
    typecast: str
    expression: Expression

    @staticmethod
    def build(typecast: str, expr: str) -> Typecast:
        return Typecast(expr_type=ExpressionType.Typecast, typecast=typecast, expression=expr)

    def __str__(self) -> str:
        return f'({self.typecast}) ({self.expression})'


@dataclass
class Operator(Expression):
    op: str
    left: Expression
    right: Expression

    @staticmethod
    def build(op: str, left: Expression, right: Expression) -> Operator:
        return Operator(expr_type=ExpressionType.Operator, op=op, left=left, right=right)

    def __str__(self) -> str:
        return f'(({str(self.left)}) {self.op} ({str(self.right)}))'


@dataclass
class UnaryOperator(Expression):
    op: str
    value: Expression

    @staticmethod
    def build(op: str, value: Expression) -> UnaryOperator:
        return UnaryOperator(expr_type=ExpressionType.UnaryOperator, op=op, value=value)

    def __str__(self) -> str:
        return f'({self.op}{str(self.value)})'


@dataclass
class StructTag(Expression):
    symbol: Symbol

    @staticmethod
    def build(symbol: Symbol) -> StructTag:
        return StructTag(expr_type=ExpressionType.StructTag, symbol=symbol)

    def __str__(self) -> str:
        return f'struct {str(self.symbol)}'


@dataclass
class Pointer(Expression):
    expression: Expression

    @staticmethod
    def build(expr: Expression) -> Pointer:
        return Pointer(expr_type=ExpressionType.Pointer, expression=expr)

    def __str__(self) -> str:
        return f'({str(self.expression)}) *'


@dataclass
class Dereference(Expression):
    expression: Expression

    @staticmethod
    def build(expr: Expression) -> Dereference:
        return Dereference(expr_type=ExpressionType.Dereference, expression=expr)

    def __str__(self) -> str:
        return f'*({str(self.expression)})'


@dataclass
class Address(Expression):
    expression: Expression

    @staticmethod
    def build(expr: Expression) -> Address:
        return Address(expr_type=ExpressionType.Address, expression=expr)

    def __str__(self) -> str:
        return f'&({str(self.expression)})'


@dataclass
class SideEffect(Expression):
    effect: str
    args: list[Expression]

    @staticmethod
    def build(effect: str, args: list[Expression]) -> SideEffect:
        return SideEffect(expr_type=ExpressionType.SideEffect, effect=effect, args=args)

    def __str__(self) -> str:
        args = ', '.join([str(a) for a in self.args])
        return f'{self.effect}({args})'


@dataclass
class Struct(Expression):
    symbol: Symbol
    args: list[Expression]

    @staticmethod
    def build(symbol: Symbol, args: list[Expression]) -> Struct:
        return Struct(expr_type=ExpressionType.Struct, symbol=symbol, args=args)

    def __str__(self) -> str:
        args = ', '.join([str(a) for a in self.args])
        return f'(struct {str(self.symbol)}) {{ {args} }}'


@dataclass
class Member(Expression):
    member: Symbol
    obj: Expression

    @staticmethod
    def build(member: Symbol, obj: Expression) -> Member:
        return Member(expr_type=ExpressionType.Member, member=member, obj=obj)

    def __str__(self) -> str:
        return f'({str(self.obj)}).{str(self.member)}'


@dataclass
class Array(Expression):
    array_type: Type
    elements: list[Expression]

    @staticmethod
    def build(array_type: Type, elements: list[Expression]) -> Array:
        return Array(expr_type=ExpressionType.Array, array_type=array_type, elements=elements)

    def __str__(self) -> str:
        elements = [str(a) for a in self.elements]
        if self.array_type == 'unsigned short int' and all([e.isdigit() for e in elements]):
            chars = [f"'{chr(int(e))}'" for e in elements].extend(["'\\0'"])
            array = ', '.join(chars)
            return f'{{ {array} }}'
    
        array = ', '.join(elements)
        return f'{{ {array} }}'


@dataclass
class Index(Expression):
    index: Expression
    obj: Expression

    @staticmethod
    def build(index: Expression, obj: Expression) -> Index:
        return Index(expr_type=ExpressionType.Index, index=index, obj=obj)

    def __str__(self) -> str:
        return f'({str(self.obj)})[{str(self.index)}]'

