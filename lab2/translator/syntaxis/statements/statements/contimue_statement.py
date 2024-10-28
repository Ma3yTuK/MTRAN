from .statement import Statement
from dataclasses import dataclass
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.keywords import KeywordName
from ....lexic.identifiers_and_types import Variable
from ....vm.commands import Commands, add_command, add_literal
from .for_statement import ForStatement
from ...syntaxis_exception import SyntaxisException
from struct import pack



@dataclass
class ContinueStatement(Statement):
    for_statement: ForStatement
    stack_pos: int

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_CONTINUE:
            return token_table_index, None
        
        if not ForStatement.for_stack:
            raise SyntaxisException(token_table[token_table_index], "Continue must be inside for")

        token_table_index += 1
        new_node = cls(new_starting_token, ForStatement.for_stack[-1], Variable.current_stack_pos)

        return token_table_index, new_node

    def gen_code(self):
        add_command(Commands.POP)
        add_literal(pack('!i', self.stack_pos - self.for_statement.after_init_stack_pos), None)
        add_command(Commands.JMP)
        add_literal(pack('!i', self.for_statement.continue_pos), None)

    def __str__(self):
        return self.__class__.__name__ + '\n'