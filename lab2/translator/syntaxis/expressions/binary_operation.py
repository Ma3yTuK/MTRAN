from .expression import Expression
from ..node import Node
from dataclasses import dataclass
from ...lexic.operators_punctuation import PunctuationName, OperatorName, binary_operators, binary_operator_precedence, boolean_binary_operators, any_binray_operators_bool, numeric_binary_operators_bool, numeric_binary_operators_number
from ...lexic.tokens import token_table, Token, TokenType
from ...vm.commands import Commands, add_command
from ...lexic.identifiers_and_types import BoolType, NumericType, TypeName, identifier_tables, IntegerNumbericType, FloatingNumericType, Type
from .unary_expressions.unary_expression import UnaryExpression
from ..syntaxis_exception import SyntaxisException
from ..semantics_exception import SemanticsException



@dataclass
class BinaryOperator(Node):
    operator: str # binary

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        
        if token_table[token_table_index].token_type != TokenType.operator or token_table[token_table_index].name not in binary_operators:
            return token_table_index, None

        new_node = cls(new_starting_token, token_table[token_table_index].name)
        token_table_index += 1

        return token_table_index, new_node

    def __str__(self):
        return self.__class__.__name__ + '(' + self.operator + ')\n'


@dataclass
class BinaryOperation(Expression):
    operator: BinaryOperator
    argument1: Expression
    argument2: Expression

    @classmethod
    def get_node(cls, token_table_index):
        new_starting_token = token_table[token_table_index]
        arguments_stack: List[Expression] = []
        operators_stack: List[BinaryOperator] = []

        new_token_table_index, new_unary_expression = UnaryExpression.get_node(token_table_index)

        if new_unary_expression == None:
            return token_table_index, None

        arguments_stack.append(new_unary_expression)
        new_token_table_index, new_operator = BinaryOperator.get_node(new_token_table_index)

        if new_operator == None:
            return token_table_index, None

        new_addressable = False
        token_table_index = new_token_table_index

        if token_table[token_table_index].token_type == TokenType.operator and token_table[token_table_index].name == OperatorName.O_ASS:
            return token_table_index, None

        while new_operator != None:
            
            while operators_stack and binary_operator_precedence[new_operator.operator] <= binary_operator_precedence[operators_stack[-1].operator]:
                new_argument2 = arguments_stack.pop()
                new_argument1 = arguments_stack.pop()
                new_expression = cls(new_starting_token, new_addressable, operators_stack.pop(), new_argument1, new_argument2)
                new_expression.check_semantics()
                arguments_stack.append(new_expression)

            operators_stack.append(new_operator)
            token_table_index, new_unary_expression = UnaryExpression.get_node(token_table_index)

            if new_unary_expression == None:
                raise SyntaxisException(token_table[token_table_index], "Expression expected!")

            arguments_stack.append(new_unary_expression)
            token_table_index, new_operator = BinaryOperator.get_node(token_table_index)

        while operators_stack:
            new_argument2 = arguments_stack.pop()
            new_argument1 = arguments_stack.pop()
            new_expression = cls(new_starting_token, new_addressable, operators_stack.pop(), new_argument1, new_argument2)
            new_expression.check_semantics()
            arguments_stack.append(new_expression)

        new_node = arguments_stack[0]

        return token_table_index, new_node

    def check_semantics(self):

        if self.argument1.eval_type() != self.argument2.eval_type():
            raise SemanticsException(self.operator.starting_token, "Invalid operands!")
        if self.operator.operator in numeric_binary_operators_bool | numeric_binary_operators_number and not (isinstance(self.argument1.eval_type(), NumericType) and isinstance(self.argument2.eval_type(), NumericType)):
            raise SemanticsException(self.operator.starting_token, "Numeric operands expected!")
        if self.operator.operator in boolean_binary_operators and not (isinstance(self.argument1.eval_type(), BoolType) and isinstance(self.argument2.eval_type(), BoolType)):
            raise SemanticsException(self.operator.starting_token, "Boolean operands expected!")
        if self.operator.operator in any_binray_operators_bool and not (isinstance(self.argument1.eval_type(), Type) and isinstance(self.argument2.eval_type(), Type)):
            raise SemanticsException(self.operator.starting_token, "Invalid operands!")

    def eval_type(self):

        if not hasattr(self, "_type"):

            if self.operator.operator in numeric_binary_operators_number:
                
                if isinstance(self.argument1.eval_type(), NumericType) and isinstance(self.argument2.eval_type(), NumericType):

                    if self.argument1.eval_type() == self.argument2.eval_type():
                        self._type = self.argument1.eval_type()
            
            if self.operator.operator in numeric_binary_operators_bool:
                
                if isinstance(self.argument1.eval_type(), NumericType) and isinstance(self.argument2.eval_type(), NumericType):

                    if self.argument1.eval_type() == self.argument2.eval_type():
                        self._type = identifier_tables[0][TypeName.T_BOOL]

            if self.operator.operator in boolean_binary_operators:

                if isinstance(self.argument1.eval_type(), BoolType) and isinstance(self.argument2.eval_type(), BoolType):
                    
                    if self.argument1.eval_type() == self.argument2.eval_type():
                        self._type = identifier_tables[0][TypeName.T_BOOL]

            if self.operator.operator in any_binray_operators_bool:

                if isinstance(self.argument1.eval_type(), Type) and isinstance(self.argument2.eval_type(), Type):
                    
                    if self.argument1.eval_type() == self.argument2.eval_type():
                        self._type = identifier_tables[0][TypeName.T_BOOL]

            if not hasattr(self, "_type"):
                self._type = None
        
        return self._type

    def gen_code(self):
        self.argument1.gen_code()
        self.argument2.gen_code()

        match self.operator.operator:
            case OperatorName.O_MINUS:
                if isinstance(self.argument1.eval_type(), IntegerNumbericType):
                    add_command(Commands.SUB)
                else:
                    add_command(Commands.SUBF)
            case OperatorName.O_PLUS:
                if isinstance(self.argument1.eval_type(), IntegerNumbericType):
                    add_command(Commands.SUM)
                else:
                    add_command(Commands.SUMF)
            case OperatorName.O_MUL_OR_REF:
                if isinstance(self.argument1.eval_type(), IntegerNumbericType):
                    add_command(Commands.MUL)
                else:
                    add_command(Commands.MULF)
            case OperatorName.O_DIV:
                if isinstance(self.argument1.eval_type(), IntegerNumbericType):
                    add_command(Commands.DIV)
                else:
                    add_command(Commands.DIVF)
            case OperatorName.O_MOD:
                if isinstance(self.argument1.eval_type(), IntegerNumbericType):
                    add_command(Commands.PERC)
                else:
                    add_command(Commands.PERCF)
            case OperatorName.O_GE:
                if isinstance(self.argument1.eval_type(), IntegerNumbericType):
                    add_command(Commands.GE)
                else:
                    add_command(Commands.GEF)
            case OperatorName.O_GT:
                if isinstance(self.argument1.eval_type(), IntegerNumbericType):
                    add_command(Commands.GT)
                else:
                    add_command(Commands.GTF)
            case OperatorName.O_LE:
                if isinstance(self.argument1.eval_type(), IntegerNumbericType):
                    add_command(Commands.LE)
                else:
                    add_command(Commands.LEF)
            case OperatorName.O_LT:
                if isinstance(self.argument1.eval_type(), IntegerNumbericType):
                    add_command(Commands.LT)
                else:
                    add_command(Commands.LTF)
            case OperatorName.O_EQ:
                add_command(Commands.EQ)
            case OperatorName.O_NQ:
                add_command(Commands.NQ)
            case OperatorName.O_LAND:
                add_command(Commands.AND)
            case OperatorName.O_LOR:
                add_command(Commands.OR)