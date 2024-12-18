from typing import TextIO

from processing.expressions.expressions import Array, Constant, Expression, Symbol
from processing.line_processor import LineProcessor
from processing.passes.class_model_init_pass import ClassModelInitPass
from processing.passes.program_pass import ProgramPass
from processing.passes.unify_null_pass import UnifyNullPass
from processing.program_parts.complex import ProgramFunction, ProgramStaticVar
from processing.program_parts.lines import AssignLine, DeclLine, HeaderLine
from processing.sections.program_section import ProgramSection
from static import JTOC_LIBRARY_STATIC
from structs.symbol_table import SymbolTable


class StaticSection(ProgramSection):
    def __init__(self, symbols: SymbolTable, processor: LineProcessor,
                 class_models: list[AssignLine]) -> None:
        self.symbols = symbols
        self.processor = processor
        self.class_models: list[AssignLine] = class_models
        self.to_be_initialized: list[AssignLine] = []
        self.statics: list[ProgramStaticVar | DeclLine] = []
        self._process()

    def _is_literal_constarray(self, name: str) -> bool:
        return name.startswith("java::java.lang.String.Literal.") and name.endswith('constarray')

    def _handle_literals(self, var_name: str, var_value: Expression) -> None:
        assert isinstance(var_value, Array)
        
        chars: list[str] = []
        for expr in var_value.elements:
            str_expr = str(expr)
            if str_expr == '\n':
                chars.append('\\n')
            else:
                chars.append(chr(int(str_expr)))

        const_string_value = ''.join(chars)
        value = Constant.build(value=f'"{const_string_value}"')

        static = ProgramStaticVar(unified_name=var_name, var_type='char *', array_width=None, assigned_value=value)
        self.statics.append(static)

    def _process(self) -> None:
        static_variables: list[str] = self.symbols.get_static_variables()
        static_variables.extend(self.symbols.get_to_return_variables())

        for name in static_variables:
            var_name = self.symbols.unify_symbol_name(name)
            var_type = self.symbols.get_symbol_type(name)
            
            if 'Literal' in var_name and var_name.endswith('_return_value'):
                continue
            
            if var_name in JTOC_LIBRARY_STATIC:
                continue

            array_width = None
            if var_type.is_array():
                array_width = var_type.width

            unified_type = self.processor.unify_type(var_type)
            var_value = self.processor.to_expression(self.symbols.get_static_var_value(name)) 

            if self._is_literal_constarray(name):
                self._handle_literals(var_name, var_value)

            elif var_type.is_struct():
                decl_line = DeclLine(indent=0, var_type=unified_type, var_name=var_name, array_width=None)
                self.statics.append(decl_line)

                struct_name = Symbol.build(original=name, unified=var_name)
                self.to_be_initialized.append(AssignLine(indent=1, lhs=struct_name, rhs=var_value))
    
            else:
                line = ProgramStaticVar(unified_name=var_name, var_type=unified_type, 
                                        array_width=array_width, assigned_value=var_value)
                self.statics.append(line)

    def _pass_through_statics(self) -> None:
        passes: list[ProgramPass] = [
            UnifyNullPass(self.symbols, self.statics),
            ClassModelInitPass(self.symbols, self.to_be_initialized, self.class_models)
        ]

        for _pass in passes:
            _pass.do_the_pass()

    def get_static_initialization_func(self) -> ProgramFunction:
        header = HeaderLine(return_type='void', unified_name='___initialize_static_structs___', args=[])
        return ProgramFunction(header=header, body=self.to_be_initialized)

    def write_to_file(self, write_to: TextIO | None) -> None:
        self._pass_through_statics()

        print('// ========== STATIC SECTION ==========', file=write_to)
        for static_var in self.statics:
            print(str(static_var), file=write_to)
        
        print('\n', file=write_to)

        print(str(self.get_static_initialization_func()), '\n', sep='', file=write_to)
