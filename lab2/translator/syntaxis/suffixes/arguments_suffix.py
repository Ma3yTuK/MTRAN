from .suffix import Suffix
from dataclasses import dataclass
from ..expressions.expression_list import ExpressionListNode
from ...lexic.tokens import token_table, Token, TokenType
from ...lexic.operators_punctuation import PunctuationName
from ...vm.commands import Commands, add_command, add_reference
from ..syntaxis_exception import SyntaxisException



@dataclass
class ArgumentsSuffix(Suffix):
    arguments_expressions: ExpressionListNode | None

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_PARENTHESES_O:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_arguments_expressions = ExpressionListNode.get_node(token_table_index)

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_PARENTHESES_C:
            raise SyntaxisException(new_starting_token, "Closing paranthesis expected!")

        token_table_index += 1
        new_node = cls(token_table[token_table_index], new_arguments_expressions)

        return token_table_index, new_node
