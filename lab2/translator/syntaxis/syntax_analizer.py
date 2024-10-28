from .program_node import PragramNode
from .syntaxis_exception import SyntaxisException
from ..lexic.tokens import token_table



def syntax_analizer():
    token_table_index, root_node = PragramNode.get_node(0)

    if root_node == None:
        raise SyntaxisException(token_table[token_table_index], "Invalid syntax")

    return root_node