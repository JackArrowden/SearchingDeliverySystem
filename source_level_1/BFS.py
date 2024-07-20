# Breadth First Search
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from node import Node
from problem import Problem, trace_path

def BFS(problem: Problem):
    node = Node(problem.init())
    frontier = [node]
    reached = {node.state: node}

    while frontier:
        node = frontier.pop(0)

        for child in problem.EXPAND(node):
            if problem.is_goal(child.state):
                return trace_path(child)

            if child.state not in reached:
                reached[child.state] = child
                frontier.append(child)

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
problem = Problem(matrix, [(1, 1)], [(7, 8)])

path = BFS(problem)
print(path)