from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from logger import logger
from structs.irep import Irep
from structs.meta import Instruction, GotoInstruction


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

    def get_left_name(self) -> str:
        if self.left.id == 'member':
            return self.left.named_sub.component_name.id
        if self.left.id == 'dereference':
            return self.left.sub[0].named_sub.identifier.id
    
        return self.left.named_sub.identifier.id

    @staticmethod
    def build(instruction: dict[str, Any]) -> Assign:
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
            'source_location': None,
            'target': target,
            'left': left,
            'right': right
        }
        
        return Assign(**kwargs)