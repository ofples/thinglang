import re

from thinglang.lexer.lexical_tokens import LexicalParenthesesClose, LexicalQuote, LexicalSeparator, LexicalIndent, LexicalParenthesesOpen, LexicalAccess, \
    LexicalIdentifier, LexicalDunary, LexicalDeclarationThing, LexicalDeclarationMethod, LexicalNumericalValue, \
    LexicalAssignment, FirstOrderLexicalDunary, SecondOrderLexicalDunary, LexicalArgumentListIndicator, LexicalGroupEnd, \
    LexicalInlineComment
from thinglang.parser.tokens import String

IDENTIFIER_BASE = r"[a-zA-Z]\w*"
IDENTIFIER = re.compile(IDENTIFIER_BASE)
IDENTIFIER_STANDALONE = re.compile("^" + IDENTIFIER_BASE + "$")

OPERATORS = {
    ' ': None,
    '(': LexicalParenthesesOpen,
    ')': LexicalParenthesesClose,
    '.': LexicalAccess,

    "\"": LexicalQuote,
    ',': LexicalSeparator,
    "\t": LexicalIndent,

    '=': LexicalAssignment,

    '+': FirstOrderLexicalDunary,
    '-': FirstOrderLexicalDunary,
    '/': SecondOrderLexicalDunary,
    '*': SecondOrderLexicalDunary,

    '#': LexicalInlineComment
}


KEYWORDS = {'thing': LexicalDeclarationThing, 'does': LexicalDeclarationMethod, 'with': LexicalArgumentListIndicator}


def contextify_lexical_output(lexical_group, line):
    for entity in lexical_group:
        entity.context = {
            "line": line
        }

        yield entity


def lexer(source):
    for idx, line in enumerate(source.strip().split('\n')):
        yield list(contextify_lexical_output(analyze_line(line), idx))


def analyze_line(line):
    group = ""
    operator_set = OPERATORS
    for char in line:

        if char in operator_set:
            if group:
                yield finalize_group(group, char)
            if operator_set[char] is not None:
                operator = operator_set[char]
                if operator is LexicalQuote:
                    operator_set = OPERATORS if operator_set is not OPERATORS else {'"': LexicalQuote}
                    print('changed_operator set to {} {}'.format(operator_set, group))
                if operator is LexicalInlineComment:
                    break
                if operator.emittable:
                    yield OPERATORS[char](char)
            group = ""
        else:
            group += char
    if group:
        yield finalize_group(group, 'STOP')

    yield LexicalGroupEnd(None)


def finalize_group(group, terminating_char):
    if group in KEYWORDS:
        return KEYWORDS[group](group)

    if group.isdigit():
        return LexicalNumericalValue(group)

    if terminating_char == '"':
        return String(group)

    if is_identifier(group):
        return LexicalIdentifier(group)

    raise RuntimeError('Lexer: cannot finalize group {}'.format(group))


def is_identifier(component):
    return bool(IDENTIFIER_STANDALONE.match(component))
