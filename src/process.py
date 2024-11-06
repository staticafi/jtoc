import sys

from pathlib import Path

from capture import parse_functions, capture, parse_symbols
from logger import logger
from processing.program_processor import ProgramProcessor


def process_input(file: str, where_to: Path | None=None) -> None:
    classname = Path(file).name.split('.')[0]
    goto, symbol = capture(classname)
    functions = parse_functions(goto)
    symbols = parse_symbols(symbol)

    processor = ProgramProcessor(symbols)
    processor.process(functions)
    
    processor.write_to_file(where_to)


if __name__ == '__main__':
    if len(sys.argv) not in {2, 3}:
        logger.warning(f'Expected argument with path to the java file. Got {sys.argv}')
        logger.warning('Optionally add path to file as output')
        sys.exit(1)

    arg2 = None
    if len(sys.argv) == 3:
        arg2 = sys.argv[2]
    process_input(sys.argv[1], arg2)
