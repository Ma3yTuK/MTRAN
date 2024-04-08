from .primary_expression import PrimaryExpression
from dataclasses import dataclass
from ....type_nodes.type_node import TypeNode
from ...expression import Expression
from .....lexic.operators_punctuation import PunctuationName
from ....syntaxis_exception import SyntaxisException
from ....semantics_exception import SemanticsException
from .....lexic.identifiers_and_types import IntegerNumbericType, FloatingNumericType



@dataclass
class Conversion(PrimaryExpression):
    type_node: TypeNode
    expression: Expression

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_type_node = TypeNode.get_node(token_table_index)

        if new_type_node == None:
            return token_table_index, None

        if token_table[new_token_table_index].token_type != TokenType.operator or token_table[new_token_table_index].name != PunctuationName.P_PARENTHESES_O:
            raise SyntaxisException(new_starting_token, "Opening parenthesis expected!")

        new_token_table_index += 1
        new_token_table_index, new_expression = Expression.get_node(new_token_table_index)

        if new_expression == None:
            raise SyntaxisException(token_table[new_token_table_index], "Expression expected!")

        if token_table[new_token_table_index].token_type != TokenType.operator or token_table[new_token_table_index].name != PunctuationName.P_PARENTHESES_C:
            raise SyntaxisException(token_table[new_token_table_index], "Closing parenthesis expected!")

        new_token_table_index += 1
        new_addressable = False
        new_node = cls(token_table[new_token_table_index], new_addressable, new_type_node, new_expression)

        return new_token_table_index, new_node

    def check_semantics(self):

        if not self.type_node.eval_type() == self.expression.eval_type():
             
            if not ((self.type_node.eval_type() == IntegerNumbericType and self.expression.eval_type() == FloatingNumericType) or (self.type_node.eval_type() == FloatingNumericType and self.expression.eval_type() == IntegerNumbericType)):
                raise SemanticsException("Invalid cast!")

    def eval_type(self):

        if not hasattr(self, "_type"):

            if not self.type_node.eval_type() == self.expression.eval_type():
                if not ((self.type_node.eval_type() == IntegerNumbericType and self.expression.eval_type() == FloatingNumericType) or (self.type_node.eval_type() == FloatingNumericType and self.expression.eval_type() == IntegerNumbericType)):
                    self._type = None
            
            if not hasattr(self, "_type"):
                self._type = self.type_node.eval_type()

        return self._type