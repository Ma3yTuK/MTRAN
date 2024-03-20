from .type_literal import TypeLiteral
from .array_type import ArrayType
from .function_type import FuncType
from .pointer_type import PointerType
from .struct_type import StructType



TypeLiteral.child_order = [ArrayType, FuncType, PointerType, StructType]