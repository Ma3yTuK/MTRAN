from .simple_statement import SimpleStatement
from dataclasses import dataclass
from ....expressions.expression import Expression



@dataclass
class ExpressionStatement(SimpleStatement):
    statement_expression: Expression

    @classmethod
    def get_node(cls, token_table_index):
        new_token_table_index, new_statement_expression = Expression.get_node(token_table_index)

        if new_statement_expression == None:
            return token_table_index, None
        
        token_table_index = new_token_table_index
        new_node = cls(new_statement_expression)

        return token_table_index, new_node