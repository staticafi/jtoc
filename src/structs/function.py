from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from static import logger
from structs.assign import Assign
from structs.call import Call
from structs.decl import Decl
from structs.goto import Goto
from structs.instruction import Instruction
from structs.meta import GotoInstruction


@dataclass
class GotoFunction:
    name: str
    instructions: list[GotoInstruction]
    is_internal: bool
    is_body_available: bool
    signature: list[str]  # list of identifiers

    @staticmethod
    def construct_instruction(instr: dict[str, Any]) -> GotoInstruction:
        instructions: dict[Instruction, GotoInstruction] = {
            Instruction.DECL: Decl,
            Instruction.ASSIGN: Assign,
            Instruction.GOTO: Goto,
            Instruction.FUNCTION_CALL: Call,
        }

        instr_enum = Instruction[instr['instructionId']]
        if instr_enum in instructions:
            return instructions[instr_enum].build(instr)
        
        return GotoInstruction.build(instr)

    @staticmethod
    def build(func: dict[str, Any]) -> GotoFunction:
        keys = {'instructions', 'isBodyAvailable', 'isInternal', 'name', 'signature'}
        if set(func.keys()) != keys:
            logger.info(f'function does not have expected keys. Got {set(func.keys())}, expected {keys}')
        
        instructions = [GotoFunction.construct_instruction(instr) for instr in func['instructions']]

        kwargs = {
            'name': func['name'],
            'is_internal': bool(func['isInternal']),
            'is_body_available': bool(func['isBodyAvailable']),
            'instructions': instructions,
            'signature': [s['id'] for s in func['signature']]
        }
        return GotoFunction(**kwargs)
    