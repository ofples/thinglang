import os
import pytest
import glob
import subprocess

import thinglang
from tests.infrastructure.test_utils import ProgramTestCase
from thinglang import utils

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

SEARCH_PATTERN = os.path.join(BASE_PATH, '**/*.thing')


def collect_tests():
    for path in glob.glob(SEARCH_PATTERN, recursive=True):
        #if 'simple_thing' in path:
            yield ProgramTestCase(path)


def split_lines(param):
    return param.replace('\r', '').split('\n')


@pytest.mark.parametrize('test_file', collect_tests(), ids=lambda x: x.name)
def test_thing_program(test_file: ProgramTestCase):
    expected_output = test_file.metadata['expected_output']

    utils.print_header('Parsed AST')
    ast = thinglang.compiler(test_file.code)
    print(ast.tree())

    utils.print_header("Bytecode generation")
    bytecode = ast.compile().finalize()
    print(bytecode)

    utils.print_header('VM execution')

    with open(test_file.target_path, 'wb') as f:
        f.write(bytecode)

    vm = subprocess.Popen(["thinglang", test_file.target_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = (stream.decode('utf-8').strip() for stream in vm.communicate())
    print(stderr)

    utils.print_header('VM output')
    print(stdout)

    local = thinglang.run(test_file.code).output

    if not isinstance(expected_output, str):
        stdout = split_lines(stdout)
        local = split_lines(local)

    assert vm.returncode == 0, 'VM process crashed'
    assert local == expected_output, 'Execution engine output did not match expected output'
    assert stdout == expected_output, 'VM output did not match expected output'




