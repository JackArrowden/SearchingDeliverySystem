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

        for action in problem.ACTIONS(node.state):
            child_state = problem.RESULT(node.state, action)
            child_node = Node(child_state, node, node.path_cost + problem.ACTION_COST(node.state, action, child_state))

            child_key = (child_node.path_cost + f(child_node), child_node)
            if child_state not in reached or child_key < (f(reached[child_state]), reached[child_state]):
                reached[child_state] = child_node
                heapq.heappush(frontier, child_key)
    return None