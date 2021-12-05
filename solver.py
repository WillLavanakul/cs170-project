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
    alpha = 100.0
    beta = 100.0
    gamma = 3.0
    phi = 1
    lam = 1
    phero = [[1 for i in range(n+1)] for j in range(n+1)]
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
            """
            Given current state of ant, return list of weights for choosing
            next job. Can only move to jobs not done or still have time left
            to do.
            """
            heuristics = []
            sum_hueristics = 0
            max_heuristic = 0
            current_task_id = 0
            if self.task != None:
                current_task_id = self.task.get_task_id()
            for task in self.tasks:
                if self.can_do_task(task):
                    # Calculate numerator of probability with heuristic and pheromone
                    profit = gamma * float(task.get_profit(self.time + task.get_duration()))
                    duration = alpha/float(task.get_duration())
                    deadline = beta/float(task.get_deadline())
                    heuristic = profit*(phero[current_task_id][task.get_task_id()]**lam)
                    #print(task.get_task_id(), heuristic)
                    heuristics.append(heuristic)
                    max_heuristic = max(max_heuristic, heuristic)
                    sum_hueristics += heuristic
                else:
                    heuristics.append(0)
            # Scale each probability with total hueristics and pheromone
            #print(max_heuristic)
            # if sum_hueristics == 0:
            #     return heuristics
            # for i in range(len(heuristics)):
            #     heuristics[i] = (heuristics[i] / sum_hueristics)
            return heuristics

    def move_ants(ants, tasks):
        done_weights = [0]*n
        done_ants = []
        p = phero
        for i in range(len(ants)):
            ant = ants[i]
            weights = ant.get_weights()
            if weights != done_weights:
                next_task = random.choices(tasks, weights)[0]
                id = next_task.get_task_id()
                ant.task = next_task
                ant.time += next_task.get_duration()
                ant.profit += next_task.get_profit(ant.time)
                ant.path.append(id)
                ant.visited[id-1] = True
            else:
                ants[i] = Ant(n, tasks)
                done_ants.append(ant)
        return done_ants
                    

    def update_phero(ants):
        local_profit = 0
        local_path = []
        if len(ants) > 0:
            for i in range(n+1):
                for j in range(n+1):
                    phero[i][j] = 0.8*phero[i][j]
        for ant in ants:
            path = ant.path
            profit = ant.profit
            if profit > local_profit:
                local_profit = profit
                local_path = path
            print(path)
            print(profit)
            iter_profit_history.append(profit)
            for i in range(len(path)-1):
                u = path[i]
                v = path[i+1]
                phero[u][v] += (profit/(max_profit+1))
            ant.clear()
        return local_profit, local_path
    
    ants = [Ant(n, tasks) for j in range(25)]
    for i in range(1000):
        done_ants = move_ants(ants, tasks)
        local_profit, local_path = update_phero(done_ants)
        if local_profit > max_profit:
                max_profit = local_profit
                max_path = local_path
    plt.plot(iter_profit_history)
    plt.show()
    a = Ant(n, tasks)
    w = a.get_weights()
    print(max_profit)
    print(max_path)
    return max_path

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
