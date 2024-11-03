import json
import os
import shutil
import subprocess

from pathlib import Path
from subprocess import CompletedProcess
from typing import Literal

from structs import GotoFunction
from structs.symbol_table import SymbolTable
from logger import logger


ROOT = Path('/home/miro/sbapr/playground')

JBMC = ROOT / 'src' / 'jbmc'
SOURCE_CODES = ROOT / 'tests'
MAIN_PATH = ROOT / 'src'


class Capture:
    def __init__(self, filename: str, mode: Literal['goto', 'symbol']='goto') -> None:
        self._filename = filename
        self._mode = mode
        self._json = self._capture(json_ui=True)
        self._normal = self._capture(json_ui=False)

    def _write_into_file(self, content: str, json_ui: bool) -> None:
        name = f'{self._mode}.{"json" if json_ui else "txt"}'
        path = Path.cwd() / 'capture' / name
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
    os.chdir(SOURCE_CODES)
    pure_name = path.name.split('.')[0]

    logger.info('compiling java files')
    compilation = subprocess.run(['javac', f'{pure_name}.java'])

    if compilation.returncode != 0:
        raise RuntimeError('compilation failed')

    logger.info('moving compiled files')
    shutil.move(SOURCE_CODES / f'{pure_name}.class', MAIN_PATH)


def capture(filename: str) -> tuple[Capture, Capture]:
    logger.info(f'checking existence of provided file {filename}')

    path = MAIN_PATH / Path(f'{filename}.class')
    if path.exists():
        path.unlink()

    compile(path)

    logger.info('capturing jbmc output')
    os.chdir('/home/miro/sbapr/playground/src')

    goto = Capture(filename, mode='goto')
    symbol = Capture(filename, mode='symbol')

    return goto, symbol


def get_functions(capture: Capture) -> dict:
    for d in capture.get_json():
        if 'functions' in d:
            return d['functions']

    raise KeyError('Functions not in input')


def parse_functions(capture: Capture) -> list[GotoFunction]:
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
