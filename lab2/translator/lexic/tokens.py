from enum import StrEnum
from dataclasses import dataclass
from typing import List


class TokenType(StrEnum):
    identifier = "identifier"
    literal = "literal"
    keyword = "keyword"
    operator = "operator"
    file_end = "eof"


@dataclass
class Token:
    name: str
    token_type: TokenType
    row: int
    col: int


token_table: List[Token] = []