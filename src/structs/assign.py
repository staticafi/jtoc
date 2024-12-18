from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from static import logger
from structs.instruction import Instruction
from structs.irep import Irep
from structs.goto_instruction import GotoInstruction


WRAPPER_IDS = {'member', 'dereference'}


@dataclass
class Assign(GotoInstruction):
    left: Irep
    right: Irep

    def is_return(self) -> bool:
        if self.left.id in WRAPPER_IDS:
            return False
        left_name = self.left.named_sub.identifier.id
        return left_name.endswith("#return_value")

    def is_dereference(self) -> bool:
        return self.left.id == 'dereference'

    def get_left_name(self) -> str:
        if self.left.id == 'member':
            return self.left.named_sub.component_name.id
        if self.left.id == 'dereference':
            return ''
    
        return self.left.named_sub.identifier.id

    @staticmethod
    def build(instruction: dict[str, Any]) -> Assign:
        logger.debug('building Assign Instruction object')
        
        ops = instruction['operands']
        if not isinstance(ops, list) or len(ops) != 2:
            logger.warning(f'invalid operand list for ASSIGN: {instruction["operands"]}')
            return
    
        left, right = Irep.build(ops[0]), Irep.build(ops[1])

        target = None
        if 'target' in instruction:
            target = int(instruction['target'])

        kwargs = {
            'name': instruction['instruction'],
            'instruction': Instruction.ASSIGN,
            'ireps': [left, right],
            'target': target,
            'left': left,
            'right': right
        }
        
        return Assign(**kwargs)