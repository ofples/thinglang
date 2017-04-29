import re


from thinglang.lexer.tokens.logic import LexicalConditional, LexicalEquality, LexicalElse, LexicalNegation, \
    LexicalGreaterThan, LexicalLessThan, LexicalBooleanTrue, LexicalBooleanFalse, LexicalRepeat, LexicalRepeatWhile, \
    LexicalIn, LexicalRepeatFor
from thinglang.lexer.tokens.arithmetic import LexicalAddition, LexicalSubtraction, LexicalDivision, \
    LexicalMultiplication
from thinglang.lexer.tokens.base import LexicalParenthesesOpen, LexicalParenthesesClose, LexicalQuote, LexicalSeparator, \
    LexicalIndent, LexicalAccess, LexicalInlineComment, LexicalAssignment, LexicalBracketOpen, LexicalBracketClose
from thinglang.lexer.tokens.functions import LexicalReturnStatement, LexicalArgumentListIndicator, \
    LexicalDeclarationMethod, LexicalDeclarationThing, LexicalDeclarationMember, LexicalDeclarationConstructor, \
    LexicalClassInitialization
from thinglang.lexer.tokens.typing import LexicalCast

IDENTIFIER_BASE = r"[a-zA-Z]\w*"
IDENTIFIER_STANDALONE = re.compile("^" + IDENTIFIER_BASE + "$")

OPERATORS = {
    ' ': None,

    "\"": LexicalQuote,
    "\t": LexicalIndent,

    '.': LexicalAccess,
    ',': LexicalSeparator,
    '=': LexicalAssignment,

    '(': LexicalParenthesesOpen,
    ')': LexicalParenthesesClose,

    '[': LexicalBracketOpen,
    ']': LexicalBracketClose,

    '+': LexicalAddition,
    '-': LexicalSubtraction,
    '/': LexicalDivision,
    '*': LexicalMultiplication,

    '>': LexicalGreaterThan,
    '<': LexicalLessThan,

    '#': LexicalInlineComment
}


KEYWORDS = {
    'thing': LexicalDeclarationThing,
    'does': LexicalDeclarationMethod,
    'has': LexicalDeclarationMember,
    'setup': LexicalDeclarationConstructor,

    'create': LexicalClassInitialization,

    'with': LexicalArgumentListIndicator,
    'return': LexicalReturnStatement,

    'if': LexicalConditional,
    'otherwise': LexicalElse,

    'repeat': LexicalRepeat,
    'while': LexicalRepeatWhile,
    'in': LexicalIn,
    'for': LexicalRepeatFor,

    'eq': LexicalEquality,
    'not': LexicalNegation,

    'true': LexicalBooleanTrue,
    'false': LexicalBooleanFalse,

    'as': LexicalCast
}

REVERSE_OPERATORS = {
    v: k for k, v in OPERATORS.items()
}


def is_identifier(component):
    return bool(IDENTIFIER_STANDALONE.match(component))