from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from static import logger
from structs.instruction import Instruction
from structs.irep import Irep
from structs.goto_instruction import GotoInstruction


@dataclass
class Goto(GotoInstruction):
    guard: Irep
    target_to: int

    @staticmethod
    def build(instruction: dict[str, Any]) -> Goto:
        logger.debug('building Goto Instruction object')
        
        guard = instruction['guard']
        if not isinstance(guard, dict):
            logger.warning(f'invalid guard for GOTO: {instruction["guard"]}')
            return

        targets = instruction['targetTo']
        if not isinstance(targets, list) or len(targets) != 1:
            logger.warning(f'invalid targetTo for GOTO: {instruction["targetTo"]}')
            return

        target_to = int(targets[0])
        irep = Irep.build(guard)

        target = None
        if 'target' in instruction:
            target = int(instruction['target'])

        kwargs = {
            'name': instruction['instruction'],
            'instruction': Instruction.GOTO,
            'ireps': [irep],
            'target': target,
            'target_to': target_to,
            'guard': irep
        }
        
        return Goto(**kwargs)

    def is_guarded(self) -> bool:
        return not (self.guard.id == 'constant' and \
                    self.guard.named_sub.type._type == 'bool' and \
                    self.guard.named_sub.value.id == 'true')
