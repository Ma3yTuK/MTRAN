from .if_statement_optional_part import IfStatementOptionalPart
from dataclasses import dataclass
from ....expressions.expression import Expression
from .block import Block
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.keywords import KeywordName
from .....lexic.identifiers_and_types import Identifier, Variable, identifier_tables, BoolType
from .....vm.commands import Commands, code, add_command, add_literal, add_reference
from ....syntaxis_exception import SyntaxisException
from ....semantics_exception import SemanticsException
from typing import Dict
from struct import pack



@dataclass
class IfStatement(IfStatementOptionalPart):
    condition: Expression
    body: Block
    rest: IfStatementOptionalPart | None
    
    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_IF:
            return token_table_index, None

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

        new_node = cls(new_starting_token, new_condition, new_body, new_rest)
        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):

        if not isinstance(self.condition.eval_type(), BoolType):
            raise SemanticsException(self.condition.starting_token, "Condition must be boolean!")

    def gen_code(self):
        self.condition.eval_type()

        add_command(Commands.JMPIF)
        body_pos = len(code)
        add_literal(pack('!i', 0), None)

        if self.rest is not None:
            self.rest.gen_code()
        
        add_command(Commands.JMP)
        exit_pos = len(code)
        add_literal(pack('!i', 0), None)

        body_pos_destination = pack('!i', len(code))
        for index, byte in enumerate(body_pos_destination):
            code[body_pos + index] = byte
        
        self.body.gen_code()

        exit_pos_destination = pack('!i', len(code))
        for index, byte in enumerate(exit_pos_destination):
            code[exit_pos + index] = byte