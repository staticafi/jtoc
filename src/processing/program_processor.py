from pathlib import Path
from typing import TextIO

from processing.expressions import Array, Constant, Expression, Nil, Symbol
from static import JTOC_LIBRARY_STATIC, logger, JTOC_LIBRARY_STRUCTS, JTOC_LIBRARY_FUNCTIONS
from processing.data import AssignLine, DeclLine, FunctionCallLine, HeaderLine, InputArgument, ProgramFunction, ProgramLine, ProgramStaticVar, ProgramStruct, TextLine
from processing.line_processor import LineProcessor
import static
from structs.function import GotoFunction
from structs.type import Type
from structs.symbol_table import SymbolTable


class FunctionSection:
    def __init__(self, symbols: SymbolTable, processor: LineProcessor, functions: list[GotoFunction]) -> None:
        self.symbols = symbols
        self.processor = processor
        self.functions: list[ProgramFunction] = self._process_all(functions)

    def _process_all(self, functions: list[GotoFunction]) -> list[ProgramFunction]:
        translated: list[ProgramFunction] = []
        for f in functions:
            if f.name in JTOC_LIBRARY_FUNCTIONS:
                continue

            program_func = self._process(f)
            if '<init>' in f.name and len(program_func.body) == 1:
                if 'to_construct = this;' in str(program_func.body[0]):
                    program_func.body = []
            translated.append(program_func)

        return translated

    def _process_body(self, func: GotoFunction, name: str) -> list[ProgramLine]:
        logger.info(f'translating body of function {func.name}')
        lines: list[ProgramLine] = []

        if name == 'main':
            lines.append(FunctionCallLine(indent=1, func_name='___initialize_static_structs___', args=[]))

        for instr in func.instructions:
            if instr.label:
                label_line = f'{self.symbols.unify_label(instr.label)}:'
                lines.append(TextLine(indent=0, text=label_line))

            line = self.processor.get_line(instr)
            if line:
                lines.append(line)

        if 'main' in func.name:
            lines.append(TextLine(indent=1, text='return 0;'))

        return lines

    def _process_header(self, func: GotoFunction, name: str) -> HeaderLine:
        if name == 'main':
            return HeaderLine.main_function_header()

        return_type = self.symbols.get_func_return_type(func.name)
        unified_return_type = self.processor.unify_type(return_type)

        arg_list: list[InputArgument] = []
        for arg_id in func.signature:
            arg_type = self.symbols.get_symbol_type(arg_id)
            unified_type = self.processor.unify_type(arg_type)
            unified_name = self.symbols.unify_symbol_name(arg_id)
            arg_list.append(InputArgument(unified_type, unified_name))

        return HeaderLine(return_type=unified_return_type, unified_name=name, args=arg_list)

    def _process(self, func: GotoFunction) -> ProgramFunction:
        logger.info(f'processing function {func.name}')
        unified_name = self.symbols.unify_func_name(func.name)
        body = self._process_body(func, unified_name)
        header = self._process_header(func, unified_name)

        return ProgramFunction(header=header, body=body)

    def write_to_file(self, write_to: TextIO | None) -> None:
        print('// ========== FUNCTIONS SECTION ==========', file=write_to)

        for function in self.functions:
            if function.header.unified_name == 'main':
                continue

            print(str(function.header), ';', sep='', file=write_to)
    
        print('\n', file=write_to)

        for function in self.functions:
            print(str(function), file=write_to)
            print('\n', file=write_to)
        
        if 'main' not in [f.header.unified_name for f in self.functions]:
            print(f'int main() {{\n{static.INDENT_WIDTH * " "}return 0;\n}}', file=write_to)


class StructsSection:
    def __init__(self, symbols: SymbolTable, processor: LineProcessor) -> None:
        self.symbols = symbols
        self.processor = processor
        self.structs: list[ProgramStruct] = self._process()

    def _process(self) -> list[ProgramStruct]:
        structs: list[ProgramStruct] = []
        for c in self.symbols.get_classes():
            components = c['type']['namedSub']['components']['sub']
            unified_name = self.symbols.unify_symbol_name(c['name'])

            if unified_name in JTOC_LIBRARY_STRUCTS:
                continue

            lines: list[DeclLine] = []

            for component in components:
                component_type = self.processor.unify_type(Type(component['namedSub']['type']))
                component_name = self.symbols.unify_symbol_name(component["namedSub"]["name"]["id"])
                line = DeclLine(indent=1, var_type=component_type, var_name=component_name, array_width=None)
                lines.append(line)

            structs.append(ProgramStruct(unified_name=unified_name, body=lines))

        return structs

    def write_to_file(self, write_to: TextIO | None) -> None:
        print('// ========== STRUCTS SECTION ==========', file=write_to)
        for struct in self.structs:
            print(struct.header, file=write_to)

        print('\n', file=write_to)

        for struct in self.structs:
            print(str(struct), file=write_to)
            print('\n', file=write_to)


class StaticSection:
    def __init__(self, symbols: SymbolTable, processor: LineProcessor) -> None:
        self.symbols = symbols
        self.processor = processor
        self.to_be_initialized: list[TextLine] = []
        self.statics: list[ProgramStaticVar | DeclLine] = []
        self._process()

    def _is_literal_constarray(self, name: str) -> bool:
        return name.startswith("java::java.lang.String.Literal.") and name.endswith('constarray')

    def _handle_literals(self, var_name: str, var_value: Expression) -> None:
        assert isinstance(var_value, Array)
        
        const_string_value = ''.join([chr(int(str(e))) for e in var_value.elements])
        value = Constant.build(value=f'"{const_string_value}"')

        static = ProgramStaticVar(unified_name=var_name, var_type='char *', array_width=None, assigned_value=value)
        self.statics.append(static)

    def _process(self) -> None:
        for name in self.symbols.get_static_variables():
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

    def get_static_initialization_func(self) -> ProgramFunction:
        header = HeaderLine(return_type='void', unified_name='___initialize_static_structs___', args=[])
        return ProgramFunction(header=header, body=self.to_be_initialized)

    def write_to_file(self, write_to: TextIO | None) -> None:
        print('// ========== STATIC SECTION ==========', file=write_to)
        for static_var in self.statics:
            print(str(static_var), file=write_to)
        
        print('\n', file=write_to)

        print(str(self.get_static_initialization_func()), file=write_to)


class ProgramProcessor:
    def __init__(self, symbols: SymbolTable, functions: list[GotoFunction]) -> None:
        self.symbols = symbols
        line_processor = LineProcessor(self.symbols)
        
        self.functions = FunctionSection(self.symbols, line_processor, functions)
        self.structs = StructsSection(self.symbols, line_processor)
        self.statics = StaticSection(self.symbols, line_processor)

    def get_includes(self) -> str:
        return '#include <stdio.h>\n#include <stdbool.h>\n' \
               '#include <stdlib.h>\n\n#include "../lib/jtoc_lib.c"\n'

    def write_to_file(self, write_file: Path | None) -> None:
        if not write_file:
            file = None
        else:
            file = open(write_file, 'w')
        
        try:
            print(self.get_includes(), file=file)
            self.statics.write_to_file(write_to=file)
            self.structs.write_to_file(write_to=file)
            self.functions.write_to_file(write_to=file)
        except Exception as ex:
            logger.error(ex)
            if file and not file.closed:
                file.close()
