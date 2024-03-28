from ..node import Node
from dataclasses import dataclass



@dataclass
class TypeNode(Node):
    
    def eval_type(self):
        pass