# Depth First Search
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from node import Node
from problem import Problem, trace_path

def DFS(problem: Problem):
    node = Node(problem.init())
    frontier = [(node, 0)]
    reached = {node.state: node}
    depth = -1

    while frontier:
        node, priotity = frontier.pop()

        for child in problem.EXPAND(node):
            if problem.is_goal(child.state):
                return trace_path(child)
                                  
            if child.state not in reached:
                reached[child.state] = child
                frontier.append((child, depth))

        depth -= 1

    return -1

# This is a test, should not be printed unless this file is run directly
matrix =   [[0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, -1, 0, -1],
            [0, 0, -1, -1, -1, 0, 0, -1, 0, -1],
            [0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
            [0, 0, -1, -1, -1, 0, 0, -1, -1, 0],
            [1, 0, -1, 0, 0, 0, 0, 0, -1, 0],
            [0, 0, -2, 0, -1, 4, -1, 8, -1, 0],
            [0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
            [0, -1, -1, -1, -1, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 0, -1, -1, -1, 0]]
problem = Problem(matrix, (1, 1), (7, 8), 10, 20)

path = DFS(problem)
print(path)