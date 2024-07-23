# Greedy Best First Search
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from node import Node
from problem import Problem, trace_path

def GBFS(problem: Problem):
    node = Node(problem.init())
    frontier = [node]
    reached = {node.state: node}

    while frontier:
        frontier.sort(key=lambda x: problem.heuristic(x.state))
        node = frontier.pop(0)

        for child in problem.EXPAND(node):
            if problem.is_goal(child.state):
                return trace_path(child)
            
            if child.state not in reached:
                reached[child.state] = child
                frontier.append(child)

    return -1