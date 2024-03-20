from .suffix import Suffix
from dataclasses import dataclass
from ..expressions.expression import Expression
from ...lexic.tokens import token_table, Token, TokenType
from ...lexic.operators_punctuation import PunctuationName
from ..syntaxis_exception import SyntaxisException



@dataclass
class IndexSuffix(Suffix):
    index_expression: Expression

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACKETS_O:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_index_expression = Expression.get_node(token_table_index)

        if new_index_expression == None:
            raise SyntaxisException(token_table[token_table_index], "Expected expression!")

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACKETS_C:
            raise SyntaxisException(token_table[token_table_index], "Closing bracket expected!")

        token_table_index += 1
        new_node = cls(new_index_expression)

        return token_table_index, new_node