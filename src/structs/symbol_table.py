from typing import Any

from structs.irep import Type


class SymbolTable:
    def __init__(self, symbols: dict[str, Any]) -> None:
        self._symbols: dict[str, Any] = symbols

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
            