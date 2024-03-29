from .statement import Statement
from dataclasses import dataclass
from ...node import Node
from ...type_nodes.type_node import TypeNode
from typing import List
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.operators_punctuation import PunctuationName
from ...syntaxis_exception import SyntaxisException
from ..top_level_statements.top_level_statement import TopLevelStatement



@dataclass
class StatementListNode(Node):
    statement_list: List[Statement]

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_statement_list: List[Statement] = []

        new_token_table_index, new_statement = Statement.get_node(token_table_index)

        if new_statement == None:
            return token_table_index, None

        token_table_index = new_token_table_index

        while new_statement != None:
            new_statement_list.append(new_statement)

            if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_SEMICOLON:
                raise SyntaxisException(token_table[token_table_index], "Unexpected symbol at the end of statement!")

            token_table_index += 1
            token_table_index, new_statement = Statement.get_node(token_table_index)

        new_node = cls(new_starting_token, new_statement_list)

        return token_table_index, new_node