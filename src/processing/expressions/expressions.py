from __future__ import annotations

from dataclasses import dataclass
from processing.expressions.expression_type import ExpressionType
from structs.type import Type


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
    nondet_type: Type | None

    @staticmethod
    def build(effect: str, args: list[Expression], nondet_type: Type | None) -> SideEffect:
        return SideEffect(expr_type=ExpressionType.SideEffect, effect=effect, args=args, nondet_type=nondet_type)

    @staticmethod
    def _get_nondet_unified_func_name(_type: Type) -> str:
        if _type == 'bool':
            return 'nondetBoolean_org_sosy_lab_sv_benchmarks_Verifier___Z'
        if _type == 'double':
            return 'nondetDouble_org_sosy_lab_sv_benchmarks_Verifier___D'
        if _type == 'float':
            return 'nondetFloat_org_sosy_lab_sv_benchmarks_Verifier___F'
        if _type == 'int':
            return 'nondetInt_org_sosy_lab_sv_benchmarks_Verifier___I'
        if _type == 'long long int':
            return 'nondetLong_org_sosy_lab_sv_benchmarks_Verifier___J'
        if _type == 'char' or _type == 'unsigned short int':
            return 'nondetChar_org_sosy_lab_sv_benchmarks_Verifier___C'
        if _type == 'signed char':
            return 'nondetByte_org_sosy_lab_sv_benchmarks_Verifier___B'
        if _type == 'short int':
            return 'nondetShort_org_sosy_lab_sv_benchmarks_Verifier___S'
        
        return 'nondetInt_org_sosy_lab_sv_benchmarks_Verifier___I'

    def __str__(self) -> str:
        effect = self.effect

        if self.effect in {'allocate', 'java_new_array_data'}:
            effect = 'malloc'
        if self.effect == 'nondet':
            effect = SideEffect._get_nondet_unified_func_name(self.nondet_type)

        args = ', '.join([str(a) for a in self.args])
        return f'{effect}({args})'


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
            chars = [f"'{chr(int(e))}'" for e in elements]
            chars.append("'\\0'")
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

