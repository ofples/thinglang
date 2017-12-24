import glob

import os

from thinglang.lexer.values.identifier import Identifier

"""
The internal ordering of core types used by the compiler and runtime
"""

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATTERN = os.path.join(CURRENT_PATH,  'source/**/*.thing')


def list_types():
    for path in glob.glob(SOURCE_PATTERN, recursive=True):
        name = os.path.basename(path).replace('.thing', '')
        yield name, path


PRIMITIVE_TYPES = [
    'text',
    'number'
]

INTERNAL_SOURCES = {Identifier(name): path for name, path in list_types()}