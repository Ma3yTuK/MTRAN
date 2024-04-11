from ...top_level_statements.top_level_declarations.top_level_declaration import TopLevelDeclaration
from ....identifiers.identifier_node import IdentifierNode
from ....type_nodes.type_literals.function_type import Signature
from dataclasses import dataclass
from ...statements.if_statements.block import Block
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.keywords import KeywordName
from .....lexic.identifiers_and_types import Variable, identifier_tables, FunctionTypeL, Identifier, TypeName
from ....syntaxis_exception import SyntaxisException
from .....vm.commands import code, Commands, add_command, add_literal, add_reference
from ....semantics_exception import SemanticsException
from struct import pack
from typing import Dict



@dataclass
class FuncDeclaration(TopLevelDeclaration):
    name: IdentifierNode
    signature: Signature
    body: Block
    identifier_table: Dict[str, Identifier]
    has_returns: bool

    func_stack: ClassVar = []

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_FUNC:
            return token_table_index, None

        stored_stack_pos = Variable.current_stack_pos
        new_identifier_table = {}
        identifier_tables.append(new_identifier_table)

        token_table_index += 1
        token_table_index, new_name = IdentifierNode.get_node(token_table_index)

        if new_name == None:
            raise SyntaxisException(token_table[token_table_index], "Identifier expected")

        token_table_index, new_signature = Signature.get_node(token_table_index)

        if new_signature == None:
            raise SyntaxisException(token_table[token_table_index], "Signature expected!")

        new_node = cls(new_starting_token, new_name, new_signature, None, new_identifier_table, False)
        cls.func_stack.append(new_node)
        new_node.check_semantics()
        token_table_index, new_body = Block.get_node(token_table_index)

        if new_body == None:
            raise SyntaxisException(token_table[token_table_index], "Function body expected!")

        if not new_node.has_returns and new_node.signature.eval_type() is not None:
            raise SyntaxisException(token_table[token_table_index], "Function does not return value!")

        new_node.body = new_body

        identifier_tables.pop()
        Variable.current_stack_pos = stored_stack_pos

        cls.func_stack.pop()

        return token_table_index, new_node

    def check_semantics(self):

        if self.name.identifier_name in identifier_tables[0]:
            raise SemanticsException(self.name.starting_token, "Name belongs to other identifier!")

        function_type = self.signature.eval_type()
        identifier_tables[0][self.name.identifier_name] = Variable(function_type, Variable.current_stack_pos)
        Variable.current_stack_pos += function_type.size

        self.starting_stack_pos = Variable.current_stack_pos

        for parameter_declaration in self.signature.parameters.parameters:

            if parameter_declaration.fields == None:
                raise SemanticsException(parameter_declaration.starting_token, "Parameter names expected!")
            
            for parameter in parameter_declaration.fields.identifier_list:

                if parameter.identifier_name in self.identifier_table:
                    raise SemanticsException(self.spec_identifier.starting_token, "Name already exists!")
                else:
                    self.identifier_table[parameter.identifier_name] = Variable(parameter_declaration.fields_type.eval_type(), Variable.current_stack_pos)
                    Variable.current_stack_pos += parameter_declaration.fields_type.eval_type().size
        
    def gen_code(self):

        add_command(Commands.LD)
        add_literal(pack('!i', len(code) + self.signature.eval_type().size + 2), self.signature.eval_type())
        add_command(Commands.PUSH)

        table_size = 0

        for variable in self.identifier_table:
            add_command(Commands.PUSH)
            table_size += variable.value_type.size

        self.body.gen_code()

        add_command(Commands.POP)
        add_literal(pack('!i', table_size), None)
        add_command(Commands.RET)