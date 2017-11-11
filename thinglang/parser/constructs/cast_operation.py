from thinglang.compiler.context import CompilationContext
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.values.access import Access
from thinglang.parser.values.method_call import MethodCall


class CastOperation(object):

    @staticmethod
    def create(source: Identifier, destination: Identifier) -> MethodCall:
        return MethodCall(Access([source, Identifier('convert_') + destination]), MethodCall.STACK_ARGS)