from parse import read_input_file, write_output_file
import random
import matplotlib.pyplot as plt
import os

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """

    n = len(tasks)
    alpha = 60.0
    beta = 1440.0
    gamma = 1.0
    phi = 1.0
    lam = 1.0
    phero = [[1 for i in range(n+1)] for j in range(n+1)]

    class Ant:
        """
        Ant to traverse jobs. Keeps track of it's path and current profit.
        """
        def __init__(self, n, tasks, alpha, beta, gamma, task=None):
            self.tasks = tasks
            self.task = task
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
            current_task_id = 0
            if self.task != None:
                current_task_id = self.task.get_task_id()
            for task in self.tasks:
                if self.can_do_task(task):
                    # Calculate numerator of probability with heuristic and pheromone
                    profit = gamma * float(task.get_profit(self.time + task.get_duration()))
<<<<<<< HEAD
                    duration = alpha - float(task.get_duration())
                    deadline = beta - float(task.get_deadline())
                    heuristic = (profit) ** phi * phero[current_task_id][task.get_task_id()] ** lam
=======
                    duration = alpha/float(task.get_duration())
                    deadline = beta/float(task.get_deadline())
                    heuristic = phero[current_task_id][task.get_task_id()]**lam
>>>>>>> f56edc3d3604a8037ae9740fa0335e28d50e08b3
                    heuristics.append(heuristic)
                else:
                    heuristics.append(0)
            # Scale each probability with total hueristics and pheromone
            return heuristics

    def move_ants(ants, tasks):
        done = [False]*len(ants)
        done_weights = [0]*n
        while False in done:
            for i in range(len(ants)):
                if not done[i]:
                    ant = ants[i]
                    weights = ant.get_weights()
                    if weights != done_weights:
                        next_task = random.choices(tasks, weights)[0]
                        id = next_task.get_task_id()
                        ant.time += next_task.get_duration()
                        ant.profit += next_task.get_profit(ant.time)
                        ant.path.append(id)
                        ant.visited[id-1] = True
                    else:
                        done[i] = True

    def update_phero(ants):
        sum_profits = 0
        best_profit = 0
        best_path = []
        for ant in ants:
            sum_profits += ant.profit
            if ant.profit > best_profit:
                best_profit = ant.profit
                best_path = ant.path[1:]
        # for i in range(n+1):
        #     for j in range(n+1):
        #         phero[i][j] = .85*phero[i][j]
        for ant in ants:
            path = ant.path
            profit = ant.profit
            for i in range(len(path)-1):
                u = path[i]
                v = path[i+1]
                phero[u][v] += (profit/sum_profits)
        return best_profit, best_path
    
    max_profit = 0
    max_path = []
    iter_profit_history = []
    for i in range(10):
        ants = [Ant(n, tasks, alpha, beta, gamma) for j in range(10)]
        move_ants(ants, tasks)
        iter_profit, iter_path = update_phero(ants)
        print(iter_path)
        print(iter_profit)
        iter_profit_history.append(iter_profit)
        if iter_profit > max_profit:
            max_profit = iter_profit
            max_path = iter_path
    print(Ant(n, tasks, alpha, beta, gamma).get_weights())
    plt.plot(iter_profit_history)
    plt.show()
    return max_path

if __name__ == '__main__':
    tasks = read_input_file('inputs/small/small-193.in')
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
