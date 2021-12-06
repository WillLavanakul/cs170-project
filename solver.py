from parse import read_input_file, write_output_file
import random
import matplotlib.pyplot as plt
import numpy as np
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
    alpha = 2.0
    beta = 2.0
    rho = 0.001
    phero = [[1.0 for i in range(n+1)] for j in range(n+1)]
    min_cost = 0
    min_path = []

    class Ant:
        """
        Ant to traverse jobs. Keeps track of it's path and current profit.
        """
        def __init__(self, n, tasks, task=None):
            self.tasks = tasks
            self.task = task
            self.time = 1
            self.profit = 0
            self.visited = [False]*n
            self.path = [0]
            self.iter = 0
        
        def clear(self):
            self.task = None
            self.time = 0
            self.profit = 0
            self.visited = [False]*n
            self.path = [0]
            self.iter += 1

        def can_do_task(self, task):
            return not self.visited[task.get_task_id()-1]

        def get_weights(self, phero):
            weights = []
            total_weight = 0
            if self.task == None:
                current_id = 0
            else:
                current_id = self.task.get_task_id()
            for i in range(len(self.tasks)):
                task = self.tasks[i]
                if self.can_do_task(task):
                    profit = task.get_profit(self.time+task.get_duration())
                    heuristic = ((profit*(10/task.get_duration()))**alpha)*(phero[current_id][i+1]**beta)
                    weights.append(heuristic)
                    total_weight += heuristic
                else:
                    weights.append(0)
            if total_weight > 0:
                for i in range(len(weights)):
                    weights[i] /= total_weight
            return weights
            
    def update_phero(ants, t):
        deposit = [[0.0 for i in range(n+1)] for j in range(n+1)]
        best_ant = max(ants, key=lambda a:a.profit)
        for ant in ants:
            path = ant.path
            profit = ant.profit
            for i in range(min(len(path)-1, t+1)):
                u = path[i]
                v = path[i+1]
                deposit[u][v] += (ant.profit)
        for i in range(n+1):
            for j in range(n+1):
                phero[i][j] = (1.0)*phero[i][j] + deposit[i][j]**0.2
        a = Ant(n, tasks)
        # plt.plot(a.get_weights(phero))
        # plt.show()
        # a.task = tasks[18]
        # a.visited[18] = True
        # plt.plot(a.get_weights(phero))
        # plt.show()
        # a.task = tasks[34]
        # a.visited[34] = True
        # plt.plot(a.get_weights(phero))
        # plt.show()
        # print("NEW")
        return phero, best_ant

    def move_ants(ants, tasks, phero, i):
        done = [False]*len(ants)
        done_weights = [0]*n
        while False in done:
            for ants_index in range(len(ants)):
                ant = ants[ants_index]
                weights = ant.get_weights(phero)
                if weights == done_weights:
                    done[ants_index] = True
                else:
                    next_task = random.choices(tasks, weights)[0]
                    ant.task = next_task
                    ant.path.append(next_task.get_task_id())
                    ant.time += next_task.get_duration() + 1
                    ant.profit += next_task.get_profit(ant.time)
                    ant.visited[next_task.get_task_id()-1] = True   
        return done



    max_profit = 0
    last_i = 0
    for i in range(100000000):
        ants = [Ant(n, tasks) for j in range(10)]
        move_ants(ants, tasks, phero, i)
        phero, best_ant = update_phero(ants, i)
        if i-last_i > 50:
            print(i)
            phero = [[phero[i][j]**0.2 for i in range(n+1)] for j in range(n+1)]
            # plt.plot(phero[19])
            # plt.show()
            last_i = i
            #print(best_ant.path)
        if best_ant.profit > max_profit:
            last_i = i
            max_profit = best_ant.profit
            print(max_profit, i)
        
    # Show plot
    plt.show()
    print(max_profit)
    return []

def over_time(path, tasks):
    time = 1
    for i in path:
        time += tasks[i-1].duration
    return time > 1440

if __name__ == '__main__':
    tasks = read_input_file('inputs/small/small-193.in')
    output = solve(tasks)
    # for input_path in os.listdir('inputs'):
    #    for file_name in os.listdir('inputs/' + input_path):
    #         output_path = 'outputs/' + input_path + "/" + file_name[:len(file_name)-3] + '.out'
    #         tasks = read_input_file('inputs/' + input_path + "/" + file_name)
    #         print('inputs/' + input_path + "/" + file_name)
    #         output = solve(tasks)
    #         if over_time(output, tasks):
    #             raise ValueError('A very specific bad thing happened.')
    #         write_output_file(output_path, output)

# part-1/test.in
# inputs/large/large-16.in
# inputs/large/large-247.in
# inputs/small/small-193.in
# samples/100.in
# inputs/medium/medium-192.in
