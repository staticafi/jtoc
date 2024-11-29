from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

from static import logger
from structs.instruction import Instruction
from structs.irep import Irep
from structs.source_info import SourceInfo


@dataclass
class GotoInstruction:
    name: str
    instruction: Instruction
    ireps: list[Irep]
    source_location: Optional[SourceInfo]
    target: Optional[int]

    @property
    def label(self) -> Optional[int]:
        return self.target

    @staticmethod
    def build(instruction: dict[str, Any]) -> GotoInstruction:
        parsed_instruction = Instruction[instruction['instructionId']]
        logger.debug(f'building {parsed_instruction.name} Instruction object')

        target = None
        if 'target' in instruction:
            target = int(instruction['target'])

        ireps: list[Irep] = []
        if 'guard' in instruction:
            ireps.append(Irep.build(instruction['guard']))
        elif 'operands' in instruction:
            for operand in instruction['operands']:
                ireps.append(Irep.build(operand))

        kwargs = {
            'name': instruction['instruction'],
            'instruction': parsed_instruction,
            'ireps': ireps,
            'source_location': None,
            'target': target
        }
        
        return GotoInstruction(**kwargs)