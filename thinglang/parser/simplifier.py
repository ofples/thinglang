from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols import Transient
from thinglang.parser.symbols.arithmetic import ArithmeticOperation
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.functions import MethodCall, ReturnStatement
from thinglang.parser.symbols.types import ArrayInitialization, CastOperation

OBTAINABLE_VALUES = MethodCall, ArithmeticOperation, ArrayInitialization, CastOperation


def simplify(tree):
    while unwrap_returns(tree):
        pass

    for method_call in tree.find(lambda x: isinstance(getattr(x, 'value', None), OBTAINABLE_VALUES)):
        reduce_method_calls(method_call.value, method_call)

    return tree


def unwrap_returns(tree):
    had_change = False

    for child in set(tree.find(lambda x: isinstance(x, ReturnStatement) and isinstance(x.value, OBTAINABLE_VALUES))):
        id, assignment = create_transient(child.value, child)
        siblings = child.parent.children
        idx = siblings.index(child)

        siblings[idx:idx + 1] = [assignment, ReturnStatement([None, id]).contextify(child.parent)]
        had_change = True

    return had_change


def reduce_method_calls(method_call, node, parent_call=None):
    if not isinstance(method_call, OBTAINABLE_VALUES):
        return
    for argument in method_call.arguments:
        if isinstance(argument, (MethodCall, CastOperation)):
            reduce_method_calls(argument, node, parent_call=method_call)
        if isinstance(argument, ArithmeticOperation):
            for x in argument.arguments:
                reduce_method_calls(x, node, parent_call=argument)

    if parent_call is not None:
        id, assignment = create_transient(method_call, node)
        node.insert_before(assignment)
        parent_call.replace(method_call, id)


def is_compound(node):
    if not node:
        return False
    return (isinstance(node, MethodCall) and any(isinstance(arg, MethodCall) for arg in node.arguments.value)) or \
           (isinstance(node, AssignmentOperation) and is_compound(node.value))


def create_transient(value, parent):
    local_id = Transient().contextify(parent.context)
    return local_id, AssignmentOperation([None, local_id, None, value]).contextify(parent.parent)
