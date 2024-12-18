from __future__ import annotations
import re

from dataclasses import dataclass

from processing.passes.program_pass import ProgramPass
from processing.program_parts.complex import ProgramStruct
from static import JTOC_LIBRARY_STRUCTS
from structs.symbol_table import SymbolTable


@dataclass
class Node:
    unified_name: str
    edges: list[Node]


class OrderStructsPass(ProgramPass):
    def __init__(self, structs: list[ProgramStruct]) -> None:
        self.structs = structs
        self.edges: dict[str, set[str]] = {}

    def _create_edges(self, struct: ProgramStruct) -> None:
        self.edges[struct.unified_name] = set()

        for decl in struct.body:
            match = re.search(r'struct ([\w\d_]*)', decl.var_type)
            if not match:
                continue

            self.edges[struct.unified_name].add(match.group(1))

    def _dfs(self, node: str, visited: set[str], stack: list[str]) -> None:
        if node in visited:
            return

        visited.add(node)
        for neighbor in self.edges[node]:
            self._dfs(neighbor, visited, stack)
        stack.append(node)

    def _get_topological_order(self) -> list[ProgramStruct]:
        visited = set()
        stack = []

        for node in self.edges:
            self._dfs(node, visited, stack)

        structs: dict[str, ProgramStruct] = {struct.unified_name: struct for struct in self.structs}
        return [structs[name] for name in stack if name in structs]

    def do_the_pass(self) -> None:
        for s in self.structs:
            self._create_edges(s)
        
        for jtoc_struct in JTOC_LIBRARY_STRUCTS:
            self.edges[jtoc_struct] = set()

        new_order = self._get_topological_order()
        self.structs.clear()
        self.structs.extend(new_order)