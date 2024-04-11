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
from .......vm.commands import Commands, add_command, add_literal
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

        if isinstance(self.literal_type.eval_type(), UserType):

            for element in self.literal_value.elements:

                if element.key is None:
                    raise SemanticsException(element.key.starting_token, "Key expected!")

                if element.key.identifier_name not in self.literal_type.eval_type().fields:
                    raise SemanticsException(element.key.starting_token, "There is no such field!")
                
                if element.value.eval_type() != self.literal_type.eval_type().fields[element.key.identifier_name].field_type:
                    raise SemanticsException(element.key.starting_token, "Incompatible type!")
        
        if isinstance(self.literal_type.eval_type(), ArrayTypeL):

            for index, element in enumerate(self.literal_value.elements):

                if element.key is not None:
                    raise SemanticsException(element.key.starting_token, "Keyed elements are not allowed here!")

                if index >= self.literal_type.eval_type().size:
                    raise SemanticsException(element.key.starting_token, "Too many keys!")
                
                if element.value.eval_type() != self.literal_type.eval_type().value_type:
                    raise SemanticsException(element.key.starting_token, "Incompatible type!")

    def eval_type(self):

        if not hasattr(self, "_type"):

            if isinstance(self.literal_type.eval_type(), UserType) or isinstance(self.literal_type.eval_type(), ArrayTypeL):
                self._type = self.literal_type.eval_type()
            else:
                self._type = None

        return self._type

    def gen_code(self):
        value_type = self.eval_type()

        if isinstance(value_type, UserType):
            fields = dict(value_type.fields)

            for element in self.literal_value.elements:
                fields.pop(element.key.identifier_name)
                element.value.gen_code()
                add_command(Commands.RMS)

            for current_field in value_type.fields.values():
                in_keys = False
                
                for element in self.literal_value.elements:

                    if element.key == current_field.field_name:
                        element.value.gen_code()
                        in_keys = True
                        break
                
                if not in_keys:
                    add_command(Commands.LD)
                    add_literal(bytes(current_field.field_type.size), current_field.field_type)

                add_command(Commands.RMS)
        
        if isinstance(value_type, ArrayTypeL):
            index = 0
            
            for element in self.literal_value.elements:
                element.value.gen_code()
                add_command(Commands.RMS)
                index += 1

            while index != value_type.count:
                add_command(Commands.LD)
                add_literal(bytes(value_type.value_type.size), value_type.value_type)
                add_command(Commands.RMS)
                index += 1

        add_command(Commands.LDP)
        add_literal(bytes(), value_type)