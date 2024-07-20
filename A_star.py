from best_fisrt_search import *

def a_star_search(problem, W):
    return best_first_search(problem, lambda node: node.path_cost + W * problem.heuristic(node.state))

fileName = "test_level_1/input1_level1.txt"
map, start, goal = readInput(fileName)

print(start)

problem = Problem(map, start[0], goal[0])

result = a_star_search(problem, 1.5)

path = trace_path (result)

for cur in path:
    print(cur + ' ')