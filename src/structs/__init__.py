from pathlib import Path
import sys

from structs.assign import Assign
from structs.decl import Decl
from structs.goto import Goto
from structs.function import GotoFunction
from structs.irep import Irep
from structs.meta import GotoInstruction, Instruction
from structs.source_info import SourceInfo

__all__ = ['Assign', 'Decl', 'Goto', 'GotoFunction', 'Irep', 'GotoInstruction', 'Instruction', 'SourceInfo']

path = Path().cwd() / 'src'
sys.path.append(str(path.absolute()))