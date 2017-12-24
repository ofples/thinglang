from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.context import CompilationContext
from thinglang.foundation.definitions import INTERNAL_TYPE_ORDERING
from thinglang.lexer.definitions.tags import LexicalInheritanceTag
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationThing
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.member_definition import MemberDefinition
from thinglang.parser.definitions.method_definition import MethodDefinition
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule


class ThingDefinition(BaseNode):
    """
    Defines a thing, also known as a class
    """

    def __init__(self, name, extends=None, generics=None):
        super(ThingDefinition, self).__init__([name, extends, generics])
        self.name, self.extends, self.generics = name, extends, generics

    def __repr__(self):
        return f'thing {self.name}'

    def compile(self, context: CompilationContext):
        symbol_map = context.symbols[self.name]
        for method in self.methods:
            buffer = CompilationBuffer(context.symbols, method.locals)
            method.compile(buffer)
            context.add((symbol_map.index, symbol_map[method.name].index), method, buffer)

    def finalize(self):
        super().finalize()

        if Identifier.constructor() not in self.names:  # Add implicit constructor
            self.children.insert(0, MethodDefinition.empty_constructor(self))

        if self.extends and self.extends.untyped in INTERNAL_TYPE_ORDERING:
            self.children.insert(0, MemberDefinition(Identifier.super(), self.extends).deriving_from(self))

    @property
    def members(self):
        return [x for x in self.children if isinstance(x, MemberDefinition)]

    @property
    def methods(self):
        return [x for x in self.children if isinstance(x, MethodDefinition)]

    @property
    def names(self):
        return [x.name for x in self.members + self.methods]

    def slots(self, context):
        return sum(len(container.members) for container in context.symbols.inheritance(self))

    @staticmethod
    @ParserRule.mark
    def base_definition(_: LexicalDeclarationThing, name: Identifier):
        return ThingDefinition(name)

    @staticmethod
    @ParserRule.mark
    def define_generic(thing: 'ThingDefinition', generics: 'TypeVector'):
        thing.generics = generics
        return thing

    @staticmethod
    @ParserRule.mark
    def define_inheritance(thing: 'ThingDefinition', _: LexicalInheritanceTag, extends: Identifier):
        thing.extends = extends
        return thing


