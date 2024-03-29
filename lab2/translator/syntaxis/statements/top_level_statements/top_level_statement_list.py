from .top_level_statement import TopLevelStatement
from dataclasses import dataclass
from ...node import Node
from ...type_nodes.type_node import TypeNode
from typing import List
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.operators_punctuation import PunctuationName
from ...syntaxis_exception import SyntaxisException



@dataclass
class TopLevelStatementListNode(Node):
    top_level_statement_list: List[TopLevelStatement]

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_top_level_statement_list: List[TopLevelStatement] = []
        new_token_table_index, new_top_level_statement = TopLevelStatement.get_node(token_table_index)

        if new_top_level_statement == None:
            return token_table_index, None

        token_table_index = new_token_table_index

        while token_table[token_table_index].token_type != TokenType.file_end:
            if new_top_level_statement == None:
                raise SyntaxisException(token_table[token_table_index], "Top level statement expected!")

            new_top_level_statement_list.append(new_top_level_statement)

            if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_SEMICOLON:
                raise SyntaxisException(token_table[token_table_index], "Unexpected symbol at the end of top level statement!")

            token_table_index += 1
            token_table_index, new_top_level_statement = TopLevelStatement.get_node(token_table_index)

        token_table_index += 1
        new_node = cls(new_starting_token, new_top_level_statement_list)

        return token_table_index, new_node