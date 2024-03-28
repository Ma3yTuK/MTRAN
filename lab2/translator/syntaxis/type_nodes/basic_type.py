from .type_node import TypeNode
from dataclasses import dataclass
from ..expressions.unary_expressions.primary_expressions.operands.identifiers.identifier_node import IdentifierNode
from ...lexic.tokens import token_table, TokenType, Token
from ...lexic.identifiers_and_types import identifier_tables, MetaType
from ..semantics_exception import SemanticsException



@dataclass
class BasicType(TypeNode):
    type_name: IdentifierNode

    @classmethod
    def get_node(cls, token_table_index):

        new_token_table_index, new_type_name = IdentifierNode.get_node(token_table_index)

        if new_type_name == None:
            return token_table_index, None
        
        token_table_index = new_token_table_index
        new_node = cls(token_table[token_table_index], new_type_name)
        new_node.check_sematrics()

        return token_table_index, new_node

    def check_sematrics(self):

        if not isinstance(self.type_name.eval_type(), MetaType):
            raise SemanticsException(self.starting_token, "Type name expected!")

    def eval_type(self):

        if not hasattr(self, "__type"):

            if isinstance(self.type_name.eval_type(), MetaType):
                self.__type = self.type_name.eval_type().u_type
            else:
                self.__type = None
        
        return self.__type