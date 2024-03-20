from .suffix import Suffix
from .arguments_suffix import ArgumentsSuffix
from .index_suffix import IndexSuffix
from .selector_suffix import SelectorSuffix



Suffix.child_order = [ArgumentsSuffix, IndexSuffix, SelectorSuffix]