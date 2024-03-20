from ..declarations.var_declaration import VarDeclaration
from ..simple_statements.simple_statement import SimpleStatement
from dataclasses import dataclass
from ...base_var_declaration import BaseVarDeclaration
from ....expressions.unary_expressions.primary_expressions.operands.identifiers.identifier_list import IdentifierListNode
from ....expressions.expression_list import ExpressionListNode
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.operators_punctuation import OperatorName, PunctuationName
from ....syntaxis_exception import SyntaxisException



@dataclass
class SimpleVarDeclaration(SimpleStatement, BaseVarDeclaration):
    identifiers: IdentifierListNode
    values: ExpressionListNode

    @classmethod
    def get_node(cls, token_table_index):
        new_token_table_index, new_identifiers = IdentifierListNode.get_node(token_table_index)

        if new_identifiers == None or token_table[new_token_table_index].token_type != TokenType.operator or token_table[new_token_table_index].name != OperatorName.O_INIT:
            return token_table_index, None

        token_table_index = new_token_table_index + 1
        token_table_index, new_values = ExpressionListNode.get_node(token_table_index)

        if new_values == None:
            raise SyntaxisException(token_table[token_table_index], "Expression list expected!")

        if len(new_identifiers.identifier_list) != len(new_values.expression_list):
            raise SyntaxisException(token_table[token_table_index], "Declaration parts have different length!")

        new_node = cls(new_identifiers, new_values)

        return token_table_index, new_node