from dataclasses import dataclass
from .tokens import Token
from typing import Dict, List, ClassVar
from .characters import word_separators, letters, character, skip_word, word_characters
from enum import StrEnum
from ..settings import PTR_SIZE


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


type_sizes: Dict[TypeName, int] = {
    TypeName.T_INT: 4,
    TypeName.T_INT8: 1,
    TypeName.T_INT16: 2,
    TypeName.T_INT32: 4,
    TypeName.T_INT64: 8,
    TypeName.T_UINT: 4,
    TypeName.T_UINT8: 1,
    TypeName.T_UINT16: 2,
    TypeName.T_UINT32: 4,
    TypeName.T_UINT64: 8,
    TypeName.T_FLOAT32: 4,
    TypeName.T_FLOAT64: 8
}


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

    def __post_init__(self):
        self.size = 0

        for field in self.fields:
            self.size += field.field_type.size


@dataclass
class FunctionType(Type):
    operands: List[BasicType]
    return_type: BasicType

    size: ClassVar[int] = PTR_SIZE


@dataclass
class NumericType(BasicType):
    size: int


@dataclass
class FloatingNumericType(NumericType):
    pass


@dataclass
class IntegerNumbericType(NumericType):
    pass


@dataclass
class StringType(BasicType):
    size: ClassVar[int] = PTR_SIZE


@dataclass
class BoolType(BasicType):
    size: ClassVar[int] = PTR_SIZE


@dataclass
class ArrayType(CompositType):
    count: int
    value_type: BasicType

    def __post_init__(self):
        self.size = self.count * self.value_type.size
    

@dataclass
class PointerType(BasicType):
    pointer_type: BasicType
    size: ClassVar[int] = PTR_SIZE


###Variables###


@dataclass
class Variable(Identifier):
    value_type: BasicType
    address: int



identifier_tables: List[Dict[str, Identifier]] = [{
    TypeName.T_STRING: StringType(),
    TypeName.T_INT: IntegerNumbericType(type_sizes[TypeName.T_INT]),
    TypeName.T_INT8: IntegerNumbericType(type_sizes[TypeName.T_INT8]),
    TypeName.T_INT16: IntegerNumbericType(type_sizes[TypeName.T_INT16]),
    TypeName.T_INT32: IntegerNumbericType(type_sizes[TypeName.T_INT32]),
    TypeName.T_INT64: IntegerNumbericType(type_sizes[TypeName.T_INT64]),
    TypeName.T_UINT: IntegerNumbericType(type_sizes[TypeName.T_UINT]),
    TypeName.T_UINT8: IntegerNumbericType(type_sizes[TypeName.T_UINT8]),
    TypeName.T_UINT16: IntegerNumbericType(type_sizes[TypeName.T_UINT16]),
    TypeName.T_UINT32: IntegerNumbericType(type_sizes[TypeName.T_UINT32]),
    TypeName.T_UINT64: IntegerNumbericType(type_sizes[TypeName.T_UINT64]),
    TypeName.T_FLOAT32: IntegerNumbericType(type_sizes[TypeName.T_FLOAT32]),
    TypeName.T_FLOAT64: IntegerNumbericType(type_sizes[TypeName.T_FLOAT64]),
    TypeName.T_BOOL: BoolType()
}]



def get_identifier(line, pos):

    if pos + 1 == len(line) or line[pos] not in word_characters:
        return pos

    pos = skip_word(line, pos)

    if pos + 1 < len(line) and line[pos] not in word_separators:
        raise Exception(f"{pos}: Unexpected character in an identifier: {line[pos]}")

    return pos