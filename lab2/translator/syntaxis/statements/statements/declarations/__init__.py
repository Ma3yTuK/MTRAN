from .declaration import Declaration
from .type_declaration import TypeDeclaration
from .var_declaration import VarDeclaration



Declaration.child_order = [TypeDeclaration, VarDeclaration]