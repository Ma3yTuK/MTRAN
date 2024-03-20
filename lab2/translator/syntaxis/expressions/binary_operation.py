from .expression import Expression
from ..node import Node
from dataclasses import dataclass
from ...lexic.operators_punctuation import PunctuationName, OperatorName, binary_operators, binary_operator_precedence
from ...lexic.tokens import token_table, Token, TokenType
from .unary_expressions.unary_expression import UnaryExpression
from ..syntaxis_exception import SyntaxisException



@dataclass
class BinaryOperator(Node):
    operator: str # binary

    @classmethod
    def get_node(cls, token_table_index):
        
        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name not in binary_operators:
            return token_table_index, None

        new_node = cls(token_table[token_table_index].name)
        token_table_index += 1

        return token_table_index, new_node

    def __str__(self):
        return self.__class__.__name__ + '(' + self.operator + ')\n'


@dataclass
class BinaryOperation(Expression):
    operator: BinaryOperator
    argument1: Expression
    argument2: Expression

    @classmethod
    def get_node(cls, token_table_index):
        arguments_stack: List[Expression] = []
        operators_stack: List[BinaryOperator] = []

        new_token_table_index, new_unary_expression = UnaryExpression.get_node(token_table_index)

        if new_unary_expression == None:
            return token_table_index, None

        arguments_stack.append(new_unary_expression)
        new_token_table_index, new_operator = BinaryOperator.get_node(new_token_table_index)

        if new_operator == None:
            return token_table_index, None

        new_addressable = False
        token_table_index = new_token_table_index

        while new_operator != None:
            
            while operators_stack and binary_operator_precedence[new_operator.operator] <= binary_operator_precedence[operators_stack[-1].operator]:
                new_argument2 = arguments_stack.pop()
                new_argument1 = arguments_stack.pop()
                new_expression = cls(new_addressable, operators_stack.pop(), new_argument1, new_argument2)
                arguments_stack.append(new_expression)

            operators_stack.append(new_operator)
            token_table_index, new_unary_expression = UnaryExpression.get_node(token_table_index)

            if new_unary_expression == None:
                raise SyntaxisException(token_table[token_table_index], "Expression expected!")

            arguments_stack.append(new_unary_expression)
            token_table_index, new_operator = BinaryOperator.get_node(token_table_index)

        while operators_stack:
            new_argument2 = arguments_stack.pop()
            new_argument1 = arguments_stack.pop()
            new_expression = cls(new_addressable, operators_stack.pop(), new_argument1, new_argument2)
            arguments_stack.append(new_expression)

        new_node = arguments_stack[0]

        return token_table_index, new_node