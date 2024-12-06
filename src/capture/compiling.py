import os
import shutil
import subprocess

from pathlib import Path

from capture.capture import Capture
from structs import GotoFunction
from structs.symbol_table import SymbolTable
from static import logger, COMPILE_DIR, TEST_DIR


def prepare_test_files(filename: str) -> None:
    logger.info(f'checking existence of provided file {filename}')
    if not (TEST_DIR / f'{filename}.java').exists():
        logger.error(f'could not find file {filename} on in directory {TEST_DIR}')
        raise FileNotFoundError(f'{filename} could not be found')

    path = COMPILE_DIR / Path(f'{filename}.java')
    if not path.exists():
        logger.info('moving java files into compile directory')
        shutil.copyfile(TEST_DIR / f'{filename}.java', COMPILE_DIR / f'{filename}.java')


def compile(filename: str) -> None:
    os.chdir(COMPILE_DIR)

    logger.info('compiling java files')
    compilation = subprocess.run(['javac', f'{filename}.java'])

    if compilation.returncode != 0:
        raise RuntimeError('compilation failed')

    logger.info(f'compilation of file {filename}.java succesfull')


def capture(filename: str) -> tuple[Capture, Capture]:
    logger.info('capturing jbmc output')

    goto = Capture(filename, mode='goto')
    symbol = Capture(filename, mode='symbol')

    return goto, symbol


def _get_functions(capture: Capture) -> dict:
    for d in capture.get_json():
        if 'functions' in d:
            return d['functions']

    raise KeyError('Functions not in input')


def parse_functions(capture: Capture) -> list[GotoFunction]:
    logger.info('parsing captured functions')
    functions: list[GotoFunction] = []

    for func in _get_functions(capture):
        functions.append(GotoFunction.build(func))

    return functions


def parse_symbols(capture: Capture) -> SymbolTable:
    for d in capture.get_json():
        if 'symbolTable' in d:
            return SymbolTable(symbols=d['symbolTable'])

    raise KeyError('Symbol table not in input')