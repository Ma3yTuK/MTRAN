from .suffix import Suffix
from dataclasses import dataclass
from ..identifiers.identifier_node import IdentifierNode
from ...lexic.tokens import token_table, Token, TokenType
from ...lexic.operators_punctuation import OperatorName
from ..syntaxis_exception import SyntaxisException



@dataclass
class SelectorSuffix(Suffix):
    operand_identifier: IdentifierNode

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != OperatorName.O_PERIOD:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_operand_identifier = IdentifierNode.get_node(token_table_index)

        if new_operand_identifier == None:
            raise SyntaxisException(token_table[token_table_index], "Expected identifier!")

        new_node = cls(new_starting_token, new_operand_identifier)

        return token_table_index, new_node