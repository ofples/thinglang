import struct

from thinglang.foundation import definitions
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.primitive_type import PrimitiveType


class LexicalBoolean(PrimitiveType):
    """
    The base boolean type.
    """

    TYPE = Identifier('bool')
    PRIMITIVE_ID = definitions.PRIMITIVE_TYPES.index('bool')

    def __init__(self, value, source_ref=None):
        super(LexicalBoolean, self).__init__(value, source_ref)
        self.value = bool(value)

    def serialize(self):
        return struct.pack('<iB', LexicalBoolean.PRIMITIVE_ID, self.value)


class LexicalBooleanTrue(LexicalBoolean):

    def __init__(self, _, source_ref):
        super(LexicalBooleanTrue, self).__init__(True, source_ref)


class LexicalBooleanFalse(LexicalBoolean):

    def __init__(self, _, source_ref):
        super(LexicalBooleanFalse, self).__init__(False, source_ref)
