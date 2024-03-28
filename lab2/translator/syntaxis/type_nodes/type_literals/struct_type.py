from .type_literal import TypeLiteral
from dataclasses import dataclass
from ..type_node import TypeNode
from ...node import Node
from ...expressions.unary_expressions.primary_expressions.operands.identifiers.identifier_list import IdentifierListNode
from typing import List
from ....lexic.tokens import token_table, Token, TokenType
from ...syntaxis_exception import SyntaxisException
from ....lexic.keywords import KeywordName
from ....lexic.operators_punctuation import PunctuationName
from ....lexic.identifiers_and_types import UserType



@dataclass
class FieldDeclaration(Node):
    fields: IdentifierListNode
    fields_type: TypeNode

    @classmethod
    def get_node(cls, token_table_index):
        new_token_table_index, new_fields = IdentifierListNode.get_node(token_table_index)

        if new_fields == None:
            return token_table_index, None

        token_table_index = new_token_table_index
        token_table_index, new_fields_type = TypeNode.get_node(token_table_index)

        if new_fields_type == None:
            raise SyntaxisException(token_table[token_table_index], "Type expected")
        
        new_node = cls(new_fields, new_fields_type)

        return token_table_index, new_node
    
    def eval_type(self):

        if not hasattr(self, "__type"):
            self.__type = {}
            field_type = self.fields_type.eval_type()

            for name in self.fields.identifier_list:
                self.__type[name] = UserType.TypeField(name, field_type)

        return self.__type


@dataclass
class StructBody(Node):
    declarations: List[FieldDeclaration]

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACES_O:
            return token_table_index, None

        token_table_index += 1
        new_declarations: List[FieldDeclaration] = []

        while token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACES_C:
            token_table_index, new_declaration = FieldDeclaration.get_node(token_table_index)

            if new_declaration == None:
                raise SyntaxisException(token_table[token_table_index], "Field declaration expected!")

            new_declarations.append(new_declaration)

            if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_SEMICOLON:
                raise SyntaxisException(token_table[token_table_index], "Unexpected symbol at the end of field declaration!")

            token_table_index += 1

        if not new_declarations:
            raise SyntaxisException(token_table[token_table_index], "Struct cannot be blank!")

        token_table_index += 1
        new_node = cls(new_declarations)

        return token_table_index, new_node
    
    def eval_type(self):

        if not hasattr(self, "__type"):
            self.__type = {}

            for declaration in self.declarations:
                self.__type |= declaration.eval_type()

        return self.__type


@dataclass
class StructType(TypeLiteral):
    body: StructBody

    @classmethod
    def get_node(cls, token_table_index):
        
        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_STRUCT:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_body = StructBody.get_node(token_table_index)

        if new_body == None:
            raise SyntaxisException(token_table[token_table_index], "Expected struct body!")

        new_node = cls(new_body)

        return token_table_index, new_node
    
    def eval_type(self):

        if not hasattr(self, "__type"):
            self.__type = self.body.eval_type()

        return self.__type