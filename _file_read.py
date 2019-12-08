with open('puzzle_input.txt') as input_file:
    instruction_list = [input_line.strip() for input_line in input_file]
    for problem_input in instruction_list:
        problem_output += get_primary_result(int(problem_input))
