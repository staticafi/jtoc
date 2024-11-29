from pathlib import Path
from typing import TextIO

from static import logger
from processing.data import DeclLine, HeaderLine, InputArgument, ProgramFunction, ProgramLine, ProgramStaticVar, ProgramStruct, TextLine
from processing.line_processor import LineProcessor
from structs.function import GotoFunction
from structs.type import Type
from structs.symbol_table import SymbolTable


STRING_LIBRARY_FUNCTIONS = {
    'java::java.lang.String.<init>:()V',
    'java::java.lang.String.compareTo:(Ljava/lang/String;)I',
    'java::java.lang.String.concat:(Ljava/lang/String;)Ljava/lang/String;',
    'java::java.lang.String.contains:(Ljava/lang/CharSequence;)Z',
    'java::java.lang.String.endsWith:(Ljava/lang/String;)Z',
    'java::java.lang.String.equalsIgnoreCase:(Ljava/lang/String;)Z',
    'java::java.lang.String.indexOf:(I)I',
    'java::java.lang.String.indexOf:(II)I',
    'java::java.lang.String.indexOf:(Ljava/lang/String;)I',
    'java::java.lang.String.indexOf:(Ljava/lang/String;I)I',
    'java::java.lang.String.isEmpty:()Z',
    'java::java.lang.String.lastIndexOf:(I)I',
    'java::java.lang.String.lastIndexOf:(II)I',
    'java::java.lang.String.lastIndexOf:(Ljava/lang/String;)I',
    'java::java.lang.String.lastIndexOf:(Ljava/lang/String;I)I',
    'java::java.lang.String.length:()I',
    'java::java.lang.String.replace:(CC)Ljava/lang/String;',
    'java::java.lang.String.replace:(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;',
    'java::java.lang.String.startsWith:(Ljava/lang/String;)Z',
    'java::java.lang.String.startsWith:(Ljava/lang/String;I)Z',
    'java::java.lang.String.toLowerCase:()Ljava/lang/String;',
    'java::java.lang.String.toString:()Ljava/lang/String;',
    'java::java.lang.String.toUpperCase:()Ljava/lang/String;',
    'java::java.lang.String.trim:()Ljava/lang/String;',
    'java::java.lang.StringBuilder.<init>:(Ljava/lang/String;)V',
    'java::java.lang.StringBuilder.<init>:(Ljava/lang/CharSequence;)V',
    'java::java.lang.StringBuilder.<init>:()V',
    'java::java.lang.StringBuilder.<init>:(I)V',
    'java::java.lang.StringBuilder.append:(C)Ljava/lang/StringBuilder;',
    'java::java.lang.StringBuilder.append:(Ljava/lang/CharSequence;)Ljava/lang/StringBuilder;',
    'java::java.lang.StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;',
    'java::java.lang.StringBuilder.append:(Ljava/lang/StringBuffer;)Ljava/lang/StringBuilder;',
    'java::java.lang.StringBuilder.appendCodePoint:(I)Ljava/lang/StringBuilder;',
    'java::java.lang.StringBuilder.charAt:(I)C',
    'java::java.lang.StringBuilder.codePointAt:(I)I',
    'java::java.lang.StringBuilder.codePointBefore:(I)I',
    'java::java.lang.StringBuilder.codePointCount:(II)I',
    'java::java.lang.StringBuilder.length:()I',
    'java::java.lang.StringBuilder.substring:(II)Ljava/lang/String;',
    'java::java.lang.StringBuilder.substring:(I)Ljava/lang/String;',
    'java::java.lang.StringBuilder.toString:()Ljava/lang/String;',
    'java::java.lang.StringBuffer.<init>:(Ljava/lang/String;)V',
    'java::java.lang.StringBuffer.<init>:()V',
    'java::java.lang.StringBuffer.append:(C)Ljava/lang/StringBuffer;',
    'java::java.lang.StringBuffer.append:(Ljava/lang/String;)Ljava/lang/StringBuffer;',
    'java::java.lang.StringBuffer.append:(Ljava/lang/StringBuffer;)Ljava/lang/StringBuffer;',
    'java::java.lang.StringBuffer.appendCodePoint:(I)Ljava/lang/StringBuffer;',
    'java::java.lang.StringBuffer.codePointAt:(I)I',
    'java::java.lang.StringBuffer.codePointBefore:(I)I',
    'java::java.lang.StringBuffer.codePointCount:(II)I',
    'java::java.lang.StringBuffer.length:()I',
    'java::java.lang.StringBuffer.substring:(I)Ljava/lang/String;',
    'java::java.lang.StringBuffer.toString:()Ljava/lang/String;',
    'java::java.lang.CharSequence.charAt:(I)C',
    'java::java.lang.CharSequence.toString:()Ljava/lang/String;',
    'java::java.lang.CharSequence.length:()I',
}


STRING_LIBRARY_STRUCTS = {
    'struct java_lang_Object',
    'struct java_lang_AbstractStringBuilder',
    'struct java_lang_CharSequence',
    'struct java_lang_String',
    'struct java_lang_StringBuilder',
    'struct java_lang_StringBuffer'
}


class FunctionSection:
    def __init__(self, processor: LineProcessor, symbols: SymbolTable, functions: list[GotoFunction]) -> None:
        self.processor = processor
        self.symbols = symbols
        self.functions: list[ProgramFunction] = self._process_all(functions)

    def _process_all(self, functions: list[GotoFunction]) -> list[ProgramFunction]:
        translated: list[ProgramFunction] = []
        for f in functions:
            if f.name in STRING_LIBRARY_FUNCTIONS:
                continue

            program_func = self._process(f)
            translated.append(program_func)

        return translated

    def _process_body(self, func: GotoFunction) -> list[ProgramLine]:
        logger.info(f'translating body of function {func.name}')
        lines: list[ProgramLine] = [TextLine(indent=0, text='{')]

        for instr in func.instructions:
            if instr.label:
                label_line = f'{self.symbols.unify_label(instr.label)}:'
                lines.append(TextLine(indent=0, text=label_line))

            line = self.processor.get_line(instr)
            if line:
                lines.append(line)

        if 'main' in func.name:
            lines.append(TextLine(indent=1, text='return 0;'))
        lines.append(TextLine(indent=0, text='}'))

        return lines

    def _process_header(self, func: GotoFunction, name: str) -> HeaderLine:
        if name == 'main':
            return HeaderLine.main_function_header

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
        body = self._process_body(func)
        header = self._process_header(func, unified_name)

        return ProgramFunction(unified_name=unified_name, body=body, header=header)

    def write_to_file(self, write_to: TextIO | None) -> None:
        print('// ========== FUNCTIONS SECTION ==========', file=write_to)

        for function in self.functions:
            if function.unified_name == 'main':
                continue

            print(str(function.header), ';', sep='', file=write_to)
    
        print('\n', file=write_to)

        for function in self.functions:
            print(str(function), file=write_to)
            print('\n', file=write_to)


class StructsSection:
    def __init__(self, symbols: SymbolTable) -> None:
        self.symbols = symbols
        self.structs: list[ProgramStruct] = self._process() 

    def _process(self) -> list[ProgramStruct]:
        structs: list[ProgramStruct] = []
        for c in self.symbols.get_classes():
            components = c['type']['namedSub']['components']['sub']
            unified_name = self.symbols.unify_symbol_name(c['name'])

            if f'struct {unified_name}' in STRING_LIBRARY_STRUCTS:
                continue

            lines: list[DeclLine] = []

            for component in components:
                component_type = Type(component['namedSub']['type'])
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
        self.statics: list[ProgramStaticVar] = self._process()

    def _process(self) -> list[ProgramStaticVar]:
        static_vars: list[ProgramStaticVar] = []
        for name in self.symbols.get_static_variables():
            var_name = self.symbols.unify_symbol_name(name)
            var_type = self.symbols.get_symbol_type(name)
            
            if 'Literal' in var_name and var_name.endswith('_return_value'):
                continue
            
            array_width = None
            if var_type.is_array():
                array_width = var_type.width

            unified_type = self.processor.unify_type(var_type)
            var_value = self.processor.to_expression(self.symbols.get_static_var_value(name)) 

            line = ProgramStaticVar(unified_name=var_name, var_type=unified_type, 
                                    array_width=array_width, assigned_value=var_value)
            static_vars.append(line)

        return static_vars

    def write_to_file(self, write_to: TextIO | None) -> None:
        print('// ========== STATIC SECTION ==========', file=write_to)
        for static_var in self.statics:
            print(str(static_var), file=write_to)
        
        print('\n', file=write_to)


class ProgramProcessor:
    def __init__(self, symbols: SymbolTable, functions: list[GotoFunction]) -> None:
        self.symbols = symbols
        line_processor = LineProcessor(self.symbols)
        
        self.functions = FunctionSection(line_processor, self.symbols, functions)
        self.structs = StructsSection(self.symbols)
        self.statics = StaticSection(self.symbols, line_processor)

    def get_includes(self) -> str:
        return '#include <stdio.h>\n#include <stdbool.h>\n' \
               '#include <stdlib.h>\n\n#include "lib/jtoc_string.c"\n'

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
        except:
            if file and not file.closed:
                file.close()
