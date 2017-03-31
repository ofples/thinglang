from thinglang.lexer.symbols import LexicalBinaryOperation
from thinglang.parser.tokens import BaseToken
from thinglang.parser.tokens.arithmetic import ArithmeticOperation


class ListInitializationPartial(BaseToken):
    def __init__(self, slice):
        super(ListInitializationPartial, self).__init__(slice)
        if len(slice) == 3 and isinstance(slice[1], LexicalBinaryOperation):
            self.value = slice[0].value[:-1] + [ArithmeticOperation([slice[0][-1]] + slice[1:])]
        elif isinstance(slice[0], ListInitializationPartial):
            self.value = slice[0].value + [slice[2]]
        else:
            self.value = [slice[1]]

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]


class ListInitialization(BaseToken):

    def __init__(self, slice=None):
        super(ListInitialization, self).__init__(slice)

        if slice and isinstance(slice[0], ListInitializationPartial):
            self.arguments = slice[0].value
        else:
            self.arguments = []

    def __iter__(self):
        return iter(self.arguments)

    def __len__(self):
        return len(self.arguments)

    def evaluate(self, stack):
        return [value.evaluate(stack) for value in self.arguments]

    def describe(self):
        return self.arguments

    def replace(self, original, replacement):
        self.arguments = [replacement if x is original else x for x in self.arguments]