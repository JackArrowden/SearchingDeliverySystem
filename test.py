from problem import Problem
from UCS_level_2_3 import UCS_level_2_3
from A_star import a_star_search
from FileHandler import readInput


(matrix, start, goal) = readInput('./test_level_1/input1_level1.txt')
problem = Problem(matrix, start, goal)
path = UCS_level_2_3(problem)

print(path)
