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
from .if_statements.block import Block
from typing import ClassVar, Dict, List



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

        stored_stack_pos = Variable.current_stack_pos
        new_identifier_table = {}
        identifier_tables.append(new_identifier_table)

        new_node = cls(new_starting_token, None, None, None, None, new_identifier_table)
        cls.for_stack.append(new_node)

        token_table_index += 1
        token_table_index, new_initial_statement = SimpleStatement.get_node(token_table_index)

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
        Variable.current_stack_pos = stored_stack_pos

        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):

        if not isinstance(self.condition.eval_type(), BoolType):
            raise SemanticsException(self.condition.starting_token, "Condition must be boolean!")