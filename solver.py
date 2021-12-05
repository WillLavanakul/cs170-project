from parse import read_input_file, write_output_file
import random
import matplotlib.pyplot as plt
import math
import os

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """

    n = len(tasks)
    alpha = 1440.0
    beta = 60.0
    gamma = 3.0
    phi = 2 # GREEDY PARAMATER
    lam = 3
    phero = [[1.0 for i in range(n+1)] for j in range(n+1)]
    max_profit = 0
    max_path = []
    iter_profit_history = []

    class Ant:
        """
        Ant to traverse jobs. Keeps track of it's path and current profit.
        """
        def __init__(self, n, tasks, task=None):
            self.tasks = tasks
            self.task = task
            self.time = 0
            self.profit = 0
            self.visited = [False]*n
            self.path = [0]
        
        def clear(self):
            self.task = None
            self.time = 0
            self.profit = 0
            self.visited = [False]*n
            self.path = [0]

        def can_do_task(self, task):
            return self.time + task.get_duration() <= 1440 and not self.visited[task.get_task_id()-1]

        def get_weights(self):
            weights = []
            max_weight = 0
            if self.task == None:
                current_id = 0
            else:
                current_id = self.task.get_task_id()
            for task in self.tasks:
                if self.can_do_task(task):
                    profit = gamma * task.get_profit(self.time + task.get_duration())
                    duration = beta / task.get_duration()
                    deadline = alpha/ task.get_deadline()
                    heuristic = profit*duration*deadline
                    weights.append(heuristic)
                    max_weight = max(heuristic, max_weight)
                else:
                    weights.append(0)
            if max_weight > 0:
                for i in range(len(weights)):
                    weights[i] = ((weights[i] / max_weight)**phi) * (phero[current_id][i+1]**lam)
            return weights
            
    def update_phero(ants, t):
        for i in range(n+1):
            for j in range(n+1):
                phero[i][j] *= 0.9
        new_phero = phero[:]
        best_ant = max(ants, key=lambda a:a.profit)
        worst_ant = min(ants, key=lambda a:a.profit)
        delta = best_ant.profit - worst_ant.profit
        iter_path = best_ant.path
        for ant in ants:
            path = ant.path
            profit = ant.profit
            for i in range(len(path)-1):
                u = path[i]
                v = path[i+1]
                if delta:
                    new_phero[u][v] = new_phero[u][v] + ((profit-worst_ant.profit)/delta)**20
                else:
                    new_phero[u][v] = new_phero[u][v] + 1
        iter_profit_history.append(best_ant.profit)
        return new_phero, best_ant

    def move_ants(ants, tasks):
        p = phero
        done = [False]*len(ants)
        done_weights = [0]*n
        while False in done:
            for ants_index in range(len(ants)):
                ant = ants[ants_index]
                weights = ant.get_weights()
                if weights == done_weights:
                    done[ants_index] = True
                else:
                    next_task = random.choices(tasks, weights)[0]
                    ant.task = next_task
                    ant.path.append(next_task.get_task_id())
                    ant.time += next_task.get_duration()
                    ant.profit += next_task.get_profit(ant.time)
                    ant.visited[next_task.get_task_id()-1] = True

    
    max_ant = Ant(n, tasks)
    for i in range(5):
        ants = [Ant(n, tasks) for j in range(10)]
        move_ants(ants, tasks)
        phero, best_ant = update_phero(ants, i)
        if best_ant.profit > max_ant.profit:
            max_ant = best_ant
    return max_path[1:]

if __name__ == '__main__':
    tasks = read_input_file('inputs/large/large-16.in')
    output = solve(tasks)
    # for input_path in os.listdir('inputs'):
    #    for file_name in os.listdir('inputs/' + input_path):
    #         output_path = 'outputs/' + input_path + "/" + file_name[:len(file_name)-3] + '.out'
    #         tasks = read_input_file('inputs/' + input_path + "/" + file_name)
    #         print('inputs/' + input_path + "/" + file_name)
    #         output = solve(tasks)
    #         write_output_file(output_path, output)

# part-1/test.in
# inputs/large/large-16.in
# inputs/large/large-247.in
# inputs/small/small-193.in
# samples/100.in
# inputs/medium/medium-192.in
