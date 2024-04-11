from .node import Node
from dataclasses import dataclass
from .statements.top_level_statements.top_level_statement_list import TopLevelStatementListNode
from ..lexic.tokens import token_table
from ..lexic.identifiers_and_types import identifier_tables, Variable
from ..vm.commands import Commands, add_command, add_reference
from .semantics_exception import SemanticsException



@dataclass
class PragramNode(Node):
    top_level_statements: TopLevelStatementListNode

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_top_level_statements = TopLevelStatementListNode.get_node(token_table_index)

        if new_top_level_statements != None:
            new_node = cls(new_starting_token, new_top_level_statements)
            new_node.check_semantics()
            return new_token_table_index, new_node

        return token_table_index, None

    def check_semantics(self):
        
        if 'main' not in identifier_tables[0]:
            raise SemanticsException(self.starting_token, "Program has no entry point!")
        
        self.ref = identifier_tables[0]['main'].stack_pos - Variable.current_stack_pos

    def gen_code(self):

        for top_level_statement in self.top_level_statements.top_level_statement_list:
            top_level_statement.gen_code()

        add_command(Commands.LD)
        add_reference(self.ref, identifier_tables[0]['main'].value_type)
        add_command(Commands.CALL)