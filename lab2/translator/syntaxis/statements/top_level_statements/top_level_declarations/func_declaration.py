from ...top_level_statements.top_level_declarations.top_level_declaration import TopLevelDeclaration
from ....expressions.unary_expressions.primary_expressions.operands.identifiers.identifier_node import IdentifierNode
from ....type_nodes.type_literals.function_type import Signature
from dataclasses import dataclass
from ...statements.if_statements.block import Block
from .....lexic.tokens import token_table, Token, TokenType
from .....lexic.keywords import KeywordName
from ....syntaxis_exception import SyntaxisException



@dataclass
class FuncDeclaration(TopLevelDeclaration):
    name: IdentifierNode
    signature: Signature
    body: Block
    identifier_table: Dict[str, Identifier]

    @classmethod
    def get_node(cls, token_table_index):

        if token_table[token_table_index].token_type != TokenType.keyword or token_table[token_table_index].name != KeywordName.K_FUNC:
            return token_table_index, None

        token_table_index += 1
        token_table_index, new_name = IdentifierNode.get_node(token_table_index)

        if new_name == None:
            raise SyntaxisException(token_table[token_table_index], "Identifier expected")

        token_table_index, new_signature = Signature.get_node(token_table_index)

        if new_signature == None:
            raise SyntaxisException(token_table[token_table_index], "Signature expected!")

        token_table_index, new_body = Block.get_node(token_table_index)
        new_node = cls(new_name, new_signature, new_body)

        return token_table_index, new_node