from .primary_expression import PrimaryExpression
from .operands.operand import Operand
from dataclasses import dataclass
from ....node import Node
from ...expression import Expression
from ....suffixes.suffix import Suffix
from ....suffixes.arguments_suffix import ArgumentsSuffix
from ....suffixes.index_suffix import IndexSuffix
from ....suffixes.selector_suffix import SelectorSuffix
from .....lexic.identifiers_and_types import identifier_tables, FunctionTypeL, ArrayTypeL, UserType
from .....lexic.tokens import Token, token_table, TokenType
from ....semantics_exception import SemanticsException



@dataclass
class PrimaryExpressionWithSuffix(PrimaryExpression):
    primary_expression: PrimaryExpression
    expression_suffix: Suffix

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_primary_expression = Operand.get_node(token_table_index)

        if new_primary_expression == None:
            return token_table_index, None

        new_token_table_index, new_expression_suffix = Suffix.get_node(new_token_table_index)

        if new_expression_suffix == None:
            return token_table_index, None

        token_table_index = new_token_table_index

        while new_expression_suffix != None:
            
            if isinstance(new_expression_suffix, ArgumentsSuffix):
                new_addressable = False
            else:
                new_addressable = new_primary_expression.addressable

            new_primary_expression = cls(new_starting_token, new_addressable, new_primary_expression, new_expression_suffix)
            new_primary_expression.check_semantics()
            token_table_index, new_expression_suffix = Suffix.get_node(token_table_index)

        new_node = new_primary_expression

        return token_table_index, new_node

    def check_semantics(self):

        if isinstance(self.expression_suffix, ArgumentsSuffix):
            
            if not isinstance(self.primary_expression.eval_type(), FunctionTypeL):
                raise SemanticsException(self.starting_token, "Function type expected!")

            if self.expression_suffix.arguments_expressions == None and self.primary_expression.eval_type().operands or len(self.expression_suffix.arguments_expressions.expression_list) != len(self.primary_expression.eval_type().operands):
                raise SemanticsException(self.expression_suffix.starting_token, "Wrong number of arguments!")

            for i, operand_type in enumerate(self.primary_expression.eval_type().operands):
                
                if self.expression_suffix.arguments_expressions.expression_list[i].eval_type() != operand_type:
                    raise SemanticsException(self.expression_suffix.arguments_expressions.expression_list[i].starting_token, "Invalid argument type!")
        
        if isinstance(self.expression_suffix, IndexSuffix):

            if not isinstance(self.primary_expression.eval_type(), ArrayTypeL):
                raise SemanticsException(self.starting_token, "Array type expected!")

        if isinstance(self.expression_suffix, SelectorSuffix):
            
            if not isinstance(self.primary_expression.eval_type(), UserType):
                raise SemanticsException(self.starting_token, "Struct expected!")

            if not self.expression_suffix.operand_identifier.identifier_name in self.primary_expression.eval_type().fields:
                raise SemanticsException(self.expression_suffix.operand_identifier.starting_token, "There is no such field in struct!")

    def eval_type(self):

        if not hasattr(self, "_type"):

            if isinstance(self.expression_suffix, ArgumentsSuffix) and isinstance(self.primary_expression.eval_type(), FunctionTypeL):
                self._type =  self.primary_expression.eval_type().return_type
            
            if isinstance(self.expression_suffix, IndexSuffix) and isinstance(self.primary_expression.eval_type(), ArrayTypeL):
                self._type = self.primary_expression.eval_type().value_type

            if isinstance(self.expression_suffix, SelectorSuffix) and isinstance(self.primary_expression.eval_type(), UserType) and self.expression_suffix.operand_identifier.identifier_name in self.primary_expression.eval_type().fields:
                self._type = self.primary_expression.eval_type().fields[self.expression_suffix.operand_identifier.identifier_name].field_type

            if not hasattr(self, "_type"):
                self._type = None

        return self._type