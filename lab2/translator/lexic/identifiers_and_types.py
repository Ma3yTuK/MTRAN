from dataclasses import dataclass
from .tokens import Token
from typing import Dict, List, ClassVar
from .characters import word_separators, letters, character, skip_word, word_characters
from enum import StrEnum
from ..settings import PTR_SIZE
import struct



STRING_SIZE = 256
FLOAT_SIZE = 4
INT_SIZE = 4
BOOL_SIZE = 1
TYPE_SIZE = 1


###Types###


class TypeName(StrEnum):
    T_INT = "int"
    T_UINT = "uint"
    T_FLOAT32 = "float32"
    T_BOOL = "bool"
    T_STRING = "string"


type_sizes: Dict[TypeName, int] = {
    TypeName.T_INT: 4,
    TypeName.T_UINT: 4,
    TypeName.T_FLOAT32: 4
}


type_aliases: Dict[TypeName, str] = {
    TypeName.T_INT: "!i",
    TypeName.T_UINT: "!I",
    TypeName.T_FLOAT32: "!f",
    TypeName.T_STRING: f"!{STRING_SIZE}s",
    TypeName.T_BOOL: "!?"
}


@dataclass
class Type:

    def from_python(self, value):
        pass
    
    def to_python(self, value):
        pass


@dataclass
class NormalType(Type):

    def from_python(self, value):
        pass
    
    def to_python(self, value):
        pass


@dataclass
class MetaType(Type):
    u_type: NormalType

    size: ClassVar[int] = TYPE_SIZE


@dataclass
class BasicType(NormalType):
    pass


@dataclass
class CompositType(NormalType):
    pass


@dataclass
class UserType(NormalType):

    @dataclass
    class TypeField:
        field_name: str
        field_type: NormalType

    fields: Dict[str, TypeField] # field_name : field

    def __post_init__(self):
        self.size = 0

        for name, field in self.fields.items():
            self.size += field.field_type.size

    def from_python(self, value):
        result = bytes()

        for index, (name, field) in enumerate(self.fields.items()):
            result += field.field_type.from_python(value[index])

        return result

    def to_python(self, value):
        result = []
        pos = 0

        for name, field in self.fields.items():
            new_pos = pos + field.field_type.size
            result.append(field.field_type.to_python(value[pos:new_pos]))
            pos = new_pos

        return result


@dataclass
class FunctionTypeL(NormalType):
    operands: List[NormalType]
    return_type: NormalType | None

    size: ClassVar[int] = INT_SIZE

    def from_python(self, value):
        return struct.pack(type_aliases[TypeName.T_INT], value)

    def to_python(self, value):
        return struct.unpack(type_aliases[TypeName.T_INT], value)


@dataclass
class NumericType(BasicType):
    pass


@dataclass
class FloatingNumericType(NumericType):
    size: ClassVar[int] = FLOAT_SIZE

    def from_python(self, value):
        return struct.pack(type_aliases[TypeName.T_FLOAT32], value)

    def to_python(self, value):
        return struct.unpack(type_aliases[TypeName.T_FLOAT32], value)


@dataclass
class IntegerNumbericType(NumericType):
    size: ClassVar[int] = INT_SIZE

    def from_python(self, value):
        return struct.pack(type_aliases[TypeName.T_INT], value)

    def to_python(self, value):
        return struct.unpack(type_aliases[TypeName.T_INT], value)


@dataclass
class StringType(BasicType):
    size: ClassVar[int] = STRING_SIZE

    def from_python(self, value):
        return struct.pack(type_aliases[TypeName.T_STRING], value.encode())

    def to_python(self, value):
        return struct.unpack(type_aliases[TypeName.T_STRING], value).decode()


@dataclass
class BoolType(BasicType):
    size: ClassVar[int] = BOOL_SIZE

    def from_python(self, value):
        return struct.pack(type_aliases[TypeName.T_BOOL], value.encode())

    def to_python(self, value):
        return struct.unpack(type_aliases[TypeName.T_BOOL], value).decode()


@dataclass
class ArrayTypeL(CompositType):
    count: int
    value_type: NormalType

    def __post_init__(self):
        self.size = self.count * self.value_type.size

    def from_python(self, value):
        result = bytes()

        for element in value:
            result += self.value_type.from_python(element)

        return result

    def to_python(self, value):
        result = []
        pos = 0

        for index in range(self.count):
            new_pos = pos + field.field_type.size
            result.append(self.value_type.to_python(value[pos:new_pos]))
            pos = new_pos

        return result
    

@dataclass
class PointerTypeL(NormalType):
    pointer_type: NormalType
    size: ClassVar[int] = INT_SIZE

    def from_python(self, value):
        return struct.pack(type_aliases[TypeName.T_INT], value)

    def to_python(self, value):
        return struct.unpack(type_aliases[TypeName.T_INT], value)


###Variables###


@dataclass
class Identifier:
    value_type: Type
    stack_pos: int

    current_stack_pos: ClassVar = 0



identifier_tables: List[Dict[str, Identifier]] = [{
    TypeName.T_STRING: Identifier(MetaType(StringType()), 0),
    TypeName.T_INT: Identifier(MetaType(IntegerNumbericType(type_sizes[TypeName.T_INT])), 0),
    TypeName.T_UINT: Identifier(MetaType(IntegerNumbericType(type_sizes[TypeName.T_UINT])), 0),
    TypeName.T_FLOAT32: Identifier(MetaType(IntegerNumbericType(type_sizes[TypeName.T_FLOAT32])), 0),
    TypeName.T_BOOL: Identifier(MetaType(BoolType()), 0)
}]



def get_identifier(line, pos):

    if pos + 1 == len(line) or line[pos] not in word_characters:
        return pos

    pos = skip_word(line, pos)

    if pos + 1 < len(line) and line[pos] not in word_separators:
        raise Exception(f"{pos}: Unexpected character in an identifier: {line[pos]}")

    return pos