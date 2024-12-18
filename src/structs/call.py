from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from static import logger
from structs.instruction import Instruction
from structs.irep import Irep
from structs.goto_instruction import GotoInstruction
from structs.type import Type

@dataclass
class FunctionInfo:
    name: str
    return_type: Type
    parameters: list[Type]

    @staticmethod
    def build(info: dict[str, Any]) -> FunctionInfo:
        type_info = info['type']['namedSub']

        params = []
        if 'sub' in type_info['parameters']:
            params = type_info['parameters']['sub']

        kwargs = {
            'name': info['identifier']['id'],
            'return_type': Type(type_info['return_type']),
            'parameters': [Type(p) for p in params]
        }

        return FunctionInfo(**kwargs)


@dataclass
class Call(GotoInstruction):
    func_info: FunctionInfo
    arguments: list[Irep]

    def is_printf(self) -> bool:
        # Currently supports only printf calls
        if not self.func_info.name.startswith('java::java.io.PrintStream.println'):
            return False
        if len(self.arguments) != 2:
            return False
        stream = self.arguments[0]
        return stream.id == 'symbol' or \
            stream.named_sub.identifier.id == 'java::java.lang.System.out'

    @staticmethod
    def build(instruction: dict[str, Any]) -> Call:
        logger.debug('building Call Instruction object')

        ops = instruction['operands']
        if not isinstance(ops, list) or len(ops) != 3:
            logger.warning(f'invalid operand list for FUNCTION_CALL: {instruction["operands"]}')
            return
    
        func_info = FunctionInfo.build(ops[1]['namedSub'])
        args = []
        if 'sub' in ops[2]:
            args = [Irep.build(arg) for arg in ops[2]['sub']]

        target = None
        if 'target' in instruction:
            target = int(instruction['target'])

        kwargs = {
            'name': func_info.name,
            'instruction': Instruction.FUNCTION_CALL,
            'ireps': [],
            'target': target,
            'func_info': func_info,
            'arguments': args
        }
        
        return Call(**kwargs)
