from .if_statement_optional_part import IfStatementOptionalPart
from dataclasses import dataclass
from ....expressions.expression import Expression
from .block import Block
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.keywords import KeywordName
from .....lexic.identifiers_and_types import Identifier, Variable, identifier_tables, BoolType
from ....syntaxis_exception import SyntaxisException
from ....semantics_exception import SemanticsException
from typing import Dict



@dataclass
class IfStatement(IfStatementOptionalPart):
    condition: Expression
    body: Block
    rest: IfStatementOptionalPart | None
    identifier_table: Dict[str, Identifier]
    
    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_IF:
            return token_table_index, None

        stored_stack_pos = Variable.current_stack_pos
        new_identifier_table = {}
        identifier_tables.append(new_identifier_table)

        token_table_index += 1
        token_table_index, new_condition = Expression.get_node(token_table_index)

        if new_condition == None:
            raise SyntaxisException(token_table[token_table_index], "If condition expected")

        token_table_index, new_body = Block.get_node(token_table_index)

        if new_body == None:
            raise SyntaxisException(token_table[token_table_index], "If body expected")

        if token_table[token_table_index].token_type == TokenType.keyword and token_table[token_table_index].name == KeywordName.K_ELSE:
            token_table_index += 1
            token_table_index, new_rest = IfStatementOptionalPart.get_node(token_table_index)

            if new_rest == None:
                raise SyntaxisException(token_table[token_table_index], "Invalid syntaxis after else")

        else:
            new_rest = None

        new_node = cls(new_starting_token, new_condition, new_body, new_rest,new_identifier_table)

        identifier_tables.pop()
        Variable.current_stack_pos = stored_stack_pos

        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):

        if not isinstance(self.condition.eval_type(), BoolType):
            raise SemanticsException(self.condition.starting_token, "Condition must be boolean!")