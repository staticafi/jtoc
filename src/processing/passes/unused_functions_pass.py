from processing.passes.program_pass import ProgramPass
from processing.program_parts.lines import FunctionCallLine 
from processing.program_parts.complex import ProgramFunction, ProgramLine
from static import JTOC_LIBRARY_FUNCTIONS
from structs.symbol_table import SymbolTable


class UnusedFunctionsPass(ProgramPass):
    def __init__(self, symbols: SymbolTable, functions: list[ProgramFunction]) -> None:
        self.symbols = symbols
        self.functions = functions

    def _calls_other_program_function(self, line: ProgramLine) -> bool:
        if not isinstance(line, FunctionCallLine):
            return False

        return line.func_name not in JTOC_LIBRARY_FUNCTIONS

    def _pass_one_function(self, function: ProgramFunction) -> set[str]:
        called_functions: set[str] = set()
        for line in function.body:
            if not self._calls_other_program_function(line):
                continue

            assert isinstance(line, FunctionCallLine)
            called_functions.add(line.func_name)
    
        return called_functions

    def do_the_pass(self) -> None:
        num_of_calls: dict[str, set[str]] = {}
        name_to_func: dict[str, ProgramFunction] = {f.header.unified_name: f for f in self.functions}

        for f in self.functions:
            num_of_calls.setdefault(f.header.unified_name, 0)
            if f.header.unified_name == 'main':
                num_of_calls['main'] += 1

            for called_f in self._pass_one_function(f):
                num_of_calls[called_f] = num_of_calls.get(called_f, 0) + 1 

        for f_name in num_of_calls:
            if num_of_calls.get(f_name, 0) == 0 and name_to_func.get(f_name):
                self.functions.remove(name_to_func[f_name])
