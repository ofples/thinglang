import pytest

from thinglang.execution.errors import UnknownVariable
from thinglang.runner import run


def test_stack_resolution_in_block():
    assert run("""
thing Program
    does start

        number i = 0
        Output.write("outside before, i =", i)
        if true
            Output.write("inside before, i =", i)
            i = 10
            Output.write("inside after, i =", i)

        Output.write("outside after, i =", i)

    """).output == """
outside before, i = 0
inside before, i = 0
inside after, i = 10
outside after, i = 10""".strip()


