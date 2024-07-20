from best_fisrt_search import *

def a_star_search(problem, W):
    return best_first_search(problem, lambda node: node.path_cost + W * problem.heuristic(node.state))

# fileName = "test_level_1/input1_level1.txt"
# map, start, goal = readInput(fileName)

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

result = a_star_search(problem, 1.5)

path = trace_path (result)

print(path)