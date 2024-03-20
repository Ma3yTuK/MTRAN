from .operand import Operand
from .parenthesis_operand import ParanthesisOperand
from .literals.literal_node import LiteralNode
from .identifiers.identifier_node import IdentifierNode



Operand.child_order = [LiteralNode, IdentifierNode, ParanthesisOperand]