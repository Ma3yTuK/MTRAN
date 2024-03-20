from .top_level_statement import TopLevelStatement
from .top_level_declarations.top_level_declaration import TopLevelDeclaration



TopLevelStatement.child_order = [TopLevelDeclaration]