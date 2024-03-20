from ...statements.statement import Statement
from ...base_declaration import BaseDeclaration
from dataclasses import dataclass



@dataclass
class Declaration(Statement, BaseDeclaration):
    pass