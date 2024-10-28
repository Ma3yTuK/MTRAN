from .statement import Statement
from dataclasses import dataclass
from .simple_statements.simple_statement import SimpleStatement
from ...expressions.expression import Expression
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.operators_punctuation import PunctuationName
from ...syntaxis_exception import SyntaxisException
from ...semantics_exception import SemanticsException
from ....lexic.keywords import KeywordName
from ....lexic.identifiers_and_types import Identifier, identifier_tables, Variable, BoolType
from ....vm.commands import code, Commands, add_command, add_literal, add_reference
from .if_statements.block import Block
from typing import ClassVar, Dict, List
from struct import pack



@dataclass
class ForStatement(Statement):
    initial_statement: SimpleStatement
    condition: Expression
    post_statement: SimpleStatement
    for_body: Block
    identifier_table: Dict[str, Identifier]

    for_stack: ClassVar = []
    
    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        
        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_FOR:
            return token_table_index, None

        new_identifier_table = {}
        identifier_tables.append(new_identifier_table)

        new_node = cls(new_starting_token, None, None, None, None, new_identifier_table)
        cls.for_stack.append(new_node)
        new_node.starting_stack_pos = Variable.current_stack_pos

        token_table_index += 1
        token_table_index, new_initial_statement = SimpleStatement.get_node(token_table_index)

        new_node.after_init_stack_pos = Variable.current_stack_pos

        if new_initial_statement == None:
            raise SyntaxisException(token_table[token_table_index], "Simple statement expected")
        
        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_SEMICOLON:
            raise SyntaxisException(token_table[token_table_index], "Semicolon expected")
        
        token_table_index += 1
        token_table_index, new_condition = Expression.get_node(token_table_index)

        if new_condition == None:
            raise SyntaxisException(token_table[token_table_index], "Condition expected")
        
        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_SEMICOLON:
            raise SyntaxisException(token_table[token_table_index], "Semicolon expected")

        token_table_index += 1
        token_table_index, new_post_statement = SimpleStatement.get_node(token_table_index)

        if new_post_statement == None:
            raise SyntaxisException(token_table[token_table_index], "Simple statement expected")

        token_table_index, new_for_body = Block.get_node(token_table_index)

        if new_for_body == None:
            raise SyntaxisException(token_table[token_table_index], "For body expected")

        new_node.initial_statement = new_initial_statement
        new_node.condition = new_condition
        new_node.post_statement = new_post_statement
        new_node.for_body = new_for_body

        cls.for_stack.pop()
        identifier_tables.pop()
        new_node.end_stack_pos = Variable.current_stack_pos
        Variable.current_stack_pos = new_node.starting_stack_pos

        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):

        if not isinstance(self.condition.eval_type(), BoolType):
            raise SemanticsException(self.condition.starting_token, "Condition must be boolean!")

    def gen_code(self):
        self.initial_statement.gen_code()
        start_pos = len(code)
        self.condition.gen_code()

        add_command(Commands.JMPIF)
        jump_pos = len(code)
        add_literal(pack('!i', 0), None)

        add_command(Commands.POP)
        add_literal(pack('!i', self.after_init_stack_pos - self.starting_stack_pos), None)

        self.break_pos = len(code)

        add_command(Commands.JMP)
        exit_pos = len(code)
        add_literal(pack('!i', 0), None)

        new_iteration_pos = len(code)

        add_command(Commands.POP)
        add_literal(pack('!i', self.end_stack_pos - self.after_init_stack_pos), None)

        self.continue_pos = len(code)

        self.post_statement.gen_code()

        add_command(Commands.JMP)
        add_literal(pack('!i', start_pos), None)

        jump_pos_destination = pack('!i', len(code))
        for index, byte in enumerate(jump_pos_destination):
            code[jump_pos + index] = byte

        self.for_body.gen_code()

        add_command(Commands.JMP)
        add_literal(pack('!i', new_iteration_pos), None)

        exit_pos_destination = pack('!i', len(code))
        for index, byte in enumerate(exit_pos_destination):
            code[exit_pos + index] = byte