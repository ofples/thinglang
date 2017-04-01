from thinglang.utils.type_descriptors import ValueType, ReplaceableArguments
from thinglang.lexer.tokens.arithmetic import LexicalAddition, LexicalMultiplication, LexicalSubtraction, \
    LexicalDivision
from thinglang.lexer.tokens.logic import LexicalEquality, LexicalInequality, LexicalGreaterThan, LexicalLessThan
from thinglang.parser.symbols import BaseSymbol


class ArithmeticOperation(BaseSymbol, ValueType, ReplaceableArguments):
    OPERATIONS = {
        LexicalAddition: lambda lhs, rhs: lhs + rhs,
        LexicalMultiplication: lambda lhs, rhs: lhs * rhs,
        LexicalSubtraction: lambda lhs, rhs: lhs - rhs,
        LexicalDivision: lambda lhs, rhs: lhs / rhs,
        LexicalEquality: lambda lhs, rhs: lhs == rhs,
        LexicalInequality: lambda lhs, rhs: lhs != rhs,
        LexicalGreaterThan: lambda lhs, rhs: lhs > rhs,
        LexicalLessThan: lambda lhs, rhs: lhs < rhs
    }

    def __init__(self, slice):
        super(ArithmeticOperation, self).__init__(slice)
        self.arguments = [slice[0], slice[2]]
        self.operator = type(slice[1])

    def evaluate(self, resolver):
        return self.OPERATIONS[self.operator](self[0].evaluate(resolver), self[1].evaluate(resolver))

    def describe(self):
        return '|{} {} {}|'.format(self[0], self.operator, self[1])

    def __getitem__(self, item):
        return self.arguments[item]