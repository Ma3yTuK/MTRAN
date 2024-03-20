from .simple_statement import SimpleStatement
from ....node import Node
from ....expressions.expression_list import ExpressionListNode
from dataclasses import dataclass
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.operators_punctuation import OperatorName, PunctuationName, assignment_operators
from ....syntaxis_exception import SyntaxisException


@dataclass
class AssignmentOperator(Node):
    operator: str

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name not in assignment_operators:
            return token_table_index, None
        
        new_operator = token_table[token_table_index].name
        token_table_index += 1
        new_node = cls(new_operator)

        return token_table_index, new_node


@dataclass
class AssignmentStatement(SimpleStatement):
    expression_list1: ExpressionListNode
    assignment_operator: AssignmentOperator
    expression_list2: ExpressionListNode

    @classmethod
    def get_node(cls, token_table_index):
        new_token_table_index, new_expression_list1 = ExpressionListNode.get_node(token_table_index)

        if new_expression_list1 == None:
            return token_table_index, None

        new_token_table_index, new_assignment_operator = AssignmentOperator.get_node(new_token_table_index)

        if new_assignment_operator == None:
            return token_table_index, None

        if new_expression_list1.addressable == False:
            raise SyntaxisException(token_table[token_table_index], "Expression must be addressable here!")

        token_table_index = new_token_table_index
        token_table_index, new_expression_list2 = ExpressionListNode.get_node(token_table_index)

        if new_expression_list2 == None:
            raise SyntaxisException(token_table[token_table_index], "Expression list expected!")

        if len(new_expression_list1.expression_list) != len(new_expression_list2.expression_list):
            raise SyntaxisException(token_table[token_table_index], "Parts of assignment have different length!")

        new_node = cls(new_expression_list1, new_assignment_operator, new_expression_list2)

        return token_table_index, new_node
        