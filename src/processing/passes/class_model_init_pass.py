from processing.expressions.expressions import ExpressionType, Symbol
from processing.passes.program_pass import ProgramPass
from processing.program_parts.lines import AssignLine
from structs.symbol_table import SymbolTable


class ClassModelInitPass(ProgramPass):
    def __init__(self, symbols: SymbolTable, to_be_initialized: list[AssignLine], 
                 class_models: list[AssignLine]) -> None:
        self.symbols = symbols
        self.to_be_initialized = to_be_initialized
        self.initialized_models = class_models

    def _is_class_model(self, line: AssignLine) -> bool:
        if line.lhs.expr_type != ExpressionType.Symbol:
            return False

        assert isinstance(line.lhs, Symbol)
        return self.symbols.is_static_symbol(line.lhs.original) and \
            line.lhs.original.endswith('@class_model')

    def _pass_line(self, line: AssignLine) -> None:
        for model in self.initialized_models:
            if model.lhs == line.lhs:
                line.rhs = model.rhs

    def do_the_pass(self) -> None:
        for line in self.to_be_initialized:
            if self._is_class_model(line):
                self._pass_line(line)
