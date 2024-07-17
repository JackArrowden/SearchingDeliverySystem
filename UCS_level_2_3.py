from problem import Problem, trace_path
from node import Node
from queue import PriorityQueue


def UCS_level_2_3(problem: Problem):
    node = Node(problem.init())
    frontier = PriorityQueue()
    frontier.put((node.path_cost, node))
    reached = {node.state: node}
    while not frontier.empty():
        _, node = frontier.get()


        if problem.is_goal(node.state):
            return trace_path(node)

        if reached[node.state] != node:
            continue
        for child in problem.EXPAND(node):
            if child not in reached or reached[child.state].path_cost > child.path_cost:
                reached[child.state] = child
                frontier.put((child.path_cost, child))

    return None