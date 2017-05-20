import struct

from thinglang.compiler.opcodes import OPCODES
from thinglang.utils.tree_utils import TreeTraversal, inspects


class BytecodeSymbols(object):

    @classmethod
    def push_static(cls, id):
        return struct.pack('<BI', OPCODES['PUSH_STATIC'], id)

    @classmethod
    def call(cls, thing, idx):
        return struct.pack('<BII', OPCODES['CALL'], thing, idx)

    @classmethod
    def call_internal(cls, thing, idx):
        return struct.pack('<BII', OPCODES['CALL_INTERNAL'], thing, idx)

    @classmethod
    def method_end(cls):
        return struct.pack('<B', OPCODES['METHOD_END'])

    @classmethod
    def call_method(cls, idx):
        return struct.pack('<BI', OPCODES['CALL_METHOD'], idx)


class CompilationContext(object):

    def __init__(self):
        self.symbols = []
        self.data = []

    def append(self, symbol):
        if isinstance(symbol, bytes):
            self.symbols.append(symbol)
        elif symbol:
            self.symbols.extend(symbol)

    def finalize(self):
        code = bytes().join(x if isinstance(x, bytes) else struct.pack(x[0], *x[1:]) for x in self.symbols)
        data = bytes().join(x for x in self.data)
        header = bytes('THING', 'utf-8') + struct.pack('<II', len(data) + len(code), len(data))

        return header + data + code

    def append_static(self, data):
        self.data.append(data)
        return len(self.data) - 1


class Compiler(TreeTraversal):

    def __init__(self, ast):
        super(Compiler, self).__init__(ast)
        self.context = CompilationContext()

    @inspects(priority=0)
    def extract_static_data(self, node):
        #self.context.append_static(node.statics())
        pass

    @inspects(priority=1)
    def compile_dfs(self, node):
        print('DFS inspection on node {}'.format(node))
        self.context.append(node.compile(self.context))