from problem import Problem, trace_path
from node import Node
from queue import Queue


def BFS_level_2_3(problem: Problem):
    node = Node(problem.init())
    if problem.is_goal(node.state):
        return trace_path(node)
    frontier = Queue()
    frontier.put(node)
    reached = {node.state}

    while not frontier.empty():
        node = frontier.get()

        for child in problem.EXPAND(node):
            if problem.is_goal(child.state):
                return trace_path(child)
            if child.state not in reached:
                reached.add(child.state)
                frontier.put(child)

    return -1