from .simple_statement import SimpleStatement
from ....node import Node
from ....expressions.expression_list import ExpressionListNode
from dataclasses import dataclass
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.operators_punctuation import OperatorName, PunctuationName, assignment_operators
from .....lexic.identifiers_and_types import identifier_tables, NumericType
from ....syntaxis_exception import SyntaxisException
from ....semantics_exception import SemanticsException


@dataclass
class AssignmentOperator(Node):
    operator: str | None

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index = token_table_index

        if token_table[new_token_table_index].token_type == TokenType.operator and token_table[new_token_table_index].name in assignment_operators:
            new_token_table_index += 1
            new_operator = token_table[token_table_index].name
        else:
            new_operator = None

        if token_table[new_token_table_index].token_type != TokenType.operator or token_table[new_token_table_index].name != OperatorName.O_ASS:
            return token_table_index, None
        
        new_token_table_index += 1
        token_table_index = new_token_table_index
        new_node = cls(new_starting_token, new_operator)

        return token_table_index, new_node


@dataclass
class AssignmentStatement(SimpleStatement):
    expression_list1: ExpressionListNode
    assignment_operator: AssignmentOperator
    expression_list2: ExpressionListNode

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
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

        new_node = cls(new_starting_token, new_expression_list1, new_assignment_operator, new_expression_list2)
        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):

        for i, expression in enumerate(self.expression_list1.expression_list):

            if not (isinstance(expression.eval_type(), NumericType) and isinstance(self.expression_list2.expression_list[i].eval_type(), NumericType)):

                if self.assignment_operator.operator != None:
                    raise SemanticsException(self.expression_list2.expression_list[i].starting_token, "Invalid type!")
                
                if expression.eval_type() != self.expression_list2.expression_list[i].eval_type():
                    raise SemanticsException(self.expression_list2.expression_list[i].starting_token, "Invalid type!")