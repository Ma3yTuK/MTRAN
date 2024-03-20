from ..statement_list import StatementListNode
from .if_statement_optional_part import IfStatementOptionalPart
from dataclasses import dataclass
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.operators_punctuation import PunctuationName
from ....syntaxis_exception import SyntaxisException



@dataclass
class Block(IfStatementOptionalPart):
    statements: StatementListNode

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACES_O:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_statements = StatementListNode.get_node(token_table_index)

        if new_statements == None:
            raise SyntaxisException(token_table[token_table_index], "Block cannot be blank")

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACES_C:
            raise SyntaxisException(token_table[token_table_index], "Closing brace expected")

        token_table_index += 1
        new_node = cls(new_statements)

        return token_table_index, new_node