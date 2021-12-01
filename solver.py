from parse import read_input_file, write_output_file
import os

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    # n = len(tasks)
    # mem = [[0] + [-float('inf')]*1440]*n
    # P = []
    # for i in range(n):
    #     row = []
    #     task = tasks[i]
    #     for j in range(0, 1441):
    #         if j > 0 and j < task.duration:
    #             row.append(0)
    #         elif j:
    #             row.append(task.get_late_benefit(j-task.deadline))
    #         else:
    #             row.append(0)
    #     print(row)
    #     P.append(row)

    # Profit matrix; assumes deadlines are all 1440.
    n = len(tasks)
    P = []
    for row in range (0, n):
        profits = []
        for col in range (0, 1441):
            t = tasks[row]
            if col < t.get_duration():
                profits.append(0)
            elif col >= t.get_duration() and col <= t.get_deadline():
                profits.append(t.get_max_benefit())
            else:
                profits.append(t.get_late_benefit(col - t.get_deadline()))
        P.append(profits)
    
    mem = [[0]*1441]
    largest = 0
    largest_id = [0, 0]
    for i in range(1, n+1):
        task = tasks[i-1]
        row = []
        for t in range(1441):
            t_prime = t - task.get_duration()
            if t_prime < 0:
                row.append(mem[i-1][t])
            else:
                profit = P[i-1][t]
                new = max(mem[i-1][t], profit + mem[i-1][t_prime])
                if new > largest:
                    largest_id = [i, t]
                largest = max(largest, new)
                row.append(new)
        mem.append(row)

    S = []
    def get_sequence(i, t):
        if i == 0:
            return
        if mem[i][t] == mem[i-1][t]:
            get_sequence(i-1, t)
        else:
            task = tasks[i-1]
            t_prime = t - task.get_duration()
            get_sequence(i-1, t_prime)
            S.append(i)

    get_sequence(largest_id[0], largest_id[1])
    return S


#change

# Here's an example of how to run your solver.
if __name__ == '__main__':
    for input_path in os.listdir('inputs'):
       for file_name in os.listdir('inputs/' + input_path):
            output_path = 'outputs/' + input_path + "/" + file_name[:len(file_name)-3] + '.out'
            tasks = read_input_file('inputs/' + input_path + "/" + file_name)
            print('inputs/' + input_path + "/" + file_name)
            output = solve(tasks)
            write_output_file(output_path, output)