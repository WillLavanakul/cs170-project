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
    best_profit = 0
    best_path = []
    pop_size = 1000
    k = 20 # Size of tournament
    m = 200 # Size of mating pool
    e = 15 # Number of elites
    population = initial_population(pop_size, tasks)
    for i in range(1000):
        population = rank_paths(population, tasks)
        profit, path = fitness(population[0], tasks)
        if profit > best_profit:
            print(profit)
            best_profit = profit
            best_path = path
        mating_pool = []
        for i in range(m):
            tournament = random.sample(population, k)
            parent = max(tournament, key=lambda x:fitness(x, tasks))
            mating_pool.append(parent)
        mating_pool.sort(key=lambda x:fitness(x, tasks))
        children = breed_next_population(mating_pool, e, pop_size)
        population = mutationPopulation(children, 0.009)
    
    
    

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


def get_path(tasks):
    return random.sample(list(range(1, len(tasks)+1)), len(tasks))

def initial_population(pop_size, tasks):
    """Returns a solution object with a randomized feasible solution"""
    population = []
    for i in range(pop_size):
        path = get_path(tasks)
        population.append(path)
    return population

def rank_paths(population, tasks):
    fitness_map = {}
    for i in range(len(population)):
        fitness_map[i] = fitness(population[i], tasks)
    sorted_population = list(range(len(population)))
    sorted_population.sort(key = lambda x : fitness_map[x], reverse=True)
    return [population[i] for i in sorted_population]

def breed(parent1, parent2):
    used = {}
    child = [0]*len(parent1)

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        child[i] = parent1[i]
        used[parent1[i]] = 1
    parent2_index = 0
    child_index = 0
    while child_index < startGene:
        if parent2[parent2_index] not in used:
            child[child_index] = parent2[parent2_index]
            child_index += 1
        parent2_index += 1
    child_index = endGene
    while child_index < len(child):
        if parent2[parent2_index] not in used:
            child[child_index] = parent2[parent2_index]
            child_index += 1
        parent2_index += 1
    return child

def breed_next_population(mating_pool, elites, pop_size):
    ret = []
    for i in range(0, elites):
        ret.append(mating_pool[i])
    for i in range(0, pop_size-elites):
        parents = random.sample(mating_pool, 2)
        ret.append(breed(parents[0], parents[1]))
    return ret

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            task1 = individual[swapped]
            task2 = individual[swapWith]
            
            individual[swapped] = task2
            individual[swapWith] = task1
    return individual

def mutationPopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop
    
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
    tasks = read_input_file('inputs/small/small-10.in')
    output = solve(tasks)
    # output_path = 'outputs/large/large-291.out'
    # write_output_file(output_path, output)
    # for input_path in os.listdir('inputs'):
    #    for file_name in os.listdir('inputs/' + input_path):
    #         output_path = 'outputs/' + input_path + "/" + file_name[:len(file_name)-3] + '.out'
    #         tasks = read_input_file('inputs/' + input_path + "/" + file_name)
    #         print('inputs/' + input_path + "/" + file_name)
    #         output = solve(tasks)
    #         write_output_file(output_path, output)