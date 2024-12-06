from processing.expressions.expressions import Constant, ExpressionType
from processing.program_parts.lines import DeclLine
from processing.program_parts.complex import ProgramStaticVar
from processing.passes.program_pass import ProgramPass
from structs.symbol_table import SymbolTable


class UnifyNullPass(ProgramPass):
    def __init__(self, symbols: SymbolTable, statics: list[ProgramStaticVar | DeclLine]) -> None:
        self.symbols = symbols
        self.statics = statics
        self.conversion = {
            'bool': 'false',
            'float': '0.0',
            'double': '0.0',
            'char': "'\\0'",
            'unsigned short int': "'\\0'",
            'unsigned char': '0U',
            'unsigned int': '0U',
            'unsigned long long int': '0LL',
            'short int': '0',
            'int': '0',
            'long long int': '0LL'
        }

    def _pass_static(self, static: ProgramStaticVar | DeclLine) -> None:
        if isinstance(static, DeclLine):
            return 

        if static.assigned_value.expr_type == ExpressionType.Nil and \
            static.var_type in self.conversion:
                static.assigned_value = Constant.build(self.conversion[static.var_type])

    def do_the_pass(self) -> None:
        for static in self.statics:
            self._pass_static(static)
