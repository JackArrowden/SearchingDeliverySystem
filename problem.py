from typing import Optional
from state import State
from node import Node
from grid import Grid
import random

class Problem:
    def __init__(self, matrix, start_list, goal_list, limit_time = None, fuel_capacity = None):
        self.grid = Grid(matrix)

        self.start = start_list
        self.goal = [[goal] for goal in goal_list]

        self.limit_time = limit_time
        self.fuel_capacity = fuel_capacity

        self.delta = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.trip_points = start_list + goal_list

    def generate_distination(self, trip_id):
        while True:
            x = random.randint(0, self.grid.num_row - 1)  
            y = random.randint(0, self.grid.num_col - 1)  
            
            point = (x, y)
            if self.grid.is_blank_cell(x, y) and point not in self.trip_points:
                self.trip_points.append(point)
                self.goal[trip_id].append(point)
                return point

    def in_time(self, x: int, y: int, cur_time, trip_id: int = 0) -> bool:
        if cur_time is not None and cur_time < abs(x - self.goal[trip_id][-1][0]) + abs(y - self.goal[trip_id][-1][1]):
            return False
        return True
    
    def is_valid_state(self, state: State, trip_id: int = 0):
        return state.fuel >= 0 and self.in_time(state.x, state.y, state.time, trip_id)

    def heuristic(self, current: State, trip_id: int = 0):
        return abs(current.x - self.goal[trip_id][-1][0]) + abs(current.y - self.goal[trip_id][-1][1]) 
    
    def is_goal(self, current: State, trip_id: int = 0) -> bool:
        if  current.x == self.goal[trip_id][-1][0] and current.y == self.goal[trip_id][-1][1]:
            return True
        return False
    
    def get_num_trips(self):
        return len(self.start)
    
    def init(self, trip_id: int = 0) -> State:
        return State(self.start[trip_id][0], self.start[trip_id][1], self.fuel_capacity, self.limit_time)

    def ACTIONS(self, current: State) -> list:
        actions = []

        # check conditions to add the action of refill fuel
        if self.fuel_capacity is not None and current.fuel == 0:
                return actions
        
        # check condition to add the action of move to new cell 
        for delta_x, delta_y in self.delta:
            new_x = current.x + delta_x
            new_y = current.y + delta_y
            if not self.grid.is_move_cell(new_x, new_y):
                continue
            
            if self.limit_time is not None:
                new_time = current.time - self.grid.time_2_in(new_x, new_y)
                if not self.in_time(new_x, new_y, new_time):
                    continue
            
            actions.append((delta_x, delta_y))

        return actions

    def RESULT(self, current: State, action: tuple[2]) -> State:
        new_x = current.x + action[0]
        new_y = current.y + action[1]

        new_fuel = None
        if self.grid.is_gas_station(new_x, new_y):
            new_fuel = self.fuel_capacity
        elif current.fuel is not None:
            new_fuel = current.fuel - 1
        
        new_time = None
        if current.time is not None:
            new_time = current.time - self.grid.time_2_in(new_x, new_y)

        return State(new_x, new_y, new_fuel, new_time)

    def ACTION_COST(self, prev_state: State, action, cur_state: State):
        return 1

    def time_cost(self, prev_state: State, action, cur_state: State):
        return self.grid.time_2_in(cur_state.x, cur_state.y)

    def EXPAND(self, node: Node):
        cur_state = node.state

        for action in self.ACTIONS(cur_state):
            next_state = self.RESULT(cur_state, action)

            cost = node.path_cost + self.ACTION_COST(cur_state, action, next_state)
            yield Node(next_state, node, cost)


def trace_path(node: Node):
    if node is None:
        return [-1]
    path = []
    while node is not None:
        path.append((node.state.x, node.state.y))
        node = node.parent
    path.reverse()
    return path