from .statement import Statement
from dataclasses import dataclass
from ...expressions.expression import Expression
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.identifiers_and_types import Variable, IntegerNumbericType, FloatingNumericType, StringType
from ....lexic.keywords import KeywordName
from ...semantics_exception import SemanticsException
from ...syntaxis_exception import SyntaxisException
from ....vm.commands import Commands, add_command, add_literal
from ..top_level_statements.top_level_declarations.func_declaration import FuncDeclaration



@dataclass
class PrintStatement(Statement):
    value: Expression

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_PRINT:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_value = Expression.get_node(token_table_index)

        if new_value == None:
            raise SyntaxisException(token_table[token_table_index], "Expression expected!")

        new_node = cls(new_starting_token, new_value)
        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):

        if not (isinstance(self.value.eval_type(), IntegerNumbericType) or isinstance(self.value.eval_type(), FloatingNumericType) or isinstance(self.value.eval_type(), StringType)):
            raise SemanticsException(self.value.starting_token, "Unsupported expression type!")

    def gen_code(self):
        self.value.gen_code()

        if isinstance(self.value.eval_type(), IntegerNumbericType):
            add_command(Commands.PRINTI)
        
        if isinstance(self.value.eval_type(), FloatingNumericType):
            add_command(Commands.PRINTF)
        
        if isinstance(self.value.eval_type(), StringType):
            add_command(Commands.PRINTS)