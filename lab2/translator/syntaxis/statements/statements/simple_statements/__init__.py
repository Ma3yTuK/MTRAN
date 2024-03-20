from .simple_statement import SimpleStatement
from .assignment_statement import AssignmentStatement
from .expression_statement import ExpressionStatement
from .simple_var_declaration import SimpleVarDeclaration
from .inc_dec_statement import IncDecStatement



SimpleStatement.child_order = [AssignmentStatement, SimpleVarDeclaration, IncDecStatement, ExpressionStatement] # order is important here