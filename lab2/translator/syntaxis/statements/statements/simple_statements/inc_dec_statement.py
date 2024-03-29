from .simple_statement import SimpleStatement
from ....node import Node
from ....expressions.expression import Expression
from dataclasses import dataclass
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.operators_punctuation import OperatorName, PunctuationName, assignment_operators
from .....lexic.identifiers_and_types import IntegerNumbericType
from ....syntaxis_exception import SyntaxisException
from ....semantics_exception import SemanticsException


@dataclass
class IncDecOperator(Node):
    operator: str

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name not in {OperatorName.O_INCREMENT, OperatorName.O_DECREMENT}:
            return token_table_index, None
        
        new_operator = token_table[token_table_index].name
        token_table_index += 1
        new_node = cls(new_starting_token, new_operator)

        return token_table_index, new_node


@dataclass
class IncDecStatement(SimpleStatement):
    expression: Expression
    operator: IncDecOperator

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_expression = Expression.get_node(token_table_index)

        if new_expression == None:
            return token_table_index, None

        new_token_table_index, new_operator = IncDecOperator.get_node(new_token_table_index)

        if new_operator == None:
            return token_table_index, None

        if new_expression.addressable == False:
            raise SyntaxisException(token_table[token_table_index], "Expression must be addressable here")

        token_table_index = new_token_table_index
        new_node = cls(new_starting_token, new_expression, new_operator)
        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):

        if not isinstance(self.expression.eval_type(), IntegerNumbericType):
            raise SemanticsException(self.expression.starting_token, "Expression type must be int!")