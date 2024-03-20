from .base_declaration import BaseDeclaration
from .base_statement import BaseStatement
from .base_var_declaration import BaseVarDeclaration
from .statements.declarations.declaration import Declaration
from .top_level_statements.top_level_statement import TopLevelStatement
from .statements.statement import Statement
from .top_level_statements.top_level_declarations.top_level_declaration import TopLevelDeclaration
from .statements.declarations.var_declaration import VarDeclaration
from .statements.simple_statements.simple_var_declaration import SimpleVarDeclaration



BaseDeclaration.child_order = [BaseVarDeclaration, Declaration, TopLevelDeclaration]
BaseStatement.child_order = [BaseDeclaration, TopLevelStatement, Statement]
BaseVarDeclaration.child_order = [VarDeclaration, SimpleVarDeclaration]