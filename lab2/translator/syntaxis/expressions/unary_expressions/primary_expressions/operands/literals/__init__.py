from .literal_node import LiteralNode
from .basic_literal import BasicLiteral
from .composit_literal import CompositLiteral



LiteralNode.child_order = [CompositLiteral, BasicLiteral]