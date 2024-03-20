from .type_literal import TypeLiteral
from dataclasses import dataclass
from ...expressions.expression import Expression
from ....lexic.tokens import token_table, TokenType, Token
from ..type_node import TypeNode
from ....lexic.operators_punctuation import PunctuationName
from ...syntaxis_exception import SyntaxisException



@dataclass
class ArrayType(TypeLiteral):
    count: Expression
    element_type: TypeNode

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACKETS_O:
            return token_table_index, None

        token_table_index += 1
        new_token_table_index, new_count = Expression.get_node(token_table_index)

        if new_count == None:
            raise SyntaxisException(token_table[token_table_index], "Expected expression!")

        token_table_index = new_token_table_index

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACKETS_C:
            raise SyntaxisException(token_table[token_table_index], "Closing bracket expected!")

        token_table_index += 1
        new_token_table_index, new_element_type = TypeNode.get_node(token_table_index)

        if new_element_type == None:
            raise SyntaxisException(token_table[token_table_index], "Undefined type!")

        new_node = cls(new_count, new_element_type)
        return new_token_table_index, new_node