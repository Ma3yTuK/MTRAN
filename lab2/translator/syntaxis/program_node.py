from .node import Node
from dataclasses import dataclass
from .statements.top_level_statements.top_level_statement_list import TopLevelStatementListNode



@dataclass
class PragramNode(Node):
    top_level_statements: TopLevelStatementListNode

    @classmethod
    def get_node(cls, token_table_index):
        new_token_table_index, new_top_level_statements = TopLevelStatementListNode.get_node(token_table_index)

        if new_top_level_statements != None:
            new_node = cls(new_top_level_statements)
            return new_token_table_index, new_node

        return token_table_index, None