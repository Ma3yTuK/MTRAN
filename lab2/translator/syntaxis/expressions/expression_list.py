from .expression import Expression
from dataclasses import dataclass
from ..node import Node
from ...lexic.operators_punctuation import PunctuationName
from ...lexic.tokens import token_table, Token, TokenType
from ..syntaxis_exception import SyntaxisException
from typing import List



@dataclass
class ExpressionListNode(Node):
    addressable: bool
    expression_list: List[Expression]

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_expression_list: List[Expression] = []

        new_token_table_index, new_expression = Expression.get_node(token_table_index)

        if new_expression == None:
            return token_table_index, None

        new_addressable = new_expression.addressable

        token_table_index = new_token_table_index
        new_expression_list.append(new_expression)

        while token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == PunctuationName.P_COMMA:
            token_table_index += 1
            token_table_index, new_expression = Expression.get_node(token_table_index)

            if new_expression == None:
                raise SyntaxisException(token_table[token_table_index], "Parameter list expected!")

            new_addressable = new_addressable and new_expression.addressable
            new_expression_list.append(new_expression)

        new_node = cls(new_starting_token, new_addressable, new_expression_list)

        return token_table_index, new_node
