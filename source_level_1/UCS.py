# Uniform Cost Search
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from node import Node
from problem import Problem, trace_path

def UCS(problem: Problem):
    node = Node(problem.init())
    frontier = [(node, 0)]
    reached = {node.state: node}

    while frontier:
        frontier.sort(key=lambda x: x[1])
        node, priotity = frontier.pop(0)

        if problem.is_goal(node.state):
            return trace_path(node)

        for child in problem.EXPAND(node):
            if child.state not in reached:
                reached[child.state] = child
                frontier.append((child, child.path_cost))

    return -1