from .statement import Statement
from dataclasses import dataclass
from ...expressions.expression import Expression
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.identifiers_and_types import Variable
from ....lexic.keywords import KeywordName
from ...semantics_exception import SemanticsException
from ....vm.commands import Commands, add_command, add_literal
from ..top_level_statements.top_level_declarations.func_declaration import FuncDeclaration



@dataclass
class ReturnStatement(Statement):
    value: Expression | None
    pop_count: int


    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_RETURN:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_value = Expression.get_node(token_table_index)
        new_node = cls(new_starting_token, new_value, Variable.current_stack_pos - FuncDeclaration.func_stack[-1].starting_stack_pos)

        FuncDeclaration.func_stack[-1].has_returns = True

        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):

        if self.value is not None:

            if self.value.eval_type() != FuncDeclaration.func_stack[-1].signature.result.eval_type():
                raise SemanticsException(self.value.starting_token, "Invalid return type!")

        else:

            if FuncDeclaration.func_stack[-1].signature.result.eval_type() is not None:
                raise SemanticsException(self.starting_token, "Function must return value!")

    def gen_code(self):
        add_command(Commands.POP)
        add_literal(pack('!i', pop_count), None)

        if self.value is not None:
            self.value.gen_code()

        add_command(Commands.RET)