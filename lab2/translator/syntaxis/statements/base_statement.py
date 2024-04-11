from ..node import Node
from dataclasses import dataclass



@dataclass
class BaseStatement(Node):
    
    def gen_code(self):
        pass