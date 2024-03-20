from .type_node import TypeNode
from dataclasses import dataclass
from ..expressions.unary_expressions.primary_expressions.operands.identifiers.identifier_node import IdentifierNode
from ...lexic.tokens import token_table, TokenType, Token



@dataclass
class BasicType(TypeNode):
    type_name: IdentifierNode

    @classmethod
    def get_node(cls, token_table_index):

        new_token_table_index, new_type_name = IdentifierNode.get_node(token_table_index)

        if new_type_name == None:
            return token_table_index, None
        
        token_table_index = new_token_table_index
        new_node = cls(new_type_name)

        return token_table_index, new_node