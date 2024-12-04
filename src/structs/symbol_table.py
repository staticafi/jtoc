from __future__ import annotations

import re

from dataclasses import dataclass
from typing import Any

from static import logger
from structs.irep import Irep
from structs.type import Type


@dataclass
class SymbolMatch:
    class_name: str
    function_name: str
    args: str | None
    return_type: str | None

    @staticmethod
    def match_symbol(symbol: str) -> SymbolMatch | None:
        last_part = symbol.split('$')[-1].split('::')[-1]
        match = re.search(r"(([\w\d\[\]]+\.)*)([<>\w\d\[\]]*)(:\(([^\)]*)\)(.+))?", last_part)
        if match:
            c_name = match.group(1).replace('[', '__').replace(']', '__').replace('.', '_')
            f_name = f'lambda_{match.group(3)}' if match.group(3).isdigit() else match.group(3)
            args = match.group(5)
            return_type = match.group(6)

            return SymbolMatch(class_name=c_name, function_name=f_name, args=args, return_type=return_type)

        logger.warning(f'[add_func_name] name of function {symbol} does not confirm to any regex')
        return None


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

    def get_func_return_type(self, symbol: str) -> Type | None:
        irep = self._symbols[symbol]['type']
        if 'return_type' not in irep:
            return None

        return Type(irep['return_type'])

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

        match = SymbolMatch.match_symbol(symbol)
        unified_args = ''
        unified_ret = ''

        if match.args:
            unified_args = self._unify_arg_list(match.args)
        if match.return_type:
            unified_ret = self._unify_return_type(match.return_type)

        if match.function_name in {'<clinit>', '<clinit_wrapper>', '<init>'}:
            inside = re.search(r'<([^<>]*)>', match.function_name).group(1)
            unified_name = f'___{match.class_name}_{inside}{"_" if unified_args else ""}{unified_args}___'
        else:
            unified_name = f'{match.function_name}_{match.class_name}_{unified_args}_{unified_ret}'
            if match.function_name == 'main' and unified_args == 'String' and unified_ret == 'V':
                unified_name = 'main'

        self._func_names[symbol] = unified_name
        return

    def _replace_with_underscore(self, symbol: str) -> str:
        chars: list[str] = []
        for char in symbol:
            new_char = char
            if char in '[].()/:#;':
                new_char = '_'
            chars.append(new_char)

        return ''.join(chars)

    def unify_symbol_name(self, s: str) -> str:
        symbol = s
        if s.startswith('java::'):
            symbol = s[6:]

        if self.is_static_symbol(s):
            last_section = symbol.split('$')[-1]

            symbol_name = self._replace_with_underscore(last_section)
            if last_section.startswith('@'):
                return f'___{symbol_name[1:]}___'

            return symbol_name

        last_section = symbol.split('$')[-1]
        last_part = last_section.split('::')[-1]
        var_name = self._replace_with_underscore(last_part)

        if var_name.startswith('@'):
            return f'___{var_name[1:].replace(".", "_")}___'
        if var_name[0] in '0123456789':
            if 'lambda' in symbol:
                return f'lambda_{var_name}'
            return f'local_{var_name}'
        return var_name.replace('.', '_')

    @staticmethod
    def unify_label(label_num: int) -> str:
        return f'label{label_num}'

    def unify_func_name(self, func_name: str) -> str:
        self.add_func_name(func_name)
        return self.get_func_name(func_name)
