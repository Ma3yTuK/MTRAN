from ..declarations.var_declaration import VarDeclaration
from ..simple_statements.simple_statement import SimpleStatement
from dataclasses import dataclass
from ...base_var_declaration import BaseVarDeclaration
from ....identifiers.identifier_list import IdentifierListNode
from ....expressions.expression_list import ExpressionListNode
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.operators_punctuation import OperatorName, PunctuationName
from .....lexic.identifiers_and_types import identifier_tables, Variable
from ....syntaxis_exception import SyntaxisException
from ....semantics_exception import SemanticsException
from .....vm.commands import Commands, add_command, add_literal, add_reference



@dataclass
class SimpleVarDeclaration(SimpleStatement, BaseVarDeclaration):
    identifiers: IdentifierListNode
    values: ExpressionListNode

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_identifiers = IdentifierListNode.get_node(token_table_index)

        if new_identifiers == None or token_table[new_token_table_index].token_type != TokenType.operator or token_table[new_token_table_index].name != OperatorName.O_INIT:
            return token_table_index, None

        token_table_index = new_token_table_index + 1
        token_table_index, new_values = ExpressionListNode.get_node(token_table_index)

        if new_values == None:
            raise SyntaxisException(token_table[token_table_index], "Expression list expected!")

        if len(new_identifiers.identifier_list) != len(new_values.expression_list):
            raise SyntaxisException(token_table[token_table_index], "Declaration parts have different length!")

        new_node = cls(new_starting_token, new_identifiers, new_values)
        new_node.check_semantics()

        return token_table_index, new_node


    def check_semantics(self):

        for i, new_var in enumerate(self.identifiers.identifier_list):
            
            if new_var.identifier_name in identifier_tables[-1]:
                raise SemanticsException(new_var.starting_token, "Name already exists!")
            else:
                current_type = self.values.expression_list[i]

                if current_type.eval_type() is None:
                    raise SemanticsException(current_type.starting_token, "Cannot initialize with null!")

                identifier_tables[-1][new_var.identifier_name] = Variable(current_type.eval_type(), Variable.current_stack_pos)
                Variable.current_stack_pos += current_type.eval_type().size

    
    def gen_code(self):

        for index, identifier in enumerate(self.identifiers.identifier_list):
            self.values.expression_list[index].gen_code()
            add_command(Commands.PUSH)