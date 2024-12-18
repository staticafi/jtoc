from __future__ import annotations
from enum import Enum
from typing import Any


class Types(Enum):
    SignedBitVector = 'signedbv'
    UnsignedBitVector = 'unsignedbv'
    FloatBitVector = 'floatbv'
    Boolean = 'bool'
    Empty = 'empty'
    StructTag = 'struct_tag'
    String = 'string'
    Pointer = 'pointer'
    Array = 'array'
    Other = 'other'

    @staticmethod
    def from_type_id(type_id: str) -> Types:
        if type_id == 'c_bool':
            return Types.Boolean
        
        if type_id not in {type_.value for type_ in Types}:
            return Types.Other

        return Types(type_id)
    
    def is_recursive(self) -> bool:
        return self == Types.Array or self == Types.Pointer

    def has_width(self) -> bool:
        return self in {
            Types.SignedBitVector,
            Types.UnsignedBitVector,
            Types.FloatBitVector,
            Types.Array
        }


class Type:
    def __init__(self, type_irep: dict[str, Any]) -> None:
        self._type: Types = self._get_current_type(type_irep)
        self.inside: Type | None = self._get_inside(type_irep)
        self.width: int = self._get_width(type_irep)
        self.raw_name: str | None = self._get_raw_name(type_irep)

    def __eq__(self, other: str) -> bool:
        if not isinstance(other, str):
            return False
        
        if self.is_array():
            return self.get_array_elem_type() == other

        return self.to_string() == other

    def is_pointer(self) -> bool:
        return self._type == Types.Pointer

    def is_array(self) -> bool:
        return self._type == Types.Array

    def is_struct(self) -> bool:
        return self._type == Types.StructTag

    def get_array_elem_type(self) -> str:
        return self.inside.to_string()

    def to_string(self) -> str:
        if self._type == Types.SignedBitVector:
            ints = {
                8: 'signed char',
                16: 'short int',
                32: 'int',
                64: 'long long int'
            }

            return ints[self.width]

        if self._type == Types.UnsignedBitVector:
            uints = {
                8: 'unsigned char',
                16: 'unsigned short int',
                32: 'unsigned int',
                64: 'unsigned long long int'
            }

            return uints[self.width]

        if self._type == Types.FloatBitVector:
            return 'float' if self.width == 32 else 'double'

        if self._type == Types.Boolean:
            return 'bool'

        if self._type == Types.Empty:
            return 'void'
        
        if self._type == Types.String:
            return 'const char *'

        if self._type == Types.Pointer:
            return f'{self.inside.to_string()} *'

        if self._type == Types.StructTag:
            return f'struct {self.raw_name}'
        
        if self._type == Types.Array:
            return f'{self.inside.to_string()}[{self.width}]'
        
        if self._type == Types.Other:
            return self.raw_name

    def _get_current_type(self, irep: dict[str, Any]) -> Types:
        type_info = irep
        if irep['id'] in {'symbol', 'parameter'}:
            type_info = irep['namedSub']['type']

        return Types.from_type_id(type_info['id'])

    def _get_width(self, irep: dict[str, Any]) -> int:
        if not self._type.has_width():
            return -1

        type_info = irep
        if irep['id'] in {'symbol', 'parameter'}:
            type_info = irep['namedSub']['type']

        if self._type == Types.Array:
            if type_info['namedSub']['size']['id'] == 'infinity':
                return -1

            return int(type_info['namedSub']['size']['namedSub']['value']['id'], 16)

        return int(type_info['namedSub']['width']['id'])

    def _get_inside(self, irep: dict[str, Any]) -> Type | None:
        if not self._type.is_recursive():
            return None

        type_info = irep
        if irep['id'] in {'symbol', 'parameter'}:
            type_info = irep['namedSub']['type']

        return Type(type_info['sub'][0])

    def _get_raw_name(self, irep: dict[str, Any]) -> str | None:
        if self._type == Types.StructTag:
            return irep['namedSub']['identifier']['id']

        if self._type == Types.Other:
            return irep['id']
        
        return None

