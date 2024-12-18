from processing.expressions.expressions import Constant, ExpressionType, SideEffect, Symbol
from processing.passes.program_pass import ProgramPass
from processing.program_parts.complex import ProgramFunction
from processing.program_parts.lines import AssignLine, ProgramLine
from structs.symbol_table import SymbolTable


class MallocCallPass(ProgramPass):
    def __init__(self, symbols: SymbolTable, functions: list[ProgramFunction]) -> None:
        self.symbols = symbols
        self.functions = functions

    def _contains_malloc(self, line: ProgramLine) -> bool:
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

    def _correct_malloc_size(self, line: AssignLine) -> None:
        assert isinstance(line.lhs, Symbol)
        assert isinstance(line.rhs, SideEffect)

        lhs_type = self.symbols.get_symbol_type(line.lhs.original)
        pointer_to = lhs_type.inside
        assert pointer_to is not None
        
        # this if shouldn't happen in normal user-written code, only in JBMC backend
        if pointer_to.is_array():
            return

        first_arg = Constant.build(f'sizeof(struct {self.symbols.unify_symbol_name(pointer_to.raw_name)})')
        line.rhs.args[0] = first_arg

    def _pass_one_function(self, function: ProgramFunction) -> None:
        for line in function.body:
            if self._contains_malloc(line):
                self._correct_malloc_size(line)

    def do_the_pass(self) -> None:
        for f in self.functions:
            self._pass_one_function(f)
