import struct

from thinglang.builtins import TT_NUMBER
from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.tokens import LexicalToken, LexicalBinaryOperation


class LexicalNumericalValue(LexicalToken, ValueType):

    STATIC = True

    def __init__(self, value):
        super(LexicalNumericalValue, self).__init__(value)
        self.value = int(value)

    def evaluate(self, _):
        return self.value

    def describe(self):
        return self.value

    def serialize(self):
        return struct.pack('<ii', -2, self.value)

    @staticmethod
    def resolve_type():
        return TT_NUMBER


class FirstOrderLexicalBinaryOperation(LexicalBinaryOperation):  # addition, subtraction
    pass


class SecondOrderLexicalBinaryOperation(LexicalBinaryOperation):  # division, multiplication
    pass


class LexicalAddition(FirstOrderLexicalBinaryOperation):
    pass


class LexicalSubtraction(FirstOrderLexicalBinaryOperation):
    pass


class LexicalMultiplication(SecondOrderLexicalBinaryOperation):
    pass


class LexicalDivision(SecondOrderLexicalBinaryOperation):
    pass
