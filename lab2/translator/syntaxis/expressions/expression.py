from ..node import Node
from dataclasses import dataclass



@dataclass
class Expression(Node):
    addressable: bool

    def eval_type(self):
        pass

    def __str__(self):
        return f"({self.eval_type().__class__.__name__}){super().__str__()}"

    def gen_code(self):
        pass