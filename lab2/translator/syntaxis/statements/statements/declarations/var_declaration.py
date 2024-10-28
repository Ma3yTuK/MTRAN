from ...statements.declarations.declaration import Declaration
from ...top_level_statements.top_level_declarations.top_level_declaration import TopLevelDeclaration
from ....node import Node
from dataclasses import dataclass
from ....identifiers.identifier_list import IdentifierListNode
from ....expressions.expression_list import ExpressionListNode
from ....type_nodes.type_node import TypeNode
from typing import List
from .....lexic.tokens import token_table, Token, TokenType
from ....syntaxis_exception import SyntaxisException
from .....lexic.keywords import KeywordName
from .....lexic.operators_punctuation import PunctuationName, OperatorName
from .....lexic.identifiers_and_types import identifier_tables, Variable
from .....vm.commands import Commands, add_literal, add_command, switch_global, unswitch_global, code, global_code
from ...base_var_declaration import BaseVarDeclaration
from ....semantics_exception import SemanticsException



@dataclass
class VarSpec(Node):
    spec_identifiers: IdentifierListNode
    spec_type: TypeNode | None
    spec_expressions: ExpressionListNode | None

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_spec_identifiers = IdentifierListNode.get_node(token_table_index)

        if new_spec_identifiers == None:
            return token_table_index, None
        
        token_table_index = new_token_table_index
        token_table_index, new_spec_type = TypeNode.get_node(token_table_index)

        if token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == OperatorName.O_ASS:
            token_table_index += 1
            token_table_index, new_spec_expressions = ExpressionListNode.get_node(token_table_index)

            if new_spec_expressions == None:
                raise SyntaxisException(token_table[token_table_index], "List of expressions expected!")

            if len(new_spec_expressions.expression_list) != len(new_spec_identifiers.identifier_list):
                raise SyntaxisException(token_table[token_table_index], "Variable declaration lists have different sizes!")
        else:

            if new_spec_type is None:
                raise SyntaxisException(token_table[token_table_index], "Type expected!")

            new_spec_expressions = None

        new_node = cls(new_starting_token, new_spec_identifiers, new_spec_type, new_spec_expressions)
        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):
        current_type = self.spec_type

        for i, new_var in enumerate(self.spec_identifiers.identifier_list):
            
            if new_var.identifier_name in identifier_tables[-1]:
                raise SemanticsException(new_var.starting_token, "Name already exists!")
            else:
                
                if self.spec_type != None:
                    
                    if self.spec_expressions != None and self.spec_expressions.expression_list[i].eval_type() != current_type.eval_type():
                        raise SemanticsException(self.spec_expressions.expression_list[i].starting_token, "Invalid expression type!")
                else:
                    current_type = self.spec_expressions.expression_list[i]

                    if current_type.eval_type() is None:
                        raise SemanticsException(current_type.starting_token, "Cannot initialize with null!")
                    
                identifier_tables[-1][new_var.identifier_name] = Variable(current_type.eval_type(), Variable.current_stack_pos)
                Variable.current_stack_pos += current_type.eval_type().size


@dataclass
class VarDeclaration(Declaration, TopLevelDeclaration, BaseVarDeclaration):
    var_specs: List[VarSpec]
    is_global: bool

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        
        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_VAR:
            return token_table_index, None

        token_table_index += 1
        
        if token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == PunctuationName.P_PARENTHESES_O:
            parenthesis = True
            token_table_index += 1
        else:
            parenthesis = False

        new_token_table_index, new_var_spec = VarSpec.get_node(token_table_index)
        
        if new_var_spec == None:
            raise SyntaxisException(token_table[token_table_index], "Var spec expected!")
        
        token_table_index = new_token_table_index
        new_var_specs: List[TypeSpec] = [new_var_spec]

        if parenthesis:

            if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_SEMICOLON:
                raise SyntaxisException(token_table[token_table_index], "Unexpected symbol at the end of type declaration!")
            
            token_table_index += 1

            while token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_PARENTHESES_C:
                token_table_index, new_var_spec = VarSpec.get_node(token_table_index)
                
                if new_var_spec == None:
                    raise SyntaxisException(token_table[token_table_index], "Var spec expected!")

                new_var_specs.append(new_var_spec)

                if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_SEMICOLON:
                    raise SyntaxisException(token_table[token_table_index], "Unexpected symbol at the end of var declaration!")

                token_table_index += 1

            token_table_index += 1
        
        new_node = cls(new_starting_token, new_var_specs, len(identifier_tables) == 1)

        return token_table_index, new_node

    def gen_code(self):
        
        if self.is_global:
            switch_global()

        for spec in self.var_specs:

            for index, identifier in enumerate(spec.spec_identifiers.identifier_list):

                if spec.spec_expressions is None:
                    add_command(Commands.LD)
                    add_literal(bytes(spec.spec_type.eval_type().size), spec.spec_type.eval_type())
                else:
                    spec.spec_expressions.expression_list[index].gen_code()

                add_command(Commands.PUSH)
        
        if self.is_global:
            unswitch_global()