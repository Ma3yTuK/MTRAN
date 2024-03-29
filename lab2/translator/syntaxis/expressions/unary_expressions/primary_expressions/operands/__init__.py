from .operand import Operand
from .parenthesis_operand import ParanthesisOperand
from .literals.literal_node import LiteralNode
from .identifier_operand import IdentifierOperand



Operand.child_order = [LiteralNode, IdentifierOperand, ParanthesisOperand]