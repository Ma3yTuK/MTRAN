from dataclasses import dataclass
from .tokens import Token
from typing import Dict
from .identifiers_and_types import TypeAlias, TypeName, get_identifier, NormalType, identifier_tables
from .characters import digits, character, word_separators, skip_number, skip_word, ENCODING_TYPE, exponent



BOOLEAN_TRUE = "true"
BOOLEAN_FALSE = "false"


MAX_STRING_LEN = 100


@dataclass
class Literal:
    value_type: NormalType
    value: bytes


literals: Dict[str, Literal] = {
    "true":  Literal(identifier_tables[0][TypeName.T_BOOL], identifier_tables[0][TypeName.T_BOOL].from_python(True)),
    "false":  Literal(identifier_tables[0][TypeName.T_BOOL], identifier_tables[0][TypeName.T_BOOL].from_python(False)),
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

        if end_pos + 1 - pos > MAX_STRING_LEN:
            raise Exception(f"{pos}: String literal is too long")

        result = line[pos:end_pos+1]
        
        if result not in literals:
            literals[result] = Literal(identifier_tables[0][TypeName.T_STRING], identifier_tables[0][TypeName.T_STRING].from_python(result))

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
                        literals[result] = Literal(identifier_tables[0][TypeName.T_FLOAT32], identifier_tables[0][TypeName.T_FLOAT32].from_python(float(result)))

                    return end_pos


        elif end_pos == len(line) or line[end_pos] in word_separators:
            result = line[pos:end_pos]

            if result not in literals:
                literals[result] = Literal(identifier_tables[0][TypeName.T_INT], identifier_tables[0][TypeName.T_INT].from_python(int(result)))

            return end_pos

        raise Exception(f"{end_pos}: Unexpected symbol in numeric")

    end_pos = get_identifier(line, pos)

    if end_pos + 1 < pos:
        result = line[pos, end_pos]

        if result in {BOOLEAN_FALSE, BOOLEAN_TRUE}:
            return end_pos

    return pos