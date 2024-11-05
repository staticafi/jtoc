from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

from structs.type import Type

@dataclass
class Irep:
    id: str
    named_sub: Optional[Irep]
    sub: Optional[list[Irep]]
    value: Optional[Irep]
    identifier: Optional[Irep]
    size: Optional[Irep]
    component_name: Optional[Irep]
    statement: Optional[Irep]
    type: Optional[Type]
    is_nondet_nullable: Optional[Irep]
    java_member_access: Optional[Irep]
    java_array_access: Optional[Irep]
    mode: Optional[Irep]
    width: Optional[Irep]

    @staticmethod
    def build(obj: dict[str, Any]) -> Irep:
        keywords = {'value', 'identifier', 'size', 'component_name', 
                    'statement', 'type', 'is_nondet_nullable', 
                    'java_member_access', 'java_array_access', 'mode', 'width'}

        kwargs: dict[str, Any] = {
            'id': obj.get('id', 'NOT INCLUDED'),
            'named_sub': None,
            'sub': None,
            'value': None,
            'identifier': None,
            'size': None,
            'component_name': None,
            'statement': None,
            'type': None,
            'is_nondet_nullable': None,
            'java_member_access': None,
            'java_array_access': None,
            'mode': None, 
            'width': None
        }

        if 'sub' in obj:
            if isinstance(obj['sub'], list):
                kwargs['sub'] = [Irep.build(elem) for elem in obj['sub']]
            else:
                kwargs['sub'] = [Irep.build(obj['sub'])]
        
        if 'namedSub' in obj:
            kwargs['named_sub'] = Irep.build(obj['namedSub'])

        for arg in keywords:
            if arg not in obj:
                continue

            if arg == 'type':
                kwargs[arg] = Type(obj[arg])
            else:
                kwargs[arg] = Irep.build(obj[arg])

        return Irep(**kwargs)

    def get_keys(self) -> set[str]:
        return {attr for attr in dir(self) if getattr(self, attr) is not None and not attr.startswith('__') and attr not in {'build', 'as_json', 'get_keys'}}
