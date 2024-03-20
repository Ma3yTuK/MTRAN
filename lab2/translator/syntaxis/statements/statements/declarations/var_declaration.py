from ...statements.declarations.declaration import Declaration
from ...top_level_statements.top_level_declarations.top_level_declaration import TopLevelDeclaration
from ....node import Node
from dataclasses import dataclass
from ....expressions.unary_expressions.primary_expressions.operands.identifiers.identifier_list import IdentifierListNode
from ....expressions.expression_list import ExpressionListNode
from ....type_nodes.type_node import TypeNode
from typing import List
from .....lexic.tokens import token_table, Token, TokenType
from ....syntaxis_exception import SyntaxisException
from .....lexic.keywords import KeywordName
from .....lexic.operators_punctuation import PunctuationName, OperatorName
from ...base_var_declaration import BaseVarDeclaration



@dataclass
class VarSpec(Node):
    spec_identifiers: IdentifierListNode
    spec_type: TypeNode | None
    spec_expressions: ExpressionListNode | None

    @classmethod
    def get_node(cls, token_table_index):
        new_token_table_index, new_spec_identifiers = IdentifierListNode.get_node(token_table_index)

        if new_spec_identifiers == None:
            return token_table_index, None
        
        token_table_index = new_token_table_index
        token_table_index, new_spec_type = TypeNode.get_node(token_table_index)

        if token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == OperatorName.O_ASS:
            token_table_index += 1
            token_table_index, new_spec_expressions = ExpressionListNode.get_node(token_table_index)

            if new_spec_expressions == None:
                raise SyntaxisException(token_table[token_table_index], "List of expressions expected!")

            if len(new_spec_expressions.expression_list) != len(new_spec_identifiers.identifier_list):
                raise SyntaxisException(token_table[token_table_index], "Variable declaration lists have different sizes!")
        else:
            new_spec_expressions = None

        new_node = cls(new_spec_identifiers, new_spec_type, new_spec_expressions)

        return token_table_index, new_node


@dataclass
class VarDeclaration(Declaration, TopLevelDeclaration, BaseVarDeclaration):
    var_specs: List[VarSpec]

    @classmethod
    def get_node(cls, token_table_index):
        
        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_VAR:
            return token_table_index, None

        token_table_index += 1
        
        if token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == PunctuationName.P_PARENTHESES_O:
            parenthesis = True
            token_table_index += 1
        else:
            parenthesis = False

        new_token_table_index, new_var_spec = VarSpec.get_node(token_table_index)
        
        if new_var_spec == None:
            raise SyntaxisException(token_table[token_table_index], "Var spec expected!")
        
        token_table_index = new_token_table_index
        new_var_specs: List[TypeSpec] = [new_var_spec]

        if parenthesis:

            while token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == PunctuationName.P_COMMA:
                token_table_index += 1
                token_table_index, new_var_spec = VarSpec.get_node(token_table_index)

                if new_var_spec == None:
                    raise SyntaxisException(token_table[token_table_index], "Var spec expected!")

                new_var_specs.append(new_var_spec)

            if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_PARENTHESES_C:
                raise SyntaxisException(token_table[token_table_index], "Closing parenthesis expected!")

            token_table_index += 1
        
        new_node = cls(new_var_specs)

        return token_table_index, new_node