from tests.infrastructure.test_utils import parse_local
from tests.parser.test_method_call_parsing import validate_method_call
from thinglang.lexer.tokens.arithmetic import LexicalNumericalValue
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.arithmetic import ArithmeticOperation
from thinglang.parser.nodes.base import AssignmentOperation, InlineString
from thinglang.parser.nodes.functions import MethodCall


def validate_assignment(node, type, name, value):
    assert node.implements(AssignmentOperation)
    assert node.name == LexicalIdentifier(name)
    assert node.name.type == (LexicalIdentifier(type) if type else None)
    assert node.intent == (AssignmentOperation.DECELERATION if type else AssignmentOperation.REASSIGNMENT)

    if value in (MethodCall, ArithmeticOperation):
        assert isinstance(node.value, value)


def test_immediate_declarations():
    validate_assignment(parse_local('number a = 5'), 'number', 'a', LexicalNumericalValue(5))
    validate_assignment(parse_local('text a = "hello world!"'), 'text', 'a', InlineString('hello world!'))


def test_immediate_assignments():
    validate_assignment(parse_local('a = 5'), None, 'a', LexicalNumericalValue(5))
    validate_assignment(parse_local('a = "hello world!"'), None, 'a', InlineString('hello world!'))


def test_simple_method_call_value_type():
    assignment = parse_local('number a = number.random()')
    validate_assignment(assignment, 'number', 'a', MethodCall)
    validate_method_call(assignment.value, ['number', 'random'], [])


def test_complex_method_call_value_type():
    assignment = parse_local('number a = distribution.normal(number.random(10), number.random(25))')
    validate_assignment(assignment, 'number', 'a', MethodCall)
    validate_method_call(assignment.value, ['distribution', 'normal'], [[LexicalNumericalValue], [LexicalNumericalValue]])


def test_arithmetic_operation_value_type():
    assignment = parse_local('number a = 2 * (4 + 2) * (3 + 2)')
    validate_assignment(assignment, 'number', 'a', ArithmeticOperation)
    assert assignment.value.evaluate() == 60
