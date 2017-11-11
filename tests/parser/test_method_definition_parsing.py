import pytest

from tests.infrastructure.test_utils import parse_local
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.method_definition import MethodDefinition
from thinglang.parser.errors import VectorReductionError


def validate_method_definition(node, name, expected_arguments=(), return_type=None):
    assert isinstance(node, MethodDefinition)
    assert node.name == (name if isinstance(name, Identifier) else Identifier(name))
    assert node.return_type == return_type
    for actual_argument, expected_argument in zip(node.arguments, expected_arguments):
        assert actual_argument.value == expected_argument[0]
        assert actual_argument.type.value == expected_argument[1]


def test_simple_method_definition():
    method = parse_local("does say_hello")
    validate_method_definition(method, 'say_hello')


def test_simple_constructor_definition():
    method = parse_local("setup")
    parse_local("thing container").attach(method)
    validate_method_definition(method, Identifier.constructor(), return_type=Identifier('container'))


def test_constructor_arguments():
    method = parse_local("setup with text name, number age")
    parse_local("thing container").attach(method)
    validate_method_definition(method, Identifier.constructor(), [('name', 'text'), ('age', 'number')], Identifier('container'))


def test_method_definition_return_type():
    method = parse_local("does compute returns number")
    validate_method_definition(method, 'compute', (), Identifier('number'))


def test_single_argument_method_definition():
    method = parse_local("does say_hello with text message")
    validate_method_definition(method, 'say_hello', [('message', 'text')])


def test_multiple_argument_method_definition():
    method = parse_local("does say_hello with text message, number count")
    validate_method_definition(method, 'say_hello', [('message', 'text'), ('count', 'number')])


def test_combined_method_definition():
    method = parse_local("does say_hello with text message, number count returns text")
    validate_method_definition(method, 'say_hello', [('message', 'text'), ('count', 'number')], Identifier('text'))


def test_method_definition_argument_invalid_syntax():
    with pytest.raises(VectorReductionError):
        parse_local("does say_hello with text")

    with pytest.raises(VectorReductionError):
        parse_local("does say_hello with text name, number")

    with pytest.raises(VectorReductionError):
        parse_local("does say_hello with text name age")

    with pytest.raises(VectorReductionError):
        parse_local("does say_hello with text number , , age")

    with pytest.raises(VectorReductionError):
        parse_local("does say_hello with number, age")

    with pytest.raises(VectorReductionError):
        parse_local("does say_hello with number 2")

    with pytest.raises(VectorReductionError):
        parse_local("does say_hello returns number returns text")

    with pytest.raises(VectorReductionError):
        parse_local("does say_hello returns number with number a")

