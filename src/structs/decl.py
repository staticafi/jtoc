from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from logger import logger
from structs.irep import Irep
from structs.meta import Instruction, GotoInstruction


@dataclass
class Decl(GotoInstruction):
    var_type: str

    @staticmethod
    def build(instruction: dict[str, Any]) -> Decl:
        ops = instruction['operands']
        if not isinstance(ops, list) or len(ops) != 1:
            logger.warning(f'invalid operand list for DECL: {instruction["operands"]}')
            return
    
        irep = Irep.build(ops[0])

        target = None
        if 'target' in instruction:
            target = int(instruction['target'])

        kwargs = {
            'name': irep.named_sub.identifier.id,
            'instruction': Instruction.DECL,
            'ireps': [irep],
            'source_location': None,
            'target': target,
            'var_type': irep.named_sub.type._type
        }
        
        return Decl(**kwargs)
