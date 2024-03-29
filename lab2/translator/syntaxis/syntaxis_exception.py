from ..lexic.tokens import Token



class SyntaxisException(Exception):

    def __init__(self, token: Token, message: str):
        message = f"{token.row + 1}, {token.col + 1}: {message}"
        super().__init__(message)