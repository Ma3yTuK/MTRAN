from .if_statement_optional_part import IfStatementOptionalPart
from .block import Block
from .if_statement import IfStatement



IfStatementOptionalPart.child_order = [Block, IfStatement]