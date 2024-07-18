# Greedy Best First Search
from node import Node
from problem import Problem, trace_path

def GBFS(problem: Problem):
    node = Node(problem.init())
    frontier = [node]
    reached = {node.state: node}

    while frontier:
        frontier.sort(key=lambda x: problem.heuristic(x.state))
        node = frontier.pop(0)

        if problem.is_goal(node.state):
            return trace_path(node)

        for child in problem.EXPAND(node):
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
problem = Problem(matrix, (1, 1), (7, 8), 10, 20)

path = GBFS(problem)
print(path)