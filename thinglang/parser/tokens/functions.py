from thinglang.common import ObtainableValue
from thinglang.lexer.symbols.base import LexicalIdentifier
from thinglang.parser.tokens import BaseToken, DefinitionPairToken


class Access(BaseToken):
    def __init__(self, slice):
        super(Access, self).__init__(slice)
        self.target = [x.value for x in slice if isinstance(x, LexicalIdentifier)]

    def describe(self):
        return '.'.join(self.target)

class ArgumentListPartial(BaseToken):
    def __init__(self, slice):
        super(ArgumentListPartial, self).__init__(slice)
        if isinstance(slice[0], ArgumentListPartial):
            self.value = slice[0].value + [slice[2]]
        else:
            self.value = [slice[1]]


class ArgumentList(BaseToken):
    def __init__(self, slice):
        super(ArgumentList, self).__init__(slice)
        if isinstance(slice[0], ArgumentListPartial):
            self.arguments = slice[0].value
        else:
            self.arguments = []

    def __iter__(self):
        return iter(self.arguments)

    def evaluate(self, stack):
        return [value.evaluate(stack) for value in self.arguments]

    def describe(self):
        return self.arguments


class MethodCall(BaseToken, ObtainableValue):
    def __init__(self, slice):
        super(MethodCall, self).__init__(slice)
        self.target, self.arguments = slice

        if not self.arguments:
            self.arguments = []

    def describe(self):
        return 'target={}, args={}'.format(self.target, self.arguments)


class ReturnStatement(DefinitionPairToken):
    def __init__(self, slice):
        super().__init__(slice)
        self.value = slice[1]
