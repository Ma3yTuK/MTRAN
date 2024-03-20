from .primary_expression import PrimaryExpression
from .primary_expression_with_suffix import PrimaryExpressionWithSuffix
from .operands.operand import Operand



PrimaryExpression.child_order = [PrimaryExpressionWithSuffix, Operand]