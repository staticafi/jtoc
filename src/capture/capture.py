import json
import os
import subprocess

from subprocess import CompletedProcess
from typing import Literal

from static import JBMC, COMPILE_DIR


class Capture:
    def __init__(self, filename: str, mode: Literal['goto', 'symbol']='goto') -> None:
        self._filename = filename
        self._mode = mode

        os.chdir(COMPILE_DIR)
        self._json = self._capture(json_ui=True)
        self._normal = self._capture(json_ui=False)

    def _write_into_file(self, content: str, json_ui: bool) -> None:
        name = f'{self._mode}.{"json" if json_ui else "txt"}'
        path = COMPILE_DIR / name
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
