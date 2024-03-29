from .simple_statement import SimpleStatement
from dataclasses import dataclass
from ....expressions.expression import Expression
from .....lexic.tokens import token_table



@dataclass
class ExpressionStatement(SimpleStatement):
    statement_expression: Expression

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_statement_expression = Expression.get_node(token_table_index)

        if new_statement_expression == None:
            return token_table_index, None
        
        token_table_index = new_token_table_index
        new_node = cls(new_starting_token, new_statement_expression)

        return token_table_index, new_node