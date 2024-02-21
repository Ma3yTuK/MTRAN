from enum import StrEnum
from typing import Callable
from dataclasses import dataclass
from identifiers import Variable
    

MAX_O_LEN = 3


class OperatorName(StrEnum):
    O_PLUS = "+"
    O_MINUS = "-"
    O_MUL_OR_REF = "*"
    O_DIV = "/"
    O_MOD = "%"
    O_INCREMENT = "++"
    O_DECREMENT = "--"

    O_EQ = "=="
    O_NQ = "!="
    O_GT = ">"
    O_LT = "<"
    O_GE = ">="
    O_LE = "<="

    O_LAND = "&&"
    O_LOR = "||"
    O_LNOT = "!"

    O_AND_OR_DEREF = "&"
    O_OR = "|"
    O_XOR = "^"
    O_BLEFT_SHIFT = "<<"
    O_BRIGHT_SHIFT = ">>"

    O_ASS = "="
    O_PLUS_ASS = "+="
    O_MINUS_ASS = "-="
    O_MUL_ASS = "*="
    O_DEV_ASS = "/="
    O_MOD_ASS = "%="
    O_BAND_ASS = "&="
    O_BOR_ASS = "|="
    O_BXOR_ASS = "^="
    O_BLEFT_SHIFT_ASS = "<<="
    O_BRIGHT_SHIFT_ASS = ">>="

    O_INIT = ":="

    O_PERIOD = "."


class PunctuationName(StrEnum):
    P_COMMA = ",",
    P_SEMICOLON = ";"
    P_PARENTHESES_O = "(",
    P_PARENTHESES_C = ")",
    P_BRACES_O = "{",
    P_BRACES_C = "}",
    P_BRACKETS_O = "[",
    P_BRACKETS_C = "]"


operators = {
    OperatorName.O_PLUS, 
    OperatorName.O_MINUS, 
    OperatorName.O_MUL_OR_REF, 
    OperatorName.O_DIV, 
    OperatorName.O_MOD, 
    OperatorName.O_INCREMENT, 
    OperatorName.O_DECREMENT, 
    OperatorName.O_EQ, 
    OperatorName.O_NQ, 
    OperatorName.O_GT, 
    OperatorName.O_LT, 
    OperatorName.O_GE, 
    OperatorName.O_LE, 
    OperatorName.O_LAND, 
    OperatorName.O_LOR, 
    OperatorName.O_LNOT, 
    OperatorName.O_AND_OR_DEREF, 
    OperatorName.O_OR, 
    OperatorName.O_XOR, 
    OperatorName.O_BLEFT_SHIFT, 
    OperatorName.O_BRIGHT_SHIFT, 
    OperatorName.O_ASS, 
    OperatorName.O_PLUS_ASS, 
    OperatorName.O_MINUS_ASS, 
    OperatorName.O_MUL_ASS, 
    OperatorName.O_DEV_ASS, 
    OperatorName.O_MOD_ASS, 
    OperatorName.O_BAND_ASS, 
    OperatorName.O_BOR_ASS, 
    OperatorName.O_BXOR_ASS, 
    OperatorName.O_BLEFT_SHIFT_ASS, 
    OperatorName.O_BRIGHT_SHIFT_ASS, 
    OperatorName.O_PERIOD,
    OperatorName.O_INIT
}


punctuations = {
    PunctuationName.P_COMMA, 
    PunctuationName.P_SEMICOLON,
    PunctuationName.P_PARENTHESES_O, 
    PunctuationName.P_PARENTHESES_C, 
    PunctuationName.P_BRACES_O, 
    PunctuationName.P_BRACES_C, 
    PunctuationName.P_BRACKETS_O, 
    PunctuationName.P_BRACKETS_C
}


operators_and_punctuations = operators | punctuations


def get_operator_or_punctuation(line, pos):

    max_pos = pos + MAX_O_LEN

    for end_pos in range(max_pos if max_pos + 1 < len(line) else len(line) - 1, pos, -1):
        
        if line[pos:end_pos] in operators_and_punctuations:
            return end_pos

    return pos
