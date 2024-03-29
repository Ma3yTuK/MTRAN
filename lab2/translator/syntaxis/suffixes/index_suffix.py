from .suffix import Suffix
from dataclasses import dataclass
from ..expressions.expression import Expression
from ...lexic.tokens import token_table, Token, TokenType
from ...lexic.operators_punctuation import PunctuationName
from ...lexic.identifiers_and_types import IntegerNumbericType
from ..syntaxis_exception import SyntaxisException
from ..semantics_exception import SemanticsException



@dataclass
class IndexSuffix(Suffix):
    index_expression: Expression

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACKETS_O:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_index_expression = Expression.get_node(token_table_index)

        if new_index_expression == None:
            raise SyntaxisException(token_table[token_table_index], "Expected expression!")

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACKETS_C:
            raise SyntaxisException(token_table[token_table_index], "Closing bracket expected!")

        token_table_index += 1
        new_node = cls(new_starting_token, new_index_expression)
        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):

        if not isinstance(self.index_expression.eval_type(), IntegerNumbericType):
            raise SemanticsException(self.index_expression.starting_token, "Integer expression expected!")