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
    width: Optional[Irep]

    @staticmethod
    def build(obj: dict[str, Any]) -> Irep:
        keywords = {'value', 'identifier', 'size', 'component_name', 
                    'statement', 'type', 'width'}

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
