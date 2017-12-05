from tests.compiler import compile_local, SELF_ID, LST_ID, VAL1_ID
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePushIndexImmediate, OpcodeCallInternal, OpcodePushMember, \
    OpcodePushIndex


def test_access_in_method_args():
    assert compile_local('self.action(lst[123])') == [
        OpcodePushLocal(SELF_ID),
        OpcodePushLocal(LST_ID),
        OpcodePushIndexImmediate(123),
        OpcodeCallInternal(0, 3)
    ]

    assert compile_local('self.action(lst[self.val1])') == [
        OpcodePushLocal(SELF_ID),
        OpcodePushLocal(LST_ID),
        OpcodePushMember(SELF_ID, VAL1_ID),
        OpcodePushIndex(),
        OpcodeCallInternal(0, 3)
    ]