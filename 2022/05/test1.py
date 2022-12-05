#!/usr/bin/env python3
import re

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x

def transform_lines_to_stacks(lines):
    labels = lines.pop()
    stack_number = len(labels)
    print(f"Found {stack_number} stacks")
    print(f"Found {len(lines)} lines")
    stacks = []
    for stack in range(0, stack_number):
        s = []
        for i in range(len(lines), 0, -1):
            crate = lines[i-1][stack]
            if crate != "":
                s.append(lines[i-1][stack])
        stacks.append(s)
    return stacks

def solve(data):
    """ Solve the puzzle and return the solution """
    lines = []
    moves = []
    while data[0] != "\n":
        line=data.pop(0)
        n=4 # Divided our lines by column of 4 char (either '[X] ' or '    ')
        lines.append([line[i:i+n].strip().replace('[','').replace(']','') for i in range(0, len(line), n)])
    stacks = transform_lines_to_stacks(lines)
    for move in data[1:]:
        m, source, target = re.findall(r'\d+', move.strip())
        for i in range(int(m)):
            if len(stacks[int(source)-1]) > 0:
                # We can't move anything from an empty stack
                moved_crate = stacks[int(source)-1].pop()
                stacks[int(target)-1].append(moved_crate)
    return ''.join(list(map(lambda x: x[-1], stacks)))


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == "CMZ"

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
