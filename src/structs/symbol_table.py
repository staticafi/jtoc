import re
from typing import Any

from logger import logger
from structs.irep import Irep
from structs.type import Type


class SymbolTable:
    def __init__(self, symbols: dict[str, Any]) -> None:
        self._symbols: dict[str, Any] = symbols
        self._func_names: dict[str, str] = {}

    def get_symbol_type(self, symbol: str) -> Type:
        if symbol not in self._symbols:
            raise KeyError(f'{symbol} not in self._symbols')

        symbol_type = self._symbols[symbol]['type']
        return Type(symbol_type)
    
    def get_classes(self) -> list[dict]:
        classes: list[dict] = []
        for symbol in self._symbols.values():
            if not symbol['isType']:
                continue
            classes.append(symbol)

        return classes

    def get_static_variables(self) -> list[str]:
        return [name for name in self._symbols if self._symbols[name]['isStaticLifetime']]

    def get_static_var_value(self, symbol: str) -> Irep:
        return Irep.build(self._symbols[symbol]['value'])
    
    def is_static_symbol(self, symbol: str) -> bool:
        if symbol not in self._symbols:
            return False
        
        return self._symbols[symbol]['isStaticLifetime']
    
    def get_func_name(self, symbol: str) -> str | None:
        return self._func_names.get(symbol)

    def _unify_arg_list(self, matched: str) -> str:
        arg_list: list[str] = []
        end = -1

        for index, char in enumerate(matched):
            if index < end or not char.isupper():
                continue

            if char != 'L':
                arg_list.append(char)
            else:
                end = matched[index:].index(';') + index + 1
                arg_match = re.search(r'L(([\w]+/)*)(\w*);', matched[index:end])
                arg_list.append(arg_match.group(3))
        
        return ''.join(arg_list)

    def _unify_return_type(self, ret: str) -> str:
        if not ret:
            return ret

        ret_match = re.search(r'L(([\w]+/)*)(\w*);', ret)
        if ret_match:
            return ret_match.group(3)
        return ret

    def add_func_name(self, symbol: str) -> None:
        unified_name = self.get_func_name(symbol)
        if unified_name:
            return

        match = re.search(r"(\w*)::((\w*)\.)*([^:()]*){1}:\(([^\)]*)\)(.+)", symbol)
        if not match:
            match = re.search(r"(\w*)::((\w*)\.)*([^:()]*){1}", symbol)
            if not match:
                logger.warning(f'[add_func_name] name of function {symbol} does not confirm to regex')
                return

        class_name, function_name = match.group(3), match.group(4)
        unified_args = ""

        if len(match.groups()) > 4:
            args, return_type = match.group(5), match.group(6)
            unified_args = self._unify_arg_list(args)
            unified_ret = self._unify_return_type(return_type)

        if function_name in {'<clinit>', '<clinit_wrapper>', '<init>'}:
            inside = re.search(r'<([^<>]*)>', function_name).group(1)
            unified_name = f'___{class_name}_{inside}{"_" if unified_args else ""}{unified_args}___'
        else:
            unified_name = f'{function_name}_{class_name}_{unified_args}_{unified_ret}'
            if function_name == 'main' and unified_args == 'String' and unified_ret == 'V':
                unified_name = 'main'

        self._func_names[symbol] = unified_name
        return