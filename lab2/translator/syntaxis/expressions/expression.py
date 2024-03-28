from ..node import Node
from dataclasses import dataclass



@dataclass
class Expression(Node):
    addressable: bool

    def eval_type(self):
        pass