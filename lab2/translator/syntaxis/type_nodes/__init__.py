from .type_node import TypeNode
from .type_literals.type_literal import TypeLiteral
from .type_literals.type_literal import TypeLiteral
from .basic_type import BasicType



TypeNode.child_order = [TypeLiteral, BasicType]