from best_fisrt_search import *

def a_star_search(problem, W):
    return best_first_search(problem, lambda node: node.path_cost + W * problem.heuristics[node.state])

