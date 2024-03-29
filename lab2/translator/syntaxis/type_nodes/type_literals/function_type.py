from .type_literal import TypeLiteral
from dataclasses import dataclass
from ..type_node import TypeNode
from ...node import Node
from ...identifiers.identifier_list import IdentifierListNode
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.identifiers_and_types import FunctionTypeL
from typing import List
from ...syntaxis_exception import SyntaxisException
from ....lexic.operators_punctuation import PunctuationName
from ....lexic.keywords import KeywordName



@dataclass
class ParameterDeclaration(Node):
    fields: IdentifierListNode | None
    fields_type: TypeNode

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_fields = IdentifierListNode.get_node(token_table_index)
        new_token_table_index, new_fields_type = TypeNode.get_node(new_token_table_index)

        if new_fields_type == None:

            if new_fields != None:
                raise SyntaxisException(token_table[token_table_index], "Expected type")

            return token_table_index, None

        new_node = cls(new_starting_token, new_fields, new_fields_type)
        return new_token_table_index, new_node

    def eval_type(self):

        if not hasattr(self, "_type"):
            self._type = [self.fields_type.eval_type()]

            if self.fields != None:
                self._type *= len(self.fields.identifier_list)

        return self._type
        

@dataclass
class ParameterList(Node):
    parameters: List[ParameterDeclaration]

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_PARENTHESES_O:
            return token_table_index, None

        new_parameters: List[ParameterDeclaration] = []

        token_table_index += 1
        token_table_index, new_parameter = ParameterDeclaration.get_node(token_table_index)

        if new_parameter != None:
            new_parameters.append(new_parameter)

            while token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == PunctuationName.P_COMMA:
                token_table_index += 1
                token_table_index, new_parameter = ParameterDeclaration.get_node(token_table_index)

                if new_parameter == None:
                    raise SyntaxisException(token_table[token_table_index], "Parameter list expected!")
                
                new_parameters.append(new_parameter)
        
        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_PARENTHESES_C:
            raise SyntaxisException(token_table[token_table_index], "Closing parenthesis expected!")

        token_table_index += 1
        new_node = cls(new_starting_token, new_parameters)

        return token_table_index, new_node
    
    def eval_type(self):

        if not hasattr(self, "_type"):
            self._type = []

            for parameter in self.parameters:
                self._type += parameter.eval_type()

        return self._type

        
@dataclass
class Signature(Node):
    parameters: ParameterList
    result: TypeNode | None

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_parameters = ParameterList.get_node(token_table_index)

        if new_parameters == None:
            return token_table_index, None

        token_table_index = new_token_table_index
        token_table_index, new_result = TypeNode.get_node(token_table_index)
        new_node = cls(new_starting_token, new_parameters, new_result)

        return token_table_index, new_node

    def eval_type(self):

        if not hasattr(self, "_type"):
            parameters_types = self.parameters.eval_type()

            if self.result != None:
                result_type = self.result.eval_type()
            else:
                result_type = None

            self._type = FunctionTypeL(parameters_types, result_type)

        return self._type


@dataclass
class FuncType(TypeLiteral):
    signature: Signature

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_FUNC:
            return token_table_index, None
            
        token_table_index += 1
        token_table_index, new_signature = Signature.get_node(token_table_index)

        if new_signature == None:
            raise SyntaxisException(token_table[token_table_index], "Signature expected!")
        
        new_node = cls(new_starting_token, new_signature)

        return token_table_index, new_node

    def eval_type(self):

        if not hasattr(self, "_type"):
            self._type = self.signature.eval_type()

        return self._type