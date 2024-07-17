from state import State
from typing import Optional

class Node:
    def __init__(self, state: State, parent: Optional['Node'] = None, path_cost: int = 0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

