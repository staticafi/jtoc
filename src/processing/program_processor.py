from pathlib import Path

from logger import logger
from processing.data import ProgramFunction, ProgramLine
from processing.line_processor import LineProcessor
from structs.function import GotoFunction
from structs.irep import Type
from structs.symbol_table import SymbolTable


class ProgramProcessor:
    def __init__(self, symbols: SymbolTable) -> None:
        self.symbols = symbols
        self.functions: dict[str, ProgramFunction] = {}
        self.classes: dict[str, ProgramFunction] = {}

    def translate_body(self, func: GotoFunction) -> list[ProgramLine]:
        logger.info(f'translating body of function {func.name}')
        lines: list[ProgramLine] = [ProgramLine(line='{', indent=0)]

        for instr in func.instructions:
            if instr.label:
                label_line = f'{LineProcessor.unify_label(instr.label)}:'
                lines.append(ProgramLine(line=label_line, indent=0))

            for line in LineProcessor.get_line(instr):
                lines.append(line)

        if 'main' in func.name:
            lines.append(ProgramLine(line='return 0;', indent=1))
        lines.append(ProgramLine(line='}', indent=0))
        return lines

    def translate_header(self, func: GotoFunction, name: str) -> ProgramLine:
        return_type = func.get_return_type()
        
        arg_list: list[str] = []
        for arg_id in func.signature:
            arg_type = self.symbols.get_symbol_type(arg_id)
            arg_name = LineProcessor.unify_symbol_name(arg_id)

            arg_list.append(f'{arg_type} {arg_name}')
        
        if name == 'main':
            return ProgramLine('int main(int agrc, char **argv)', indent=0)

        return ProgramLine(f'{return_type} {name}({", ".join(arg_list)})', indent=0)

    def translate(self, func: GotoFunction) -> ProgramFunction:
        logger.info(f'translating function {func.name}')
        body = self.translate_body(func)
        name = LineProcessor.unify_func_name(func.name)
        header = self.translate_header(func, name)
        return ProgramFunction(unified_name=name, body=body, header=header)

    def process(self, functions: list[GotoFunction]) -> None:
        translated: dict[str, ProgramFunction] = {}
        for f in functions:
            if f.is_internal:
                continue

            program_func = self.translate(f)  # translate instructions in functions into lines
            translated[program_func.unified_name] = program_func

        self.functions = translated

        structs: dict[str, ProgramFunction] = {}
        for c in self.symbols.get_classes():
            components = c['type']['namedSub']['components']['sub']
            lines: list[ProgramLine] = [ProgramLine(line='{', indent=0)]

            for component in components:
                component_type = Type(component['namedSub']['type'])
                component_name = LineProcessor.unify_symbol_name(component["namedSub"]["name"]["id"])
                line = f'{component_type._type} {component_name}'
                lines.append(ProgramLine(line, indent=1))

            name = c['name']
            header = f'struct {LineProcessor.unify_symbol_name(name)}'
            lines.append(ProgramLine(line='}', indent=0))
            structs[name] = ProgramFunction(name, lines, header)

        self.classes = structs


    def write_to_stdout(self) -> str:
        print('#include <stdio.h>\n')

        for struct in self.classes.values():
            print(str(struct.header), ';', sep='')

        print('\n')
        for name in self.classes:
            if 'array' in name:
                continue
            print(str(self.classes[name]))
            print('\n')

        for function in self.functions.values():
            if function.unified_name == 'main':
                continue

            print(str(function.header), ';', sep='')
    
        print('\n')

        for function in self.functions.values():
            print(str(function))
            print('\n')

    def write_to_file(self, file: Path) -> None:
        with open(file, 'w') as file:
            print('#include <stdio.h>', file=file)
            print('#include <stdbool.h>\n', file=file)
            if 'main' in self.functions:
                print(self.functions['main'], file=file)
            print('\n', file=file)
