from __future__ import annotations

from enum import Enum

from static import logger


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
    '<=': '<=',
    'and': '&&',
    'or': '||'
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
