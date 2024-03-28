from .identifier_node import IdentifierNode
from dataclasses import dataclass
from .......lexic.tokens import token_table, Token, TokenType
from .......lexic.identifiers_and_types import identifier_tables



@dataclass
class BasicIdentifier(IdentifierNode):
    identifier_name: str

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.identifier:
            return token_table_index, None
        
        new_addressable = True
        new_node = cls(new_addressable, token_table[token_table_index].name)
        token_table_index += 1

        return token_table_index, new_node

    def eval_type(self):

        if not hasattr(self, "__type"):

            for table in reversed(identifier_tables):

                if self.identifier_name in table:
                    self.__type = table[self.identifier_name].value_type
                    break

            if not hasattr(self, "__type"):
                self.__type = None
        
        return self.__type

    def __str__(self):
        return self.__class__.__name__ + '(' + self.identifier_name + ')\n'