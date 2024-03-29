from dataclasses import dataclass
from typing import ClassVar
import random
from ..lexic.tokens import Token



@dataclass
class Node:
    starting_token: Token
    
    child_order: ClassVar = []
    
    @classmethod
    def get_node(cls, token_table_index):
        
        for child in cls.child_order:
            new_token_table_index, new_node = child.get_node(token_table_index)

            if new_node != None:
                return new_token_table_index, new_node

        return token_table_index, None

    def check_semantics(self):
        pass

    def __str__(self):
        result = self.__class__.__name__ + '\n'

        r = random.randrange(0, 255, 1)
        tabulation = f"\033[38;5;{r}m\t"

        for name, attr in self.__dict__.items():
            if isinstance(attr, Node):
                result += tabulation + tabulation.join(str(attr).splitlines(True))
            elif isinstance(attr, list):
                for element in attr:
                    if isinstance(element, Node):
                        result += tabulation + tabulation.join(str(element).splitlines(True))

        return result