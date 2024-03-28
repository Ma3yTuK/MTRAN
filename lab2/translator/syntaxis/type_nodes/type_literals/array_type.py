from .type_literal import TypeLiteral
from dataclasses import dataclass
from ...expressions.unary_expressions.primary_expressions.operands.literals.basic_literal import BasicLiteral
from ....lexic.tokens import token_table, TokenType, Token
from ..type_node import TypeNode
from ....lexic.operators_punctuation import PunctuationName
from ....lexic.identifiers_and_types import ArrayTypeL, IntegerNumbericType
from ....lexic.literals import literals
from ...syntaxis_exception import SyntaxisException



@dataclass
class ArrayType(TypeLiteral):
    count: BasicLiteral
    element_type: TypeNode

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACKETS_O:
            return token_table_index, None

        token_table_index += 1
        new_token_table_index, new_count = BasicLiteral.get_node(token_table_index)

        if new_count == None:
            raise SyntaxisException(token_table[token_table_index], "Literal expected!")

        token_table_index = new_token_table_index

        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name != PunctuationName.P_BRACKETS_C:
            raise SyntaxisException(token_table[token_table_index], "Closing bracket expected!")

        token_table_index += 1
        new_token_table_index, new_element_type = TypeNode.get_node(token_table_index)

        if new_element_type == None:
            raise SyntaxisException(token_table[token_table_index], "Undefined type!")

        new_node = cls(new_count, new_element_type)
        return new_token_table_index, new_node
    
    def eval_type(self):

        if not hasattr(self, "__type"):
            count = literals[self.count.literal_name].value_type.to_python(literals[self.count.literal_name].value)
            self.__type = ArrayTypeL(count, self.element_type.eval_type())
        
        return self.__type