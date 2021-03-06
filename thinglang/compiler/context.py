import collections
import struct

from thinglang.compiler import serializer
from thinglang.compiler.opcodes import OpcodeHandlerDescription, OpcodeHandlerRangeDefinition
from thinglang.compiler.sentinels import SentinelMethodDefinition, SentinelCodeEnd, SentinelDataEnd, \
    SentinelImportTableEntry, SentinelImportTableEnd, SentinelThingDefinition, SentinelThingExtends
from thinglang.utils.source_context import SourceContext

HEADER_FORMAT = '<HIIII'
BytecodeHeader = collections.namedtuple('BytecodeHeader', [
    'version',
    'instruction_count',
    'data_item_count',
    'entrypoint',
    'initial_frame_size'
])

CompiledMethodMetadata = collections.namedtuple('CompiledMethodMetadata', ['address', 'frame_size'])


class CompilationContext(object):
    """
    The CompilationContext classes manages the entire compilation pass, including serialization into bytecode
    """
    def __init__(self, symbols, source: SourceContext=None, entry=None):

        self.symbols = symbols
        self.source = source

        self.current_locals = None
        self.entry = entry or 0

        self.classes = []

    def add_methods(self, methods, members, extending_index, methods_offset):
        """
        Add compiled method buffers
        """
        self.classes.append((methods, members, extending_index, methods_offset))
        return len(self.classes) - 1

    def buffer(self) -> 'CompilationContext':
        """
        Create a new independent compilation context which can later be merged into the primary context
        """

        return CompilationContext(self.symbols, self.source)

    def bytes(self) -> bytes:
        """
        Serializes the compilation context into thinglang bytecode
        """

        instructions = []
        data_items = []
        offsets = {}

        for class_id, (methods, members, extending_index, methods_offset) in enumerate(self.classes):
            instructions.append(SentinelThingDefinition(members, 0))
            if extending_index is not None:
                instructions.append(SentinelThingExtends(extending_index))

            for method_id, (method, buffer) in enumerate(methods):
                method_offset, data_offset = len(instructions) + len(buffer.exception_table) * 2 + 1, len(data_items)

                instructions.append(SentinelMethodDefinition(method_offset, method.frame_size))

                # First, we write the exception table for this method
                for exception, handler, start_index, end_index in buffer.exception_table:
                    exception_type = self.symbols.index(exception)
                    instructions.extend([
                        OpcodeHandlerDescription(method_offset + len(buffer.instructions) + handler, exception_type),
                        OpcodeHandlerRangeDefinition(start_index + method_offset, end_index + method_offset)
                    ])

                offsets[(class_id, method_id + methods_offset)] = CompiledMethodMetadata(method_offset, method.frame_size)
                instructions.extend(instruction.update_offset(method_offset, data_offset) for instruction in buffer.instructions)
                instructions.extend(instruction.update_offset(method_offset, data_offset) for instruction in buffer.epilogues)

                data_items.extend(buffer.data)

        for instruction in instructions:
            instruction.update_references(offsets)

        instructions.append(SentinelCodeEnd())

        if not all(x.source_ref is not None for x in instructions):
            raise Exception('Not all instructions could be mapped to their source: {}'.format([x for x in instructions if x.source_ref is None]))

        imports = bytes().join(SentinelImportTableEntry().serialize() + serializer.auto(name) for name, symbol_map in self.symbols.indexed) + SentinelImportTableEnd().serialize()
        code = bytes().join(x.serialize() for x in instructions)
        data = bytes().join(x for x in data_items) + SentinelDataEnd().serialize()
        source_map = bytes().join(x.source_ref.serialize() for x in instructions)

        entry = offsets[(self.entry.thing_index, self.entry.element_index)]
        header = bytes('THING', 'utf-8') + bytes([0xcc]) + struct.pack(HEADER_FORMAT, *BytecodeHeader(
            version=4,
            instruction_count=len(instructions),
            data_item_count=len(data_items),
            entrypoint=entry.address,
            initial_frame_size=entry.frame_size
        ))

        return header + imports + code + data + source_map + bytes(self.source.raw_contents, 'utf-8')


