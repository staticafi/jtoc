import json
import os
import shutil
import subprocess

from pathlib import Path
from subprocess import CompletedProcess
from typing import Literal

from structs import GotoFunction
from structs.symbol_table import SymbolTable
from static import logger, JBMC, COMPILE_DIR, CAPTURE_DIR, TEST_DIR


class Capture:
    def __init__(self, filename: str, mode: Literal['goto', 'symbol']='goto') -> None:
        self._filename = filename
        self._mode = mode

        os.chdir(COMPILE_DIR)
        self._json = self._capture(json_ui=True)
        self._normal = self._capture(json_ui=False)

    def _write_into_file(self, content: str, json_ui: bool) -> None:
        name = f'{self._mode}.{"json" if json_ui else "txt"}'
        path = CAPTURE_DIR / name
        if not path.parent.exists():
            path.parent.mkdir()
        
        with open(path, 'w') as file:
            file.write(content)

    def _capture(self, json_ui: bool=False) -> CompletedProcess[bytes]:
        switch = '--show-goto-functions'
        if self._mode == 'symbol':
            switch = '--show-symbol-table'

        args = [str(JBMC), switch, self._filename]
        if json_ui:
            args = [str(JBMC), switch, '--json-ui', self._filename]

        completed = subprocess.run(args, capture_output=True)
        self._write_into_file(completed.stdout.decode(), json_ui)
        return completed

    def get_json(self) -> dict:
        return json.loads(self._json.stdout.decode())

    def get_normal(self) -> str:
        return self._normal.stdout.decode()


def compile(path: Path) -> None:
    os.chdir(COMPILE_DIR)
    pure_name = path.stem

    logger.info('compiling java files')
    compilation = subprocess.run(['javac', f'{pure_name}.java'])

    if compilation.returncode != 0:
        raise RuntimeError('compilation failed')

    logger.info(f'compilation of file {pure_name}.java succesfull')


def capture(filename: str) -> tuple[Capture, Capture]:
    logger.info(f'checking existence of provided file {filename}')
    if not (TEST_DIR / f'{filename}.java').exists():
        logger.error(f'could not find file {filename} on in directory {TEST_DIR}')
        raise FileNotFoundError(f'{filename} could not be found')

    path = COMPILE_DIR / Path(f'{filename}.java')
    if not path.exists():
        logger.info('moving java files into compile directory')
        shutil.copyfile(TEST_DIR / f'{filename}.java', COMPILE_DIR / f'{filename}.java')

    compile(path)

    logger.info('capturing jbmc output')

    goto = Capture(filename, mode='goto')
    symbol = Capture(filename, mode='symbol')

    return goto, symbol


def get_functions(capture: Capture) -> dict:
    for d in capture.get_json():
        if 'functions' in d:
            return d['functions']

    raise KeyError('Functions not in input')


def parse_functions(capture: Capture) -> list[GotoFunction]:
    logger.info('parsing captured functions')
    functions: list[GotoFunction] = []

    for func in get_functions(capture):
        name: str = func['name']
        if name.startswith('__'):
            continue

        functions.append(GotoFunction.build(func))

    return functions


def parse_symbols(capture: Capture) -> SymbolTable:
    for d in capture.get_json():
        if 'symbolTable' in d:
            return SymbolTable(symbols=d['symbolTable'])

    raise KeyError('Symbol table not in input')
