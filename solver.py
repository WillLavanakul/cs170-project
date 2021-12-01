from parse import read_input_file, write_output_file
import os

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    # Profit matrix; assumes deadlines are all 1440.
    P = []
    mem = []
    for row in range (0, len(tasks)):
        profits = []
        hate = []
        for col in range (0, 1441):
            hate.append(float('-inf'))
            t = tasks[row]
            if col < t.get_duration():
                profits.append(0)
            elif col >= t.get_duration() and col <= t.get_deadline():
                profits.append(t.get_max_benefit())
            else:
                profits.append(t.get_late_benefit(col - t.get_deadline()))
        P.append(profits)
        mem.append(hate)
    pass


#change

# Here's an example of how to run your solver.
if __name__ == '__main__':
    tasks = read_input_file('part-1/test.in')
    output = solve(tasks)
    #for input_path in os.listdir('inputs'):
     #   for file_name in os.listdir('inputs/' + input_path):
      #      output_path = 'outputs/' + file_name + '.out'
       #     tasks = read_input_file('inputs/' + input_path + "/" + file_name)
        #    output = solve(tasks)
            #write_output_file(output_path, output)