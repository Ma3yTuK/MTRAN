from .operand import Operand
from dataclasses import dataclass
from ....expression import Expression
from ......lexic.tokens import token_table, Token, TokenType
from ......lexic.operators_punctuation import PunctuationName
from .....syntaxis_exception import SyntaxisException



@dataclass
class ParanthesisOperand(Operand):
    inner_expression: Expression

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_PARENTHESES_O:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_expression = Expression.get_node(token_table_index)

        if new_expression == None:
            raise SyntaxisException(token_table[token_table_index], "Expression expected!")

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_PARENTHESES_C:
            raise SyntaxisException(token_table[token_table_index], "Closing parenthesis expected!")

        token_table_index += 1
        new_addressable = new_expression.addressable
        new_node = cls(new_addressable, new_expression)

        return token_table_index, new_node

    def eval_type(self):

        if not hasattr(self, "__type"):
            self.__type = self.inner_expression.eval_type()
        
        return self.__type