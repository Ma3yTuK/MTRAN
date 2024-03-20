from .......lexic.tokens import token_table, TokenType
from .......lexic.operators_punctuation import PunctuationName
from ......node import Node
from dataclasses import dataclass
from typing import List
from .identifier_node import IdentifierNode
from .......lexic.identifiers_and_types import Identifier



@dataclass
class IdentifierListNode(Node):
    addressable: bool
    identifier_list: List[IdentifierNode]

    @classmethod
    def get_node(cls, token_table_index):
        new_identifier_list: List[IdentifierNode] = []

        new_token_table_index, new_identifier = IdentifierNode.get_node(token_table_index)

        if new_identifier == None:
            return token_table_index, None

        token_table_index = new_token_table_index
        new_identifier_list.append(new_identifier)

        while token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == PunctuationName.P_COMMA:
            token_table_index += 1
            token_table_index, new_identifier = IdentifierNode.get_node(token_table_index)

            if new_identifier == None:
                raise SyntaxisException(token_table[token_table_index], "Identifier expected!")
            
            new_identifier_list.append(new_identifier)

        new_addressable = True
        new_node = cls(new_addressable, new_identifier_list)

        return token_table_index, new_node