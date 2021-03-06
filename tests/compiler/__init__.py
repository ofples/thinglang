import pprint

from thinglang import pipeline
from thinglang.compiler.opcodes import OpcodeCallInternal
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.cast_tag import CastTag
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.utils.source_context import SourceContext

SELF_ID, A_ID, B_ID, INST_ID, LST_ID, A_INST, B_INST, C_INST, IMPLICIT_ITERATOR_ID, IMPLICIT_ITERATION_ID = range(10)
VAL1_ID, VAL2_ID, INNER_ID = 0, 1, 2
INNER1_ID, INNER2_ID, CONTAINER_INNER_ID = 0, 1, 2
STATIC_START, LOCAL_START = 3, 8

PROGRAM, CONTAINER, A_THING, B_THING, C_THING = range(5)

SYMBOL_MAPPER = SymbolMapper()

TEMPLATE = """
thing Program
    has number val1
    has number val2
    has Container inner
    
    setup
        number a = 0
        number b = 0
        Program inst = Program()
        list<Container> lst = [Container(), Container(), Container()]  
        A a_inst = A()
        B b_inst = B(42)
        C c_inst = C()
        
        {}
    
    does action with Container c 
        Console.print("action")
        
    does add with number a, number b
        return a + b


thing Container
    has number inner1
    has number inner2
    has Container inner
    
thing A
    has number a1
    
    does me returns A
        return self

thing B extends A
    has number b1
    
    setup with number b1
        self.b1 = b1
        
thing C extends B
    has number c1
    
thing Generic with type T
    
    static does static_method
        Console.print("hello!")
    
    does instance_method
        Console.print("also hello!")
        
"""

BASE_TEMPLATE = """
thing Program
    setup
        {}
"""


def compile_base(code='', thing_id=0, method_id=0, trim=False):
    context = pipeline.compile(SourceContext.wrap(code), mapper=SYMBOL_MAPPER)
    entry = context.classes[thing_id][0][method_id]
    instructions = entry[1].instructions
    return instructions[trim + 1:-1] if trim else instructions



def compile_template(code='', thing_id=0, method_id=0):
    return compile_base(TEMPLATE.format(code), thing_id, method_id)


TRIM_START = len(compile_template()) - 1


def compile_snippet(code):
    if isinstance(code, dict):
        for key, value in code.items():
           code = key + '\n\t\t\t' + '\n\t\t\t'.join(value)
    print(TEMPLATE.format(code))
    instructions = compile_template(code)[TRIM_START:-1]  # Pop off boilerplate and the return instruction
    print('Bytecode result: {}'.format(pprint.pformat(instructions)))
    return [instruction.resolve() for instruction in instructions]


def internal_call(target):
    return OpcodeCallInternal.from_reference(SYMBOL_MAPPER.resolve_named([
        CastTag(Identifier(x[3:])) if x.startswith('as ') else Identifier(x) for x in target.split('.')
    ], generic_validation=False))
