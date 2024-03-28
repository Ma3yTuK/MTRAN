from enum import StrEnum
from typing import Callable
from dataclasses import dataclass
from .identifiers_and_types import Variable
    

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

    O_DEREF = "&"

    O_ASS = "="

    O_INIT = ":="

    O_PERIOD = "."


class PunctuationName(StrEnum):
    P_COMMA = ",",
    P_SEMICOLON = ";"
    P_COLON = ":"
    P_PARENTHESES_O = "("
    P_PARENTHESES_C = ")"
    P_BRACES_O = "{"
    P_BRACES_C = "}"
    P_BRACKETS_O = "["
    P_BRACKETS_C = "]"



assignment_operators = {
    OperatorName.O_PLUS,
    OperatorName.O_MINUS,
    OperatorName.O_MUL_OR_REF,
    OperatorName.O_DIV,
    OperatorName.O_MOD
}


numeric_binary_operators_number = {
    OperatorName.O_PLUS,
    OperatorName.O_MINUS,
    OperatorName.O_MUL_OR_REF,
    OperatorName.O_DIV,
    OperatorName.O_MOD
}


numeric_binary_operators_bool = {
    OperatorName.O_GE,
    OperatorName.O_LE,
    OperatorName.O_LT,
    OperatorName.O_GT
}


any_binray_operators_bool = {
    OperatorName.O_EQ,
    OperatorName.O_NQ
}


boolean_binary_operators = {
    OperatorName.O_LAND,
    OperatorName.O_LOR
}


binary_operators = numeric_binary_operators_bool | numeric_binary_operators_number | any_binray_operators_bool | boolean_binary_operators


binary_operator_precedence = {
    OperatorName.O_PLUS : 4,
    OperatorName.O_MINUS : 4,
    OperatorName.O_MUL_OR_REF : 5,
    OperatorName.O_DIV : 5,
    OperatorName.O_MOD : 5,
    OperatorName.O_EQ : 3,
    OperatorName.O_NQ : 3,
    OperatorName.O_GT : 3,
    OperatorName.O_LT : 3,
    OperatorName.O_GE : 3,
    OperatorName.O_LE : 3,
    OperatorName.O_LAND : 2,
    OperatorName.O_LOR : 1,
}


numeric_unary_operators = {
    OperatorName.O_PLUS,
    OperatorName.O_MINUS
}


boolean_unary_operators = {
    OperatorName.O_LNOT
}


any_unary_operators = {
    OperatorName.O_MUL_OR_REF,
    OperatorName.O_DEREF
}


unary_operators = numeric_unary_operators | boolean_unary_operators | any_unary_operators


operators = binary_operators | unary_operators | {
    OperatorName.O_ASS,
    OperatorName.O_INCREMENT, 
    OperatorName.O_DECREMENT, 
    OperatorName.O_ASS, 
    OperatorName.O_PERIOD,
    OperatorName.O_INIT
}


punctuations = {
    PunctuationName.P_COMMA, 
    PunctuationName.P_SEMICOLON,
    PunctuationName.P_COLON,
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

    for end_pos in range(max_pos if max_pos < len(line) else len(line) - 1, pos, -1):
        
        if line[pos:end_pos] in operators_and_punctuations:
            return end_pos

    return pos
