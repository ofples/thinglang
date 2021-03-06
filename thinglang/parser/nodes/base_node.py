import itertools

from thinglang.utils import collection_utils
from thinglang.utils.mixins import ParsingMixin
from thinglang.utils.source_context import SourceReference


class BaseNode(ParsingMixin):
    """
    The base AST node
    """

    STATIC = False

    def __init__(self, tokens):
        self.children = []
        self.indent = 0
        self.value = None
        self.parent = None

        self.source_ref = SourceReference.combine(collection_utils.flatten(tokens))

    def attach(self, child):
        """
        Attach a child to this node
        """
        self.children.append(child)
        child.parent = self

    def remove(self):
        """
        Remove this node from the AST
        """
        self.parent.children.remove(self)
        self.parent = None

    def replace(self, node):
        node.parent = self.parent
        siblings = self.parent.children
        siblings[siblings.index(self)] = node

    def previous_sibling(self):
        siblings = self.parent.children
        return siblings[siblings.index(self) - 1]

    def next_siblings(self):
        """
        Returns this node's siblings, starting after this node
        :return:
        """
        siblings = self.parent.children
        return siblings[siblings.index(self) + 1:]

    def ascend(self, target_type):
        node = self
        while node.parent:
            node = node.parent
            if isinstance(node, target_type):
                return node


    @collection_utils.drain()
    def siblings_while(self, predicate):
        """
        Emits this node's siblings (starting after the node) until predicate returns true
        """
        return itertools.takewhile(predicate, self.next_siblings())

    def finalize(self):
        """
        Calls the finalize method on this nodes siblings
        """
        for x in self.children:
            x.finalize()

    def compile(self, context):
        """
        Recursively compile this nodes children
        """
        for child in self.children:
            child.compile(context)

        if not self.children:
            raise Exception(f'A {type(self).__name__} cannot have an empty body (at {self.source_ref})')

    def deriving_from(self, node):
        """
        Override the source reference for this node by providing the source node
        """
        self.parent = node.parent
        self.source_ref = node.source_ref
        return self

    def tree(self, depth=1):
        """
        Prints this node and its children in a tree-like format
        """
        separator = ('\n' if self.children else '') + ('\t' * depth)
        return '<L{}> {}({}){}{}'.format(self.source_ref.line_number if self.source_ref else "?",
                                         type(self).__name__,
                                         self,
                                         separator,
                                         separator.join(child.tree(depth=depth + 1) for child in self.children))

    @property
    def descendants(self):
        for child in self.children:
            yield child
            yield from child.descendants
