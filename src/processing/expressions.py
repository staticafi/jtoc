from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from structs.type import Type


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
        
        return ExpressionType(expr)


@dataclass
class Expression:
    expr_type: ExpressionType


@dataclass
class Nil(Expression):
    @staticmethod
    def build() -> Nil:
        return Operator(expr_type=ExpressionType.Nil)


@dataclass
class Constant(Expression):
    value: str

    @staticmethod
    def build(value: str) -> Constant:
        return Operator(expr_type=ExpressionType.Constant, value=value)


@dataclass
class Symbol(Expression):
    original: str
    unified: str

    @staticmethod
    def build(original: str, unified: str) -> Symbol:
        return Operator(expr_type=ExpressionType.Symbol, original=original, unified=unified)


@dataclass
class Typecast(Expression):
    typecast: str
    expression: Expression

    @staticmethod
    def build(typecast: str, expr: str) -> Typecast:
        return Operator(expr_type=ExpressionType.Typecast, typecast=typecast, expression=expr)


@dataclass
class Operator(Expression):
    op: str
    left: Expression
    right: Expression

    @staticmethod
    def build(op: str, left: Expression, right: Expression) -> Operator:
        return Operator(expr_type=ExpressionType.Operator, op=op, left=left, right=right)


@dataclass
class UnaryOperator(Expression):
    op: str
    value: Expression

    @staticmethod
    def build(op: str, value: Expression) -> UnaryOperator:
        return Operator(expr_type=ExpressionType.UnaryOperator, op=op, value=value)


@dataclass
class StructTag(Expression):
    symbol: Symbol

    @staticmethod
    def build(symbol: Symbol) -> StructTag:
        return Operator(expr_type=ExpressionType.StructTag, symbol=symbol)


@dataclass
class Pointer(Expression):
    expression: Expression

    @staticmethod
    def build(expr: Expression) -> Pointer:
        return Operator(expr_type=ExpressionType.Pointer, expression=expr)


@dataclass
class Dereference(Expression):
    expression: Expression

    @staticmethod
    def build(expr: Expression) -> Dereference:
        return Operator(expr_type=ExpressionType.Dereference, expression=expr)


@dataclass
class Address(Expression):
    expression: Expression

    @staticmethod
    def build(expr: Expression) -> Address:
        return Operator(expr_type=ExpressionType.Address, expression=expr)


@dataclass
class SideEffect(Expression):
    effect: str
    args: list[Expression]

    @staticmethod
    def build(effect: str, args: list[Expression]) -> SideEffect:
        return Operator(expr_type=ExpressionType.SideEffect, effect=effect, args=args)


@dataclass
class Struct(Expression):
    symbol: Symbol
    args: list[Expression]

    @staticmethod
    def build(symbol: Symbol, args: list[Expression]) -> Struct:
        return Operator(expr_type=ExpressionType.Struct, symbol=symbol, args=args)


@dataclass
class Member(Expression):
    member: Symbol
    obj: Expression

    @staticmethod
    def build(member: Symbol, obj: Expression) -> Member:
        return Operator(expr_type=ExpressionType.Member, member=member, obj=obj)


@dataclass
class Array(Expression):
    array_type: Type
    elements: list[Expression]

    @staticmethod
    def build(array_type: Type, elements: list[Expression]) -> Array:
        return Operator(expr_type=ExpressionType.Array, array_type=array_type, elements=elements)


@dataclass
class Index(Expression):
    index: Expression
    obj: Expression

    @staticmethod
    def build(index: Expression, obj: Expression) -> Index:
        return Operator(expr_type=ExpressionType.Index, index=index, obj=obj)


