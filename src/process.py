import sys

from pathlib import Path

from capture import parse_functions, capture, parse_symbols
from logger import logger
from processor import ProgramProcessor


def process_input(file: str, where_to: Path | None=None) -> None:
    classname = Path(file).name.split('.')[0]
    goto, symbol = capture(classname)
    functions = parse_functions(goto)
    symbols = parse_symbols(symbol)

    processor = ProgramProcessor(symbols)
    processor.process(functions)
    
    if where_to:
        processor.write_to_file(where_to)
    else:
        processor.write_to_stdout()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        logger.warning(f'Expected argument with path to the java file. Got {sys.argv}')
        sys.exit(1)

    process_input(sys.argv[1])
