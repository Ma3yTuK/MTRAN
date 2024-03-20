from ..lexic.tokens import Token



class SyntaxisException(Exception):

    def __init__(self, token: Token, message: str):
        message = f"{token.row}, {token.col}: {message}"
        super().__init__(message)