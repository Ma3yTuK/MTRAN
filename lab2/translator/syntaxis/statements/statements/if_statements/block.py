from ..statement_list import StatementListNode
from .if_statement_optional_part import IfStatementOptionalPart
from dataclasses import dataclass
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.operators_punctuation import PunctuationName
from .....lexic.identifiers_and_types import Identifier, Variable, identifier_tables
from ....syntaxis_exception import SyntaxisException
from typing import Dict



@dataclass
class Block(IfStatementOptionalPart):
    statements: StatementListNode
    identifier_table: Dict[str, Identifier]

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACES_O:
            return token_table_index, None

        stored_stack_pos = Variable.current_stack_pos
        new_identifier_table = {}
        identifier_tables.append(new_identifier_table)

        token_table_index += 1
        token_table_index, new_statements = StatementListNode.get_node(token_table_index)

        if new_statements == None:
            raise SyntaxisException(token_table[token_table_index], "Block cannot be blank")

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACES_C:
            raise SyntaxisException(token_table[token_table_index], "Closing brace expected")

        token_table_index += 1
        new_node = cls(new_starting_token, new_statements, new_identifier_table)

        identifier_tables.pop()
        Variable.current_stack_pos = stored_stack_pos
        
        return token_table_index, new_node