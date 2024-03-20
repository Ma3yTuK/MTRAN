from .expression import Expression
from .binary_operation import BinaryOperation
from .unary_expressions.unary_expression import UnaryExpression



Expression.child_order = [BinaryOperation, UnaryExpression]