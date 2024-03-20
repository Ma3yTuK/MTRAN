from ..node import Node
from dataclasses import dataclass



@dataclass
class Expression(Node):
    addressable: bool