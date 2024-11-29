from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from static import logger
from structs.irep import Irep
from structs.meta import Instruction, GotoInstruction
from structs.type import Type


@dataclass
class Decl(GotoInstruction):
    var_type: Type

    @staticmethod
    def build(instruction: dict[str, Any]) -> Decl:
        logger.debug('building Decl Instruction object')

        ops = instruction['operands']
        if not isinstance(ops, list) or len(ops) != 1:
            logger.warning(f'invalid operand list for DECL: {instruction["operands"]}')
            return
    
        irep = Irep.build(ops[0])

        target = None
        if 'target' in instruction:
            target = int(instruction['target'])

        assert irep.named_sub.type is not None

        kwargs = {
            'name': irep.named_sub.identifier.id,
            'instruction': Instruction.DECL,
            'ireps': [irep],
            'source_location': None,
            'target': target,
            'var_type': irep.named_sub.type
        }
        
        return Decl(**kwargs)
