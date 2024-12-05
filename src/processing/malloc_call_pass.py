from processing.data import AssignLine, ProgramFunction, ProgramLine
from processing.expressions import Constant, ExpressionType, SideEffect, Symbol
from structs.symbol_table import SymbolTable


class MallocPass:
    def __init__(self, symbols: SymbolTable) -> None:
        self.symbols = symbols

    def contains_malloc(self, line: ProgramLine) -> bool:
        if not isinstance(line, AssignLine):
            return False
        
        assert isinstance(line, AssignLine)
        if line.rhs.expr_type != ExpressionType.SideEffect:
            return False

        assert isinstance(line.rhs, SideEffect)
        if line.rhs.effect != 'allocate':
            return False

        if line.lhs.expr_type != ExpressionType.Symbol:
            return False

        assert isinstance(line.lhs, Symbol)
        lhs_type = self.symbols.get_symbol_type(line.lhs.original)
        return lhs_type.is_pointer()

    def correct_malloc_size(self, line: AssignLine) -> None:
        assert isinstance(line.lhs, Symbol)
        assert isinstance(line.rhs, SideEffect)

        lhs_type = self.symbols.get_symbol_type(line.lhs.original)
        pointer_to = lhs_type.inside
        assert pointer_to is not None

        first_arg = Constant.build(f'sizeof(struct {self.symbols.unify_symbol_name(pointer_to.raw_name)})')
        line.rhs.args[0] = first_arg

    def pass_one_function(self, function: ProgramFunction) -> None:
        for line in function.body:
            if self.contains_malloc(line):
                self.correct_malloc_size(line)

            