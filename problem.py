from typing import Optional
from state import State
from node import Node
from grid import Grid

class Problem:
    def __init__(self, matrix, start_list, goal_list, limit_time = None, fuel_capacity = None):
        self.grid = Grid(matrix)

        self.start = start_list
        self.goal = goal_list

        self.limit_time = limit_time
        self.fuel_capacity = fuel_capacity

        self.delta = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def in_time(self, x: int, y: int, cur_time, goal_id: int = 0) -> bool:
        if cur_time is not None and cur_time < abs(x - self.goal[goal_id][0]) + abs(y - self.goal[goal_id][1]):
            return False
        return True
    


    def heuristic(self, current: State, goal_id: int = 0):
        return abs(current.x - self.goal[goal_id][0]) + abs(current.y - self.goal[goal_id][1]) 
    
    def is_goal(self, current: State, goal_id: int = 0) -> bool:
        if  current.x == self.goal[goal_id][0] and current.y == self.goal[goal_id][1]:
            return True
        return False
    
    def init(self, start_id: int = 0) -> State:
        return State(self.start[start_id][0], self.start[start_id][1], self.fuel_capacity, self.limit_time)

    def ACTIONS(self, current: State) -> list:
        actions = []

        if self.fuel_capacity is not None:
            if self.grid.is_gas_station(current.x, current.y) and self.in_time(current.x, current.y, current.time - self.grid.refill_time(current.x, current.y)):
                actions.append((0, 0))
            if self.fuel_capacity is not None and current.fuel == 0:
                return actions
        
        for delta_x, delta_y in self.delta:
            new_x = current.x + delta_x
            new_y = current.y + delta_y
            if not self.grid.is_move_cell(new_x, new_y):
                continue
            
            if self.limit_time is not None:
                new_time = current.time - self.grid.time_2_out(current.x, current.y)
                if not self.in_time(new_x, new_y, new_time):
                    continue
            
            actions.append((delta_x, delta_y))

        return actions

    def RESULT(self, current: State, action: tuple[2]) -> State:
        new_x = current.x + action[0]
        new_y = current.y + action[1]

        new_fuel = None
        if action == (0, 0):
            new_fuel = self.fuel_capacity
        elif current.fuel is not None:
            new_fuel = current.fuel - 1
        
        new_time = None
        if action == (0, 0):
            new_time = current.time - self.grid.refill_time(current.x, current.y)
        elif current.time is not None:
            new_time = current.time - self.grid.time_2_out(current.x, current.y)

        return State(new_x, new_y, new_fuel, new_time)

    def ACTION_COST(self, prev_state: State, action, cur_state: State):
        if prev_state.x != cur_state.x or prev_state.y != cur_state.y:
            return 1
        return 0


    def EXPAND(self, node: Node):
        cur_state = node.state

        for action in self.ACTIONS(cur_state):
            next_state = self.RESULT(cur_state, action)

            cost = node.path_cost + self.ACTION_COST(cur_state, action, next_state)
            yield Node(next_state, node, cost)


def trace_path(node: Node | None):
    if node is None:
        return [-1]
    path = []
    while node is not None:
        path.append((node.state.x, node.state.y))
        node = node.parent
    path.reverse()
    return path