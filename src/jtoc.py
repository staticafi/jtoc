import sys

from pathlib import Path

from capture.compiling import parse_functions, capture, parse_symbols, compile, prepare_test_files
from static import COMPILE_DIR, TEST_DIR, logger
from processing.program_processor import ProgramProcessor


def process_input(file: str, where_to: Path | None=None) -> None:
    filepath = TEST_DIR / Path(file)

    prepare_test_files(filepath)
    compile(filepath.stem)
    goto, symbol = capture(filepath.stem)

    functions = parse_functions(goto)
    symbols = parse_symbols(symbol)

    processor = ProgramProcessor(symbols, functions)
    processor.write_to_file(where_to)


def print_help() -> None:
    output = f"""Usage: 
    $ python3 ./jtoc.py <class_name> [<c_file_name>]

    - <class_name> -> the name of the class residing in the file named <class_name>.java
                   -> the file <class_name>.java must be in directory {TEST_DIR.absolute()}
    - <c_file_name> -> optional argument
                    -> name of the C output file that will be stored in directory {COMPILE_DIR.absolute()}
                    -> if it is not provided, the file will printed to stdout
    """
    print(output)


if __name__ == '__main__':
    if len(sys.argv) not in {2, 3}:
        logger.warning('Invalid command.')
        print_help()
        sys.exit(1)

    arg2 = sys.argv[2] if len(sys.argv) == 3 else None
    process_input(sys.argv[1], arg2)
