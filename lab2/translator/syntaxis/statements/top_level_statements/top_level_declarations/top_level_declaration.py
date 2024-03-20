from ..top_level_statement import TopLevelStatement
from ...base_declaration import BaseDeclaration
from dataclasses import dataclass



@dataclass
class TopLevelDeclaration(TopLevelStatement, BaseDeclaration):
    pass