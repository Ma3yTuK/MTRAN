from .top_level_declaration import TopLevelDeclaration
from .func_declaration import FuncDeclaration
from .type_declaration import TypeDeclaration
from .var_declaration import VarDeclaration



TopLevelDeclaration.child_order = [FuncDeclaration, TypeDeclaration, VarDeclaration]