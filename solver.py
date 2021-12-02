from parse import read_input_file, write_output_file
import random
import os

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
        self.path = []
        self.done = False
        self.n = n

    def clear(self):
        """
        Resets ant fields. This is so we dont have to reinitialize ants
        on every iteration
        """

    def can_do_task(self, task):
        return self.time + task.get_duration() <= 1440 and not self.visited[task.get_task_id()-1]
        

    def get_weights(self):
        """
        Given current state of ant, return list of weights for choosing
        next job. Can only move to jobs not done or still have time left
        to do.
        """
        weights = []
        for task in self.tasks:
            if self.can_do_task(task):
                # Can change the weights to be scaled by values to prefer any feature
                weights.append(task.get_profit(self.time + task.get_duration()))
            else:
                weights.append(0)
        if weights == [0]*self.n:
            self.done = True
        return weights


def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    n = len(tasks)
    ants = [Ant(n, tasks), Ant(n, tasks), Ant(n, tasks)]
    while not move_ants(ants, tasks):
        pass
    return []

def move_ants(ants, tasks):
    for ant in ants:
        all_done = True
        if not ant.done:
            all_done = False
            weights = ant.get_weights()
            if sum(weights) == 0:
                return True
            next_task = random.choices(tasks, weights)[0]
            id = next_task.get_task_id()
            ant.time += next_task.get_duration()
            ant.profit += next_task.get_profit(ant.time)
            ant.path.append(id)
            ant.visited[id-1] = True
    return all_done


#change

# Here's an example of how to run your solver.
if __name__ == '__main__':
    tasks = read_input_file('inputs/large/large-100.in')
    output = solve(tasks)
    # for input_path in os.listdir('inputs'):
    #    for file_name in os.listdir('inputs/' + input_path):
    #         output_path = 'outputs/' + input_path + "/" + file_name[:len(file_name)-3] + '.out'
    #         tasks = read_input_file('inputs/' + input_path + "/" + file_name)
    #         print('inputs/' + input_path + "/" + file_name)
    #         output = solve(tasks)
    #         write_output_file(output_path, output)