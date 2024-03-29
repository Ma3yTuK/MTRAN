from ..node import Node
from dataclasses import dataclass
from ...lexic.tokens import token_table, Token, TokenType
from ...lexic.identifiers_and_types import identifier_tables



@dataclass
class IdentifierNode(Node):
    identifier_name: str

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.identifier:
            return token_table_index, None
        
        new_node = cls(new_starting_token, token_table[token_table_index].name)
        token_table_index += 1

        return token_table_index, new_node

    def __str__(self):
        return f"{self.__class__.__name__}({self.identifier_name})\n"