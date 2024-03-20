from .unary_expression import UnaryExpression
from .unary_operation import UnaryOperation
from .primary_expressions.primary_expression import PrimaryExpression



UnaryExpression.child_order = [UnaryOperation, PrimaryExpression]