from .type_node import TypeNode
from dataclasses import dataclass
from ..identifiers.identifier_node import IdentifierNode
from ...lexic.tokens import token_table, TokenType, Token
from ...lexic.identifiers_and_types import identifier_tables, Type
from ..semantics_exception import SemanticsException



@dataclass
class BasicType(TypeNode):
    type_name: IdentifierNode

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        new_token_table_index, new_type_name = IdentifierNode.get_node(token_table_index)

        if new_type_name == None:
            return token_table_index, None
        
        new_node = cls(new_starting_token, new_type_name)

        new_node.check_semantics()

        return new_token_table_index, new_node

    def check_semantics(self):

        for table in reversed(identifier_tables):

            if self.type_name.identifier_name in table:

                if isinstance(table[self.type_name.identifier_name], Type):
                    return
                else:
                    raise SemanticsException(self.starting_token, "Identifier is not type!")
        
        raise SemanticsException(self.starting_token, "Undefined identifier!")

    def eval_type(self):
        
        if not hasattr(self, "_type"):

            for table in reversed(identifier_tables):

                if self.type_name.identifier_name in table:
                    
                    if isinstance(table[self.type_name.identifier_name], Type):
                        self._type = table[self.type_name.identifier_name]
                    else:
                        self._type = None
                        break

            if not hasattr(self, "_type"):
                self._type = None
        
        return self._type