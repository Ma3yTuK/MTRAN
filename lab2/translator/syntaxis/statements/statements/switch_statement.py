from .statement import Statement
from dataclasses import dataclass
from ...expressions.expression import Expression
from .statement_list import StatementListNode
from typing import List, Dict
from ...node import Node
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.keywords import KeywordName
from ....lexic.identifiers_and_types import Identifier
from ...syntaxis_exception import SyntaxisException
from ....lexic.operators_punctuation import PunctuationName



@dataclass
class ExpressionCaseClause(Node):
    case_expression: Expression | None # None when default
    body: StatementListNode

    @classmethod
    def get_node(cls, token_table_index):
        is_default_clause = token_table[token_table_index].name == KeywordName.K_DEFAULT

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_CASE and not is_default_clause:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_case_expression = Expression.get_node(token_table_index)
        is_expression_present = new_case_expression != None

        if is_expression_present == is_default_clause:
            raise SyntaxisException(token_table[token_table_index], "Unexpected symbol")

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_COLON:
            raise SyntaxisException(token_table[token_table_index], "Colon expected")

        token_table_index += 1
        token_table_index, new_body = StatementListNode.get_node(token_table_index)

        if new_body == None:
            raise SyntaxisException(token_table[token_table_index], "Case body expected")

        new_node = cls(new_case_expression, new_body)

        return new_node


@dataclass
class SwitchStatement(Statement):
    switch_expression: Expression
    cases: List[ExpressionCaseClause]
    identifier_table: Dict[str, Identifier]

    @classmethod
    def get_node(cls, token_table_index):
        
        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_SWITCH:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_switch_expression = Expression.get_node(token_table_index)

        if new_switch_expression == None:
            raise SyntaxisException(token_table[token_table_index], "Expression expected")

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACES_O:
            raise SyntaxisException(token_table[token_table_index], "Opening brace expected")

        token_table_index += 1
        token_table_index, new_case = ExpressionCaseClause.get_node(token_table_index)

        if new_case == None:
            raise SyntaxisException(token_table[token_table_index], "Case expected")

        new_cases: List[ExpressionCaseClause] = [new_case]

        while new_case != None:
            token_table_index, new_case = ExpressionCaseClause.get_node(token_table_index)
            new_cases.append(new_case)

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACES_C:
            raise SyntaxisException(token_table[token_table_index], "Closing brace expected")

        token_table_index += 1
        new_node = cls(new_switch_expression, new_cases)

        return token_table_index, new_node