from enum import StrEnum
from .identifiers_and_types import get_identifier



class KeywordName(StrEnum):
    K_BREAK = "break"
    K_CASE = "case"
    K_CONST = "const"
    K_DEFAULT = "default"
    K_ELSE = "else"
    K_FOR = "for"
    K_FUNC = "func"
    K_IF = "if"
    K_RETURN = "return"
    K_STRUCT = "struct"
    K_SWITCH = "switch"
    K_CONTINUE = "continue"
    K_PRINT = "print"
    K_TYPE = "type"
    K_VAR = "var"



keywords = {
    KeywordName.K_BREAK,
    KeywordName.K_CASE,
    KeywordName.K_CONST,
    KeywordName.K_DEFAULT,
    KeywordName.K_ELSE,
    KeywordName.K_FOR,
    KeywordName.K_FUNC,
    KeywordName.K_IF,
    KeywordName.K_RETURN,
    KeywordName.K_STRUCT,
    KeywordName.K_SWITCH,
    KeywordName.K_TYPE,
    KeywordName.K_VAR,
    KeywordName.K_CONTINUE,
    KeywordName.K_PRINT
}


def is_keyword(word):
    if word not in keywords:
        return False
    else:
        return True