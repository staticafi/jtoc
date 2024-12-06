from typing import TextIO

from processing.line_processor import LineProcessor
from processing.program_parts.complex import ProgramStruct
from processing.program_parts.lines import DeclLine
from static import JTOC_LIBRARY_STRUCTS
from structs.type import Type
from structs.symbol_table import SymbolTable


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