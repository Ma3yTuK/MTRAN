from dataclasses import dataclass
from .tokens import Token
from typing import Dict
from .identifiers_and_types import TypeAlias, TypeName, get_identifier, BasicType, identifier_tables
from .characters import digits, character, word_separators, skip_number, skip_word, ENCODING_TYPE, exponent


INT_TYPE = TypeName.T_INT
FLOAT_TYPE = TypeName.T_FLOAT32

BOOLEAN_TRUE = "true"
BOOLEAN_FALSE = "false"
NIL = "nil"


@dataclass
class Literal:
    value_type: BasicType
    value: bytes


literals: Dict[str, Literal] = {
    "true":  Literal(TypeName.T_BOOL, True),
    "false": Literal(TypeName.T_BOOL, False)
}


def add_literal(line, pos):
    if pos + 1 == len(line):
        return pos

    end_pos = pos

    if line[end_pos] == character.quotes:
        end_pos += 1

        while end_pos + 1 < len(line) and line[end_pos] != character.quotes:
            end_pos += 1

        if end_pos + 1 == len(line) or end_pos + 2 < len(line) and line[end_pos+1] not in word_separators:
            raise Exception(f"{end_pos}: String literal must end with \"")
    
        result = line[pos:end_pos+1]
        
        if result not in literals:
            literals[result] = Literal(identifier_tables[0][TypeName.T_STRING], result)

        return end_pos + 1

    end_pos = skip_number(line, pos)

    if end_pos != pos:
        
        if end_pos + 2 < len(line) and (line[end_pos] == character.period or line[end_pos] in exponent):

            if line[end_pos] == character.period:
                end_pos = skip_number(line, end_pos + 1)

            if line[end_pos-1] in digits:

                if end_pos + 2 < len(line) and line[end_pos] in exponent:
                    
                    if line[end_pos+1] in {character.plus, character.minus}:
                        end_pos += 1

                    end_pos = skip_number(line, end_pos + 1)
                    
                if line[end_pos-1] in digits and (end_pos + 1 == len(line) or line[end_pos] in word_separators):
                    result = line[pos:end_pos]

                    if result not in literals:
                        literals[result] = Literal(identifier_tables[0][TypeName.T_FLOAT32], float(result))

                    return end_pos


        elif end_pos == len(line) or line[end_pos] in word_separators:
            result = line[pos:end_pos]

            if result not in literals:
                literals[result] = Literal(identifier_tables[0][TypeName.T_INT], int(result))

            return end_pos

        raise Exception(f"{end_pos}: Unexpected symbol in numeric")

    end_pos = get_identifier(line, pos)

    if end_pos + 1 < pos:
        result = line[pos, end_pos]

        if result in {BOOLEAN_FALSE, BOOLEAN_TRUE, NIL}:
            return end_pos

    return pos