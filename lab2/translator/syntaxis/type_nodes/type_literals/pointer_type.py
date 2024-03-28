from .type_literal import TypeLiteral
from dataclasses import dataclass
from ..type_node import TypeNode
from ...node import Node
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.operators_punctuation import OperatorName
from ....lexic.identifiers_and_types import PointerTypeL
from ...expressions.unary_expressions.primary_expressions.operands.identifiers.identifier_list import IdentifierListNode
from typing import List
from ...syntaxis_exception import SyntaxisException



@dataclass
class PointerType(Node):
    underlying_type: TypeNode

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != OperatorName.O_MUL_OR_REF:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_underlying_type = TypeNode.get_node(token_table_index)

        if new_underlying_type == None:
            raise SyntaxisException(token_table[token_table_index], "Expected type")

        new_node = cls(new_underlying_type)

        return token_table_index, new_node

    def eval_type(self):
        
        if not hasattr(self, "__type"):
            self.__type = PointerTypeL(self.underlying_type.eval_type())

        return self.__type