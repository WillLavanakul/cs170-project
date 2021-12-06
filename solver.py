from parse import read_input_file, write_output_file
import random
import numpy as np
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
    initial = get_initial_solution(tasks)
    tabu[initial.hash] = 1
    queue.append(initial.hash)
    max_profit = initial.profit
    max_path = []
    for i in range(300):
        neighbor = get_best_neighboring(initial, tabu, tasks, max_profit)
        if len(queue) > 30:
            removed_hash = queue.pop(0)
            tabu.pop(removed_hash)
        tabu[neighbor.hash] = 1
        queue.append(neighbor.hash)
        if neighbor.profit > max_profit:
            initial = neighbor
            max_profit = neighbor.profit
            max_path = neighbor.path
            print(check_solution(max_path, tasks), i)
    return max_path



def get_initial_solution(tasks):
    """Returns a solution object with a randomized feasible solution"""
    shuffle = tasks[:]
    solution = Solution(tasks)
    initial_strings = []
    task = random.choices(tasks, get_weights(solution, tasks))[0]
    while solution.time + task.get_duration() <= 1440 and len(tasks):
        solution.time += task.get_duration()
        solution.profit += task.get_profit(solution.time)
        solution.path.append(task.get_task_id())
        solution.visited[task.get_task_id()-1] = True
        initial_strings.append(str(task.get_task_id()))
        task = random.choices(tasks, get_weights(solution, tasks))[0]
    solution.hash = hash('-'.join(initial_strings))
    return solution

def get_best_neighboring(solution, tabu, tasks, max_profit):
    """Return the best neighboring solution of solution that is not tabu"""
    n = len(tasks)
    prefix = []
    prefix_profit = 0
    prefix_time = 0
    prefix_visited = [False]*n
    prefix_strings = []
    local_max = 0
    local_neighbor = None
    for i in np.linspace(0, len(solution.path), num=len(solution.path), dtype=int, endpoint=False):
        shuffle = tasks[:]
        id = solution.path[i]
        task = tasks[id-1]
        prefix.append(id)
        prefix_time += task.get_duration()
        prefix_profit += task.get_profit(prefix_time)
        prefix_visited[id-1] = True
        prefix_strings.append(str(id))
        neighbor_path, neighbor_time, neighbor_profit, neighbor_visited, neighbor_strings = prefix[:], prefix_time, prefix_profit, prefix_visited[:], prefix_strings[:]
        neighbor = Solution(tasks, neighbor_path, neighbor_visited, neighbor_time, neighbor_profit)
        task = random.choices(tasks, get_weights(neighbor, tasks))[0]
        while neighbor.time + task.get_duration() <= 1440 and len(shuffle):
            if not neighbor_visited[task.get_task_id()-1]:
                neighbor.time += task.get_duration()
                neighbor.profit += task.get_profit(neighbor.time)
                neighbor.path.append(task.get_task_id())
                neighbor.visited[task.get_task_id()-1] = True
                neighbor_strings.append(str(task.get_task_id()))
            task = random.choices(tasks, get_weights(neighbor, tasks))[0]
        neighbor.hash = hash('-'.join(neighbor_strings))
        if neighbor.profit > local_max and (neighbor.hash not in tabu or neighbor.profit > max_profit):
            local_max = neighbor.profit
            local_neighbor = neighbor
    return local_neighbor

def get_best_neighboring_swap(solution, tabu, tasks, max_profit):
    for i in range(20):
        new_solution = solution.path[:]
        u, v = random.sample(range(0, len(new_solution)), 2)
        new_u, new_v = new_solution[v], new_solution[u]
        new_solution[u] = new_u
        new_solution[v] = new_v
        new_profit = check_solution(new_solution, tasks)
        if new_profit > max_profit:
            print(new_profit)

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
        if solution.visited[next_task.get_task_id()-1]:
            weights.append(0)
        else:
            profit = next_task.get_profit(solution.time + next_task.get_duration())*(60/next_task.get_duration())
            heuristic = (profit*(1/next_task.get_duration())*(1/next_task.get_deadline()))**2
            weights.append(heuristic)
            sum_weights += heuristic
    return weights

# Here's an example of how to run your solver.
if __name__ == '__main__':
    tasks = read_input_file('inputs/large/large-16.in')
    output = solve(tasks)
    # output_path = 'outputs/large/large-16.out'
    # write_output_file(output_path, output)
    # for input_path in os.listdir('inputs'):
    #    for file_name in os.listdir('inputs/' + input_path):
    #         output_path = 'outputs/' + input_path + "/" + file_name[:len(file_name)-3] + '.out'
    #         tasks = read_input_file('inputs/' + input_path + "/" + file_name)
    #         print('inputs/' + input_path + "/" + file_name)
    #         output = solve(tasks)
    #         write_output_file(output_path, output)