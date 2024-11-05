from typing import Any


class Type:
    def __init__(self, _type: dict[str, Any]) -> None:
        self._type: str = self.get_type(_type)

    def __str__(self) -> str:
        return self._type

    @staticmethod
    def unify_struct_name(full_name: str) -> str:
        var_name = full_name.split("::")[-1]
        return var_name.replace('.', '_')
    
    def is_pointer(self) -> bool:
        return self._type[-1] == '*'

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
            struct_name = Type.unify_struct_name(type_info['namedSub']['identifier']['id'].replace('.', '_'))
            return f"struct {struct_name}"
        
        if type_info['id'] == 'string':
            return 'const char *'
        # logger.warning(f'unexpected irep type: {type_info["id"]}. {type_info}')
        return "DON'T KNOW YET"

