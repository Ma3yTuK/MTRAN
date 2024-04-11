from .unary_expression import UnaryExpression
from ...node import Node
from dataclasses import dataclass
from ....lexic.operators_punctuation import PunctuationName, OperatorName, unary_operators, boolean_unary_operators, any_unary_operators, numeric_unary_operators
from ....lexic.tokens import token_table, Token, TokenType
from ....lexic.identifiers_and_types import NumericType, BoolType, PointerTypeL, Type, IntegerNumbericType
from ....vm.commands import Commands, add_command, add_literal, add_reference
from .unary_expression import UnaryExpression
from ...syntaxis_exception import SyntaxisException
from ...semantics_exception import SemanticsException
from struct import pack



@dataclass
class UnaryOperator(Node):
    operator: str # unary

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        
        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name not in unary_operators:
            return token_table_index, None

        new_node = cls(new_starting_token, token_table[token_table_index].name)
        token_table_index += 1

        return token_table_index, new_node

    def __str__(self):
        return self.__class__.__name__ + '(' + self.operator + ')\n'


@dataclass
class UnaryOperation(UnaryExpression):
    operator: UnaryOperator
    argument: UnaryExpression

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        new_token_table_index, new_operator = UnaryOperator.get_node(token_table_index)

        if new_operator == None:
            return token_table_index, None

        token_table_index = new_token_table_index
        token_table_index, new_argument = UnaryExpression.get_node(token_table_index)

        if new_argument == None:
            raise SyntaxisException(token_table[token_table_index], "Exprected expression!")

        if new_operator.operator == OperatorName.O_DEREF and not new_argument.addressable:
            raise SyntaxisException(token_table[token_table_index], "Expression must be addressable here!")

        if new_operator.operator == OperatorName.O_MUL_OR_REF:
            new_addressable = True
        else:
            new_addressable = False

        new_node = cls(new_starting_token, new_addressable, new_operator, new_argument)
        new_node.check_semantics()

        return token_table_index, new_node

    def check_semantics(self):

        if self.operator.operator in numeric_unary_operators and not isinstance(self.argument.eval_type(), NumericType):
            raise SemanticsException(self.argument.starting_token, "Numeric type expected")
        
        if self.operator.operator in boolean_unary_operators and not isinstance(self.argument.eval_type(), BoolType):
            raise SemanticsException(self.argument.starting_token, "Boolean type expected")

        if self.operator.operator == OperatorName.O_MUL_OR_REF and not isinstance(self.argument.eval_type(), PointerTypeL):
            raise SemanticsException(self, "Pointer type expected")

        if self.operator.operator == OperatorName.O_DEREF and not isinstance(self.argument.eval_type(), Type):
            raise SemanticsException(self, "Invalid type")

    def eval_type(self):

        if not hasattr(self, "_type"):

            if self.operator.operator in numeric_unary_operators and isinstance(self.argument.eval_type(), NumericType):
                self._type = self.argument.eval_type()

            if self.operator.operator in boolean_unary_operators and isinstance(self.argument.eval_type(), BoolType):
                self._type = self.argument.eval_type()

            if self.operator.operator == OperatorName.O_MUL_OR_REF and isinstance(self.argument.eval_type(), PointerTypeL):
                self._type = self.argument.eval_type().pointer_type

            if self.operator.operator == OperatorName.O_DEREF and isinstance(self.argument.eval_type(), Type):
                self._type = PointerTypeL(self.argument.eval_type())
            
            if not hasattr(self, "_type"):
                self._type = None

        return self._type

    def gen_code(self):
        self.argument.gen_code()

        match self.operator.operator:
            case OperatorName.O_MINUS:
                if isinstance(self.argument.eval_type(), IntegerNumbericType):
                    add_command(Commands.NEG)
                else:
                    add_command(Commands.NEGF)
            case OperatorName.O_LNOT:
                add_command(Commands.NOT)
            case OperatorName.O_MUL_OR_REF:
                add_command(Commands.REF)
                add_literal(pack('!i', self.argument.eval_type().pointer_type.size), None)
            case OperatorName.O_DEREF:
                add_command(Commands.DEREF)