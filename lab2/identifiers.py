from dataclasses import dataclass
from tokens import Token
from typing import Dict, List
from characters import word_separators, letters, character, skip_word, word_separators
from enum import StrEnum


@dataclass
class Identifier:
    pass


###Types###


class TypeName(StrEnum):
    T_INT = "int"
    T_INT8 = "int8"
    T_INT16 = "int16"
    T_INT32 = "int32"
    T_INT64 = "int64"
    T_UINT = "uint"
    T_UINT8 = "uint8"
    T_UINT16 = "uint16"
    T_UINT32 = "uint32"
    T_UINT64 = "uint64"
    T_FLOAT32 = "float32"
    T_FLOAT64 = "float64"
    T_BOOL = "bool"
    T_STRING = "string"


class TypeAlias(StrEnum):
    T_INT = "!i"
    T_INT8 = "!b"
    T_INT16 = "!h"
    T_INT32 = "!l"
    T_INT64 = "!q"
    T_UINT = "!I"
    T_UINT8 = "!B"
    T_UINT16 = "!H"
    T_UINT32 = "!L"
    T_UINT64 = "!Q"
    T_FLOAT32 = "!f"
    T_FLOAT64 = "!d"
    T_STRING = "!s"
    T_BOOL = "!?"


@dataclass
class Type:
    pass


@dataclass
class BasicType(Type, Identifier):
    pass


@dataclass
class CompositType(Type):
    pass


@dataclass
class UserType(Type, Identifier):

    @dataclass
    class TypeField:
        field_name: str
        field_type: BasicType

    fields: Dict[str, TypeField] # field_name : field


@dataclass
class FunctionType(Type):
    operands: List[BasicType]
    return_type: BasicType


@dataclass
class MethodType(FunctionType):
    object_type: UserType


@dataclass
class NumericType(BasicType):
    type_alias: TypeAlias


@dataclass
class StringType(BasicType):
    type_alias: TypeAlias


@dataclass
class BoolType(BasicType):
    type_alias: TypeAlias


@dataclass
class ArrayType(CompositType):
    size: int
    value_type: BasicType


@dataclass
class MapType(CompositType):
    key_type: BasicType
    value_type: BasicType
    

@dataclass
class PointerType(CompositType):
    pointer_type: BasicType
    order: BasicType


###Variables###


@dataclass
class Variable(Identifier):
    value_type: BasicType
    const: bool

    address: int


###Functions###


@dataclass
class Func(Identifier):
    value_type: FunctionType

    pos: int



identifier_table: List[Dict[str, Identifier]] = [{
    TypeName.T_STRING: StringType(TypeAlias.T_STRING),
    TypeName.T_INT: NumericType(TypeAlias.T_INT),
    TypeName.T_INT8: NumericType(TypeAlias.T_INT8),
    TypeName.T_INT16: NumericType(TypeAlias.T_INT16),
    TypeName.T_INT32: NumericType(TypeAlias.T_INT32),
    TypeName.T_INT64: NumericType(TypeAlias.T_INT64),
    TypeName.T_UINT: NumericType(TypeAlias.T_UINT),
    TypeName.T_UINT8: NumericType(TypeAlias.T_UINT8),
    TypeName.T_UINT16: NumericType(TypeAlias.T_UINT16),
    TypeName.T_UINT32: NumericType(TypeAlias.T_UINT32),
    TypeName.T_UINT64: NumericType(TypeAlias.T_UINT64),
    TypeName.T_FLOAT32: NumericType(TypeAlias.T_FLOAT32),
    TypeName.T_FLOAT64: NumericType(TypeAlias.T_FLOAT64),
    TypeName.T_BOOL: BoolType(TypeAlias.T_BOOL)
}]



def get_identifier(line, pos):

    if pos + 1 == len(line) or line[pos] not in letters and line[pos] != character.underline:
        return pos

    pos = skip_word(line, pos)

    if pos + 1 < len(line) and line[pos] not in word_separators:
        raise Exception(f"{pos}: Unexpected character in an identifier: {line[pos]}")

    return pos