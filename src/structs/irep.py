from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

from logger import logger


class Type:
    def __init__(self, _type: dict[str, Any]) -> None:
        self._type: str = self.get_type(_type)

    def __str__(self) -> str:
        return self._type

    def get_type(self, irep: dict[str, Any]) -> str:
        type_info = irep
        if irep['id'] in {'symbol', 'parameter'}:
            type_info = irep['namedSub']['type']

        if type_info['id'] == 'signedbv':
            ints = {
                8: 'signed char',
                16: 'short int',
                32: 'int',
                64: 'long long int'
            }

            width = int(type_info['namedSub']['width']['id'])
            return ints[width]

        if type_info['id'] == 'unsignedbv':
            uints = {
                8: 'unsigned char',
                16: 'unsigned short int',
                32: 'unsigned int',
                64: 'unsigned long long int'
            }

            width = int(type_info['namedSub']['width']['id'])
            return uints[width]

        if type_info['id'] == 'floatbv':
            width = int(type_info['namedSub']['width']['id'])
            if width == 32:
                return 'float'
            return 'double'

        if type_info['id'] in ('c_bool', 'bool'):
            # TODO #include <stdbool.h>
            return 'bool'

        if type_info['id'] == 'empty':
            return 'void'

        if type_info['id'] == 'pointer':
            return f"{self.get_type(type_info['sub'][0])} *"

        if type_info['id'] == 'struct_tag':
            return f"struct {type_info['namedSub']['identifier']['id']}"
        
        if type_info['id'] == 'string':
            return 'const char *'
        # logger.warning(f'unexpected irep type: {type_info["id"]}. {type_info}')
        return "DON'T KNOW YET"


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
