from .statement import Statement
from dataclasses import dataclass
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.keywords import KeywordName
from .for_statement import ForStatement
from ...syntaxis_exception import SyntaxisException



@dataclass
class ContinueStatement(Statement):

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_CONTINUE:
            return token_table_index, None
        
        if ForStatement.forcount == 0:
            raise SyntaxisException(token_table[token_table_index], "Continue must be inside for")

        token_table_index += 1
        new_node = cls()

        return token_table_index, new_node