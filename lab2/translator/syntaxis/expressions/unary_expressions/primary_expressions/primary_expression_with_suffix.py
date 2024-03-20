from .primary_expression import PrimaryExpression
from .operands.operand import Operand
from dataclasses import dataclass
from ....node import Node
from .operands.identifiers.identifier_node import IdentifierNode
from ...expression import Expression
from ....suffixes.suffix import Suffix
from ....suffixes.arguments_suffix import ArgumentsSuffix
from .....lexic.tokens import Token, token_table, TokenType



@dataclass
class PrimaryExpressionWithSuffix(PrimaryExpression):
    primary_expression: PrimaryExpression
    expression_suffix: Suffix

    @classmethod
    def get_node(cls, token_table_index):
        new_token_table_index, new_primary_expression = Operand.get_node(token_table_index)

        if new_primary_expression == None:
            return token_table_index, None

        new_token_table_index, new_expression_suffix = Suffix.get_node(new_token_table_index)

        if new_expression_suffix == None:
            return token_table_index, None

        token_table_index = new_token_table_index

        while new_expression_suffix != None:
            
            if isinstance(new_expression_suffix, ArgumentsSuffix):
                new_addressable = False
            else:
                new_addressable = new_primary_expression.addressable

            new_primary_expression = cls(new_addressable, new_primary_expression, new_expression_suffix)
            token_table_index, new_expression_suffix = Suffix.get_node(token_table_index)

        new_node = new_primary_expression

        return token_table_index, new_node