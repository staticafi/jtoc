from pathlib import Path

from processing.line_processor import LineProcessor
from processing.sections.functions_section import FunctionSection
from processing.sections.program_section import ProgramSection
from processing.sections.static_section import StaticSection
from processing.sections.structs_section import StructsSection
from static import logger
from structs.function import GotoFunction
from structs.symbol_table import SymbolTable


class ProgramProcessor:
    def __init__(self, symbols: SymbolTable, functions: list[GotoFunction]) -> None:
        self.symbols = symbols
        line_processor = LineProcessor(self.symbols)
        
        self.functions = FunctionSection(self.symbols, line_processor, functions)
        self.structs = StructsSection(self.symbols, line_processor)
        self.statics = StaticSection(self.symbols, line_processor, self.functions.get_class_models())

    def get_includes(self) -> str:
        return '#include <stdio.h>\n#include <stdbool.h>\n' \
               '#include <stdlib.h>\n\n#include "../src/lib/jtoc_lib.c"\n\n'

    def write_to_file(self, write_file: Path | None) -> None:
        if not write_file:
            file = None
        else:
            file = open(write_file, 'w')
        
        sections: list[ProgramSection] = [
            self.structs,
            self.statics,
            self.functions
        ]

        try:
            print(self.get_includes(), file=file)
            for section in sections:
                section.write_to_file(write_to=file)
        except Exception as ex:
            logger.error(ex)
            if file and not file.closed:
                file.close()
            raise ex
        else:
            if file and not file.closed:
                file.close()
