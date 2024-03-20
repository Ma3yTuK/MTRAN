from .statement import Statement
from .break_statement import BreakStatement
from .contimue_statement import ContinueStatement
from .for_statement import ForStatement
from .return_statement import ReturnStatement
from .switch_statement import SwitchStatement
from .simple_statements.simple_statement import SimpleStatement
from .if_statements.if_statement_optional_part import IfStatementOptionalPart
from .declarations.declaration import Declaration



Statement.child_order = [BreakStatement, ContinueStatement, ForStatement, ReturnStatement, SwitchStatement, IfStatementOptionalPart, Declaration, SimpleStatement]