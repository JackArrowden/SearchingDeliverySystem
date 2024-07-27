from problem import Problem, trace_path
from node import Node
from queue import PriorityQueue

class HC_State:
    def __init__(self, list_states, parent = None, cur_agent = 0):
        self.parent = parent
        self.cur_agent = cur_agent
        self.states = list_states

        self.wait_time = [0] * len(list_states)

    def get_wait_time(self):
        return self.wait_time[self.cur_agent] 

    def down_wait_time(self):
        if self.wait_time[self.cur_agent] > 0: 
            self.wait_time[self.cur_agent] -= 1

    def change_agent(self):
        self.cur_agent = (self.cur_agent + 1) % len(self.states)

    def is_goal(self, problem: Problem):
        return self.cur_agent == 0 and problem.is_goal(self.states[self.cur_agent])
    
    def is_stuck(self, problem: Problem):
        return not problem.is_valid_state(self.states[0], 0) or self.states[0].fuel == 0

def next_state(cur_state: HC_State, problem: Problem, action):
    next_state = HC_State(cur_state.states.copy(), cur_state, cur_state.cur_agent)
    id = cur_state.cur_agent
    if next_state.get_wait_time() > 0:
        next_state.down_wait_time()
    else:
        next_state.states[id] = problem.RESULT(cur_state.states[id], action)
        next_state.wait_time[id] = problem.time_cost(cur_state.states[id], action, next_state.states[id]) - 1

    if id != 0 and problem.is_goal(next_state.states[id], id):
        problem.generate_distination(id)

    next_state.change_agent()
    return next_state


def A_star(cur_state: HC_State, problem: Problem):
    trip_id = cur_state.cur_agent
    node = Node(cur_state.states[trip_id])
    frontier = PriorityQueue()
    frontier.put((node.path_cost + problem.heuristic(node.state, trip_id),  node))
    reached = {node.state: node}
    while not frontier.empty():
        _, node = frontier.get()

        if problem.is_goal(node.state, trip_id):
            return trace_path(node)
        
        if reached[node.state].path_cost < node.path_cost:
            continue

        for child in problem.EXPAND(node, trip_id):
            is_agent_cell = False
            for id, agent in enumerate(cur_state.states):
                if id != trip_id and agent.x == child.state.x and agent.y == child.state.y:
                    is_agent_cell = True
                    break 
            if is_agent_cell:
                continue

            if child.state not in reached or reached[child.state].path_cost > child.path_cost:
                reached[child.state] = child
                frontier.put((child.path_cost + problem.heuristic(child.state, trip_id), child))
    return -1

def BEST(cur_state: HC_State, problem: Problem):
    if cur_state.get_wait_time() > 0:
        return next_state(cur_state, problem, (0, 0))

    path = A_star(cur_state, problem)

    if isinstance(path, int):
        return next_state(cur_state, problem, (0, 0))
    
    action = (path[1][0] - path[0][0], path[1][1] - path[0][1])
    return next_state(cur_state, problem, action)



def trace_path_level_4(last_state: HC_State, problem: Problem):
    num_agents = len(last_state.states)
    path = [[] for _ in range(num_agents)]
    cur_state = last_state
    while cur_state is not None:
        change_agent = (cur_state.cur_agent - 1 + num_agents) % num_agents
        path[change_agent].append((cur_state.states[change_agent].x, cur_state.states[change_agent].y))
        cur_state = cur_state.parent
    for index in range(num_agents - 1):
        path[index].append(problem.start[index])
    for index in range(len(path)):
        path[index].reverse()
    return path

def hill_climbing_level_4(problem: Problem):
    init_states = []
    for i in range(problem.get_num_trips()):
        init_states.append(problem.init(i))
    cur = HC_State(init_states)

    while True:
        cur = BEST(cur, problem)

        if cur.is_goal(problem):
            return (True, problem.goal, trace_path_level_4(cur, problem))
        
        if cur.is_stuck(problem):
            return (False, problem.goal, trace_path_level_4(cur, problem))



if __name__ == '__main__':
    matrix =   [[0, 0, 0, 0, -1, -1, 0,  0, 0, 0],
[0, 0, 0, 0,  0,  0, 0, -1, 0, -1],
[0, 0, -1, -1, -1, 0, 0, -1, 0, -1],
[0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
[0, 0, -1, -1, -1, 0, 0, -1, -1, 0],
[1, 0, -1, 0, 0, 0, 0, 0, -1, 0],
[0, 0, -2, 0, -1, 4, -1, 8, -1, 0],
[0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
[0, -1, -1, -1, -1, 0, 0, 0, 0, 0],
[0, 0, 5, 0, 0, 0, -1, -1, -1, 0]]
    start = [(1, 1), (2, 5), (8, 5)]
    goal = [(7, 8), (9, 0), (4, 6)]
    problem = Problem(matrix, start, goal, 50, 10)
    is_reached_goal, goals, path = hill_climbing_level_4(problem)
    print("result: ")
    for row in goals:
        print(row)
    print('\n')
    for row in path:
        print(row)