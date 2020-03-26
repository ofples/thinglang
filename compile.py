import os
import argparse

from thinglang.utils.source_context import SourceContext
from thinglang import pipeline


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sourcefile", help="The input thing source file to compile.")
    return parser.parse_args()


def compile(target_source_file_path):
    source_context = SourceContext.wrap(
        str(open(target_source_file_path, "rb").read(), encoding="utf-8"))
    compilation_result = pipeline.compile(source_context)
    return compilation_result.bytes()


def main():
    source_file = parse_args().sourcefile
    print(f"Compiling {source_file}...")

    compiled_bytecode = compile(source_file)
    target_file_path = os.path.splitext(source_file)[0] + ".tlc"
    print(f"Compilation successful, writing bytecode to {target_file_path}")

    with open(target_file_path, "wb") as bytecode_file:
        bytecode_file.write(compiled_bytecode)

    print(f"Done! :)")


if __name__ == "__main__":
    main()
