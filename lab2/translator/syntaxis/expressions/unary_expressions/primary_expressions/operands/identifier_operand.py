from .....identifiers.identifier_node import IdentifierNode
from ......lexic.identifiers_and_types import identifier_tables, Variable
from .....semantics_exception import SemanticsException
from ......lexic.tokens import token_table
from ......vm.commands import Commands, add_reference, add_command
from .operand import Operand
from dataclasses import dataclass



@dataclass
class IdentifierOperand(Operand):
    identifier: IdentifierNode

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_identifier = IdentifierNode.get_node(token_table_index)

        if new_identifier == None:
            return token_table_index, None

        new_addressable = True
        new_node = cls(new_starting_token, new_addressable, new_identifier)

        new_node.check_semantics()

        return new_token_table_index, new_node

    def check_semantics(self):

        for index, table in enumerate(reversed(identifier_tables)):

            if self.identifier.identifier_name in table:

                if isinstance(table[self.identifier.identifier_name], Variable):
                    if index + 1 == len(identifier_tables):
                        self.ref = table[self.identifier.identifier_name].stack_pos
                    else:
                        self.ref = table[self.identifier.identifier_name].stack_pos - Variable.current_stack_pos
                    return
                else:
                    raise SemanticsException(self.starting_token, "Identifier is not expression!")
        
        raise SemanticsException(self.starting_token, "Undefined identifier!")

    def eval_type(self):
        
        if not hasattr(self, "_type"):

            for table in reversed(identifier_tables):

                if self.identifier.identifier_name in table:

                    if isinstance(table[self.identifier.identifier_name], Variable):
                        self._type = table[self.identifier.identifier_name].value_type
                    else:
                        self._type = None
                    
                    break

            if not hasattr(self, "_type"):
                self._type = None
        
        return self._type

    def gen_code(self):
        add_command(Commands.LD)
        add_reference(self.ref, self.eval_type())