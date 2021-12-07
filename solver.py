from parse import read_input_file, write_output_file
import random
import numpy as np
import matplotlib.pyplot as plt
import os

class Solution():
    def __init__(self, tasks, path=[], visited=None, time=0, profit=0, hash=''):
        self.tasks = tasks
        self.path = path
        self.n = len(tasks)
        if visited == None:
            self.visited = [False]*self.n
        else:
            self.visited = visited
        self.time = time
        self.profit = profit
        self.hash = hash

    def __str__(self):
        return str(self.profit) + " " + str(self.path)

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    tabu = {}
    queue = []
    initial, initial_hash = get_initial_solution(tasks, tabu)
    tabu[initial_hash] = 1
    max_profit = fitness(initial, tasks)[0]
    tabu_initial = {initial_hash: 1}
    max_path = initial
    global_profit = 0
    global_path = []
    last_i = 0
    for i in range(6000):
        # Get neighbors from initiail and initialize local variables
        neighbors = get_neighbors(initial)
        local_profit = 0
        local_path = []
        local_hash = 0

        # Update local variables with best neighbor
        for neighbor in neighbors:
            neighbor_profit = fitness(neighbor, tasks)[0]
            neighbor_hash = hash('-'.join([str(i) for i in neighbor]))
            if neighbor_profit > local_profit and neighbor_hash not in tabu:
                local_profit = neighbor_profit
                local_path = neighbor
                local_hash = neighbor_hash
        
        # update global maximas if higher neighbor is found. Also redefine initial
        if local_profit > max_profit:
            last_i = i
            max_profit = local_profit
            max_path = local_path
            initial = max_path
        tabu[local_hash] = 1
        tabu_initial[local_hash] = 1
        queue.append(local_hash)
        if len(queue) > 200:
            tabu.pop(queue.pop(0))
        if i - last_i > 200:
            initial, initial_hash = get_initial_solution(tasks, tabu)
            while initial_hash in tabu_initial:
                print(initial_hash)
                initial, initial_hash = get_initial_solution(tasks, tabu)
            if max_profit > global_profit:
                print(max_profit)
                global_profit = max_profit
                global_path = max_path
            max_profit = 0
            tabu[initial_hash] = 1
            last_i = i
    # print(fitness(max_path, tasks))
    global_path = fitness(global_path, tasks)[1]
    # print(fitness(max_path, tasks))
    print(check_solution(global_path, tasks))
    print(global_profit)
    return global_path

def fitness(path, tasks):
    time = 0
    profit = 0
    ret = []
    for i in path:
        task = tasks[i-1]
        time += task.get_duration()
        if time > 1440:
            return profit, ret
        profit += task.get_profit(time)
        ret.append(i)
    return profit, ret



def get_initial_solution(tasks, tabu):
    """Returns a solution object with a randomized feasible solution"""
    copy = tasks[:]
    time = 0
    path = []
    while len(copy):
        weights = [(c.get_profit(time+c.get_duration())*(60.0/c.get_duration())*(1440/c.get_deadline()))**8 for c in copy]
        if weights == [0]*len(copy):
            weights = [1]*len(copy)
        next_task = random.choices(copy, weights)[0]
        copy.remove(next_task)
        time += next_task.get_duration()
        path.append(next_task.get_task_id())
    return path, hash('-'.join([str(i) for i in path]))
    
# def get_initial_solution(tasks):
#     """Returns a solution object with a randomized feasible solution"""
#     shuffle = list(range(1, len(tasks)+1))
#     random.shuffle(shuffle)
#     return shuffle, hash('-'.join([str(i) for i in shuffle]))

# def get_best_neighboring(solution, tabu, tasks, max_profit):
#     """Return the best neighboring solution of solution that is not tabu"""
#     n = len(tasks)
#     prefix = []
#     prefix_profit = 0
#     prefix_time = 0
#     prefix_visited = [False]*n
#     prefix_strings = []
#     local_max = 0
#     local_neighbor = None
#     for i in np.linspace(0, len(solution.path), num=len(solution.path), dtype=int, endpoint=False):
#         shuffle = tasks[:]
#         id = solution.path[i]
#         task = tasks[id-1]
#         prefix.append(id)
#         prefix_time += task.get_duration()
#         prefix_profit += task.get_profit(prefix_time)
#         prefix_visited[id-1] = True
#         prefix_strings.append(str(id))
#         neighbor_path, neighbor_time, neighbor_profit, neighbor_visited, neighbor_strings = prefix[:], prefix_time, prefix_profit, prefix_visited[:], prefix_strings[:]
#         neighbor = Solution(tasks, neighbor_path, neighbor_visited, neighbor_time, neighbor_profit)
#         task = random.choices(tasks, get_weights(neighbor, tasks))[0]
#         while neighbor.time + task.get_duration() <= 1440 and len(shuffle):
#             if not neighbor_visited[task.get_task_id()-1]:
#                 neighbor.time += task.get_duration()
#                 neighbor.profit += task.get_profit(neighbor.time)
#                 neighbor.path.append(task.get_task_id())
#                 neighbor.visited[task.get_task_id()-1] = True
#                 neighbor_strings.append(str(task.get_task_id()))
#             task = random.choices(tasks, get_weights(neighbor, tasks))[0]
#         neighbor.hash = hash('-'.join(neighbor_strings))
#         if neighbor.profit > local_max and (neighbor.hash not in tabu or neighbor.profit > max_profit):
#             local_max = neighbor.profit
#             local_neighbor = neighbor
#     return local_neighbor

def get_neighbors(solution):
    neighbors = []
    swap_tabu = {}
    for i in range(50):
        new_solution = solution[:]
        u, v = random.sample(range(0, len(new_solution)), 2)
        while ((u, v) in swap_tabu):
            u, v = random.sample(range(0, len(new_solution)), 2)
        swap_tabu[(u, v)] = 1
        swap_tabu[(v, u)] = 1
        new_u, new_v = new_solution[v], new_solution[u]
        new_solution[u] = new_u
        new_solution[v] = new_v
        neighbors.append(new_solution)
    return neighbors


def check_solution(path, tasks):
    time = 0
    profit = 0
    for i in path:
        task = tasks[i-1]
        time += task.get_duration()
        profit += task.get_profit(time)
        if time > 1440:
            return "Too many tasks", profit
    return profit

def get_weights(solution, tasks):
    weights = []
    sum_weights = 0
    for next_task in tasks:
        profit = next_task.get_profit(solution.time + next_task.get_duration())*(60/next_task.get_duration())
        heuristic = (profit*(1/next_task.get_duration())*(1/next_task.get_deadline()))**2
        weights.append(heuristic)
        sum_weights += heuristic
    return weights

# Here's an example of how to run your solver.
if __name__ == '__main__':
    # tasks = read_input_file('inputs/large/large-16.in')
    # output = solve(tasks)
    # output_path = 'outputs/large/large-291.out'
    # write_output_file(output_path, output)
    for input_path in os.listdir('inputs'):
       for file_name in os.listdir('inputs/' + input_path):
            output_path = 'outputs/' + input_path + "/" + file_name[:len(file_name)-3] + '.out'
            tasks = read_input_file('inputs/' + input_path + "/" + file_name)
            print('inputs/' + input_path + "/" + file_name)
            output = solve(tasks)
            write_output_file(output_path, output)