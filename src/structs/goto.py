from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from logger import logger
from structs.irep import Irep
from structs.meta import Instruction, GotoInstruction


@dataclass
class Goto(GotoInstruction):
    guard: Irep
    target_to: int

    @staticmethod
    def build(instruction: dict[str, Any]) -> Goto:
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
            'ireps': [irep],  # maybe duplicate of guard
            'source_location': None,
            'target': target,
            'target_to': target_to,
            'guard': irep
        }
        
        return Goto(**kwargs)

    def is_guarded(self) -> bool:
        return not (self.guard.id == 'constant' and \
                    self.guard.named_sub.type._type == 'bool' and \
                    self.guard.named_sub.value.id == 'true')
