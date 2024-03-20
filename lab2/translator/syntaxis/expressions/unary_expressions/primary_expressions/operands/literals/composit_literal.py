from .literal_node import LiteralNode
from dataclasses import dataclass
from ..identifiers.identifier_node import IdentifierNode
from ......node import Node
from ......expressions.expression import Expression
from ......type_nodes.type_node import TypeNode
from ......type_nodes.basic_type import BasicType
from typing import List
from .......lexic.tokens import token_table, Token, TokenType
from ......syntaxis_exception import SyntaxisException
from .......lexic.operators_punctuation import PunctuationName



@dataclass
class KeyedElement(Node):
    key: IdentifierNode | None
    value: Expression

    @classmethod
    def get_node(cls, token_table_index):
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
            
        new_node = cls(new_key, new_value)

        return token_table_index, new_node


@dataclass
class LiteralValue(Node):
    elements: List[KeyedElement]

    @classmethod
    def get_node(cls, token_table_index):
        
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
        new_node = cls(new_elements)

        return token_table_index, new_node


@dataclass
class CompositLiteral(LiteralNode):
    literal_type: TypeNode
    literal_value: LiteralValue

    @classmethod
    def get_node(cls, token_table_index):
        new_token_table_index, new_literal_type = TypeNode.get_node(token_table_index)

        if new_literal_type == None:
            return token_table_index, None

        new_token_table_index, new_literal_value = LiteralValue.get_node(new_token_table_index)

        if new_literal_value == None:

            if isinstance(new_literal_type, BasicType):
                return token_table_index, None

            raise SyntaxisException(token_table[new_token_table_index], "Literal value expected!")

        token_table_index = new_token_table_index
        new_addressable = False
        new_node = cls(new_addressable, new_literal_type, new_literal_value)

        return token_table_index, new_node