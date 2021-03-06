from thinglang.symbols.argument_selector import ArgumentSelector
from thinglang.symbols.symbol import Symbol


class MergedSymbol(object):
    """
    Managed overloaded symbols for methods.
    Contains mostly proxy functions into the common symbol
    """

    # TODO: check for signature ambiguity - static non-static consistency (note generic fulfillment assertion)

    def __init__(self, symbols):
        self.symbols = symbols

    def serialize(self):
        return [symbol.serialize() for symbol in self.symbols]

    @property
    def common(self):
        return self.symbols[0]

    @property
    def name(self):
        return self.common.name

    @property
    def static(self):
        return self.common.static

    @property
    def kind(self):
        return Symbol.METHOD

    @property
    def type(self):
        assert len(set(symbol.type for symbol in self.symbols)) == 1
        return self.symbols[0].type

    def selector(self, context):
        return ArgumentSelector(self.symbols, context)

    @property
    def convention(self):
        return self.common.convention

    @convention.setter
    def convention(self, convention):
        for symbol in self.symbols:
            symbol.convention = convention

    def is_complete(self, generics: dict) -> bool:
        return all(x.is_complete(generics) for x in self.symbols)
