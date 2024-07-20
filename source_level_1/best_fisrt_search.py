import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import heapq
from problem import *
from FileHandler import *

def best_first_search(problem : Problem, f):
    initial_node = Node(problem.init())
    frontier = []
    heapq.heappush(frontier, (f(initial_node), initial_node))
    reached = {problem.init(): initial_node}

    while frontier:
        _, node = heapq.heappop(frontier)
        if problem.is_goal(node.state):
            return node

        for child in problem.EXPAND(node):
            s = child.state
            if s not in reached or f(child) < f(reached[s]):
                reached[s] = child
                heapq.heappush(frontier, (f(child), child))
    return None

