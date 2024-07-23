from source_level_1.best_fisrt_search import *

def a_star_search(problem):
    return trace_path(best_first_search(problem, lambda node: node.path_cost + problem.heuristic(node.state)))