from .statement import Statement
from dataclasses import dataclass
from .simple_statements.simple_statement import SimpleStatement
from ...expressions.expression import Expression
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.operators_punctuation import PunctuationName
from ...syntaxis_exception import SyntaxisException
from ....lexic.keywords import KeywordName
from .if_statements.block import Block
from typing import ClassVar



@dataclass
class ForStatement(Statement):
    forcount: ClassVar = 0
    initial_statement: SimpleStatement
    condition: Expression
    post_statement: SimpleStatement
    for_body: Block

    @classmethod
    def get_node(cls, token_table_index):
        
        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_FOR:
            return token_table_index, None

        cls.forcount += 1

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

        new_node = cls(new_initial_statement, new_condition, new_post_statement, new_for_body)

        cls.forcount -= 1

        return token_table_index, new_node