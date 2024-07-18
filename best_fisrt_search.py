import heapq
from problem import *

def best_first_search(problem, f):
    initial_node = Node(problem.initial)
    frontier = []
    heapq.heappush(frontier, (f(initial_node), initial_node))
    reached = {problem.initial: initial_node}

    while frontier:
        _, node = heapq.heappop(frontier)
        if problem.is_goal(node.state):
            return node

        for child in EXPAND(node):
            s = child.state
            if s not in reached or f(child) < f(reached[s]):
                reached[s] = child
                heapq.heappush(frontier, (f(child), child))
    return None
