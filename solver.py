from parse import read_input_file, write_output_file
import os

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    pass


# Here's an example of how to run your solver.
if __name__ == '__main__':
    for input_path in os.listdir('inputs'):
        for file_name in os.listdir('inputs/' + input_path):
            output_path = 'outputs/' + file_name + '.out'
            tasks = read_input_file('inputs/' + input_path + "/" + file_name)
            output = solve(tasks)
            #write_output_file(output_path, output)