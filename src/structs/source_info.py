from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

from logger import logger

@dataclass
class SourceInfo:
    bytecode_index: Optional[int]
    line: int
    file: str
    function: str

    @staticmethod
    def build(info: dict[str, Any]) -> SourceInfo:
        optional_keywords = {'bytecodeIndex'}
        keywords = {'file', 'function', 'line'}

        if set(info.keys()) not in [keywords, keywords | optional_keywords]:
            logger.info(f'Non matching info. Expected {keywords}. Got {set(info.keys())}')
            return None

        index = None
        if 'bytecodeIndex' in info:
            index = int(info['bytecodeIndex'])

        kwargs = {
            'bytecode_index': index,
            'line': int(info['line']),
            'file': info['file'],
            'function': info['function']
        }

        return SourceInfo(**kwargs)