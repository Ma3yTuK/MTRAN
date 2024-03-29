from .literal_node import LiteralNode
from dataclasses import dataclass
from ......identifiers.identifier_node import IdentifierNode
from ......node import Node
from ......expressions.expression import Expression
from ......type_nodes.type_node import TypeNode
from ......type_nodes.basic_type import Type
from typing import List
from .......lexic.tokens import token_table, Token, TokenType
from .......lexic.identifiers_and_types import UserType, ArrayTypeL
from .......lexic.operators_punctuation import PunctuationName
from ......syntaxis_exception import SyntaxisException
from ......semantics_exception import SemanticsException



@dataclass
class KeyedElement(Node):
    key: IdentifierNode | None
    value: Expression

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_key = IdentifierNode.get_node(token_table_index)

        if token_table[new_token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == PunctuationName.P_COLON:
            
            if new_key == None:
                raise SyntaxisException[token_table[token_table_index], "Keyed element without key!"]
            
            token_table_index = new_token_table_index
            token_table_index, new_value = Expression.get_node(token_table_index)

            if new_value == None:
                raise SyntaxisException(token_table[token_table_index], "Keyed element without value")

        else:
            new_token_table_index, new_value = Expression.get_node(token_table_index)

            if new_value == None:
                return token_table_index, None
        
            token_table_index = new_token_table_index
            
        new_node = cls(new_starting_token, new_key, new_value)

        return token_table_index, new_node


@dataclass
class LiteralValue(Node):
    elements: List[KeyedElement]

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        
        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACES_O:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_element = KeyedElement.get_node(token_table_index)
        new_elements: List[KeyedElement] = []

        if new_element != None:
            new_elements.append(new_element)

            while token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == PunctuationName.P_COMMA:
                token_table_index += 1
                token_table_index, new_element = KeyedElement.get_node(token_table_index)

                if new_element == None:
                    raise SyntaxisException(token_table[token_table_index], "Element expected!")
                
                new_elements.append(new_element)

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACES_C:
            raise SyntaxisException(token_table[token_table_index], "Closing brace expected!")

        token_table_index += 1
        new_node = cls(new_starting_token, new_elements)

        return token_table_index, new_node


@dataclass
class CompositLiteral(LiteralNode):
    literal_type: TypeNode
    literal_value: LiteralValue

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        try:
            new_token_table_index, new_literal_type = TypeNode.get_node(token_table_index)

            if new_literal_type == None:
                return token_table_index, None

            new_token_table_index, new_literal_value = LiteralValue.get_node(new_token_table_index)

            if new_literal_value == None:
                raise SyntaxisException(token_table[new_token_table_index], "Literal value expected!")

            token_table_index = new_token_table_index
            new_addressable = False
            new_node = cls(new_starting_token, new_addressable, new_literal_type, new_literal_value)
            new_node.check_semantics()

            return token_table_index, new_node

        except Exception:
            return token_table_index, None

    def check_semantics(self):

        if not isinstance(self.literal_type.eval_type(), UserType) and not isinstance(self.literal_type.eval_type(), ArrayTypeL):
            raise SemanticsException(self.literal_type.starting_token, "Composit type expected!")

    def eval_type(self):

        if not hasattr(self, "_type"):

            if isinstance(self.literal_type.eval_type(), UserType) or isinstance(self.literal_type.eval_type(), ArrayTypeL):
                self._type = self.literal_type.eval_type()
            else:
                self._type = None

        return self._type