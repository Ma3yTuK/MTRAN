from .primary_expression import PrimaryExpression
from .primary_expression_with_suffix import PrimaryExpressionWithSuffix
from .operands.operand import Operand
from .conversion import Conversion



PrimaryExpression.child_order = [Conversion, PrimaryExpressionWithSuffix, Operand]