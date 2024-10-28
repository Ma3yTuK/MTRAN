from ...statements.declarations.declaration import Declaration
from ...top_level_statements.top_level_declarations.top_level_declaration import TopLevelDeclaration
from ....node import Node
from dataclasses import dataclass
from ....identifiers.identifier_node import IdentifierNode
from ....type_nodes.type_node import TypeNode
from typing import List
from .....lexic.tokens import token_table, Token, TokenType
from ....syntaxis_exception import SyntaxisException
from ....semantics_exception import SemanticsException
from .....lexic.keywords import KeywordName
from .....lexic.operators_punctuation import PunctuationName
from .....lexic.identifiers_and_types import identifier_tables



@dataclass
class TypeSpec(Node):
    spec_identifier: IdentifierNode
    spec_type: TypeNode

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_spec_identifier = IdentifierNode.get_node(token_table_index)

        if new_spec_identifier == None:
            return token_table_index, None
        
        token_table_index = new_token_table_index
        token_table_index, new_spec_type = TypeNode.get_node(token_table_index)

        if new_spec_type == None:
            raise SyntaxisException(token_table[token_table_index], "Type expected!")

        new_node = cls(new_starting_token, new_spec_identifier, new_spec_type)
        new_node.check_semantics()

        return token_table_index, new_node
    
    def check_semantics(self):
        
        if self.spec_identifier.identifier_name in identifier_tables[-1]:
            raise SemanticsException(self.spec_identifier.starting_token, "Name already exists!")
        else:
            identifier_tables[-1][self.spec_identifier.identifier_name] = self.spec_type.eval_type()


@dataclass
class TypeDeclaration(Declaration, TopLevelDeclaration):
    type_specs: List[TypeSpec]

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        
        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_TYPE:
            return token_table_index, None

        token_table_index += 1
        
        if token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == PunctuationName.P_PARENTHESES_O:
            parenthesis = True
            token_table_index += 1
        else:
            parenthesis = False

        new_token_table_index, new_type_spec = TypeSpec.get_node(token_table_index)
        
        if new_type_spec == None:
            raise SyntaxisException(token_table[token_table_index], "Type spec expected!")
        
        token_table_index = new_token_table_index
        new_type_specs: List[TypeSpec] = [new_type_spec]

        if parenthesis:

            if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_SEMICOLON:
                raise SyntaxisException(token_table[token_table_index], "Unexpected symbol at the end of type declaration!")
            
            token_table_index += 1

            while token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_PARENTHESES_C:
                token_table_index, new_type_spec = TypeSpec.get_node(token_table_index)

                if new_type_spec == None:
                    raise SyntaxisException(token_table[token_table_index], "Type spec expected!")

                new_type_specs.append(new_type_spec)

                if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_SEMICOLON:
                    raise SyntaxisException(token_table[token_table_index], "Unexpected symbol at the end of type declaration!")

                token_table_index += 1

            token_table_index += 1
        
        new_node = cls(new_starting_token, new_type_specs)

        return token_table_index, new_node