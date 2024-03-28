from .literal_node import LiteralNode
from dataclasses import dataclass
from .......lexic.tokens import token_table, Token, TokenType
from .......lexic.literals import literals



@dataclass
class BasicLiteral(LiteralNode):
    literal_name: str

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.literal:
            return token_table_index, None
        
        new_addressable = False
        new_node = cls(new_addressable, token_table[token_table_index].name)
        token_table_index += 1

        return token_table_index, new_node

    def eval_type(self):
        
        if not hasattr(self, "__type"):
            if self.literal_name in literals:
                self.__type = literals[self.literal_name].value_type

            if not hasattr(self, "__type"):
                self.__type = None

        return self.__type

    def __str__(self):
        return self.__class__.__name__ + '(' + self.literal_name + ')\n'