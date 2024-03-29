from .statement import Statement
from dataclasses import dataclass
from ...expressions.expression import Expression
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.keywords import KeywordName



@dataclass
class ReturnStatement(Statement):
    value: Expression | None

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_RETURN:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_value = Expression.get_node(token_table_index)
        new_node = cls(new_starting_token, new_value)

        return token_table_index, new_node