from typing import TextIO

from processing.expressions.expressions import ExpressionType, Symbol
from processing.line_processor import LineProcessor
from processing.passes.malloc_call_pass import MallocCallPass
from processing.passes.program_pass import ProgramPass
from processing.passes.unused_functions_pass import UnusedFunctionsPass
from processing.program_parts.complex import ProgramFunction
from processing.program_parts.lines import AssignLine, FunctionCallLine, HeaderLine, InputParameter, ProgramLine, TextLine
from processing.sections.program_section import ProgramSection
from static import logger, JTOC_LIBRARY_FUNCTIONS
from structs.function import GotoFunction
from structs.symbol_table import SymbolTable


class FunctionSection(ProgramSection):
    def __init__(self, symbols: SymbolTable, processor: LineProcessor, functions: list[GotoFunction]) -> None:
        self.symbols = symbols
        self.processor = processor
        self._cprover_init_function: ProgramFunction | None = None
        self.functions: list[ProgramFunction] = self._process_all(functions)

    def _process_all(self, functions: list[GotoFunction]) -> list[ProgramFunction]:
        translated: list[ProgramFunction] = []

        for f in functions:
            unified = self.symbols.unify_func_name(f.name)
            if unified in JTOC_LIBRARY_FUNCTIONS:
                continue

            program_func = self._process(f)
            if '<init>' in f.name and len(program_func.body) == 1:
                if 'to_construct = this;' in str(program_func.body[0]):
                    program_func.body = []

            if '__CPROVER_initialize' in f.name:
                self._cprover_init_function = program_func
            elif '__CPROVER__start' not in f.name:
                translated.append(program_func)

        return translated

    def _process_body(self, func: GotoFunction, name: str) -> list[ProgramLine]:
        logger.info(f'translating body of function {func.name}')
        lines: list[ProgramLine] = []

        if name == 'main':
            lines.append(FunctionCallLine(indent=1, func_name='___initialize_static_structs___', args=[]))

        for instr in func.instructions:
            if instr.label:
                label_line = f'{self.symbols.unify_label(instr.label)}:;'
                lines.append(TextLine(indent=0, text=label_line))

            line = self.processor.get_line(instr)
            if line:
                lines.append(line)

        if name == 'main':
            lines.append(TextLine(indent=1, text='return 0;'))

        return lines

    def _process_header(self, func: GotoFunction, name: str) -> HeaderLine:
        if name == 'main':
            return HeaderLine.main_function_header()

        return_type = self.symbols.get_func_return_type(func.name)
        unified_return_type = self.processor.unify_type(return_type)

        arg_list: list[InputParameter] = []
        for arg_id in func.signature:
            arg_type = self.symbols.get_symbol_type(arg_id)
            unified_type = self.processor.unify_type(arg_type)
            unified_name = self.symbols.unify_symbol_name(arg_id)
            arg_list.append(InputParameter(unified_type, unified_name))

        return HeaderLine(return_type=unified_return_type, unified_name=name, args=arg_list)

    def _process(self, func: GotoFunction) -> ProgramFunction:
        logger.info(f'processing function {func.name}')
        unified_name = self.symbols.unify_func_name(func.name)
        body = self._process_body(func, unified_name)
        header = self._process_header(func, unified_name)

        return ProgramFunction(header=header, body=body)

    def _pass_through_functions(self) -> None:
        passes: list[ProgramPass] = [
            MallocCallPass(self.symbols, self.functions),
            UnusedFunctionsPass(self.symbols, self.functions)
        ]

        for _pass in passes:
            _pass.do_the_pass()

    def get_class_models(self) -> list[AssignLine]:
        assigns: list[AssignLine] = []
        for line in self._cprover_init_function.body:
            if not isinstance(line, AssignLine) or line.lhs.expr_type != ExpressionType.Symbol:
                continue

            assert isinstance(line.lhs, Symbol)
            if line.lhs.original.endswith('@class_model'):
                assigns.append(line)

        return assigns

    def write_to_file(self, write_to: TextIO | None) -> None:
        self._pass_through_functions()

        print('// ========== FUNCTIONS SECTION ==========', file=write_to)

        for function in self.functions:
            if function.header.unified_name == 'main':
                continue

            print(str(function.header), ';', sep='', file=write_to)
    
        print('\n', file=write_to)

        for function in self.functions:
            print(str(function), file=write_to)
            print('\n', file=write_to)